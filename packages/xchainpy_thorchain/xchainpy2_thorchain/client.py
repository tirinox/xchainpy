import asyncio
import datetime
from collections import defaultdict
from typing import Optional, Union

from bip_utils import Bech32ChecksumError
from cosmpy.aerial.tx_helpers import SubmittedTx

from xchainpy2_client import AssetInfo, XcTx, TxType, Fees, FeeType, TokenTransfer
from xchainpy2_client import RootDerivationPaths, FeeBounds
from xchainpy2_client.fees import single_fee
from xchainpy2_cosmos import CosmosGaiaClient, TxLoadException, load_logs, TxInternalException
from xchainpy2_cosmos.utils import parse_cosmos_amount
from xchainpy2_crypto import decode_address
from xchainpy2_utils import Chain, NetworkType, AssetRUNE, RUNE_DECIMAL, CryptoAmount, Amount, remove_0x_prefix, \
    Asset, SYNTH_DELIMITER, parse_iso_date
from .const import NodeURL, DEFAULT_CHAIN_IDS, DEFAULT_CLIENT_URLS, DENOM_RUNE_NATIVE, ROOT_DERIVATION_PATHS, \
    THOR_EXPLORERS, DEFAULT_GAS_LIMIT_VALUE, DEPOSIT_GAS_LIMIT_VALUE, FALLBACK_CLIENT_URLS, DEFAULT_RUNE_FEE
from .utils import get_thor_address_prefix, build_deposit_tx_unsigned, get_deposit_tx_from_logs, get_asset_from_denom


class THORChainClient(CosmosGaiaClient):
    def __init__(self,
                 network=NetworkType.MAINNET,
                 phrase: Optional[str] = None,
                 fee_bound: Optional[FeeBounds] = None,
                 root_derivation_paths: Optional[RootDerivationPaths] = None,
                 client_urls=DEFAULT_CLIENT_URLS,
                 fallback_client_urls=FALLBACK_CLIENT_URLS,
                 chain_ids=DEFAULT_CHAIN_IDS,
                 explorer_providers=THOR_EXPLORERS,
                 ):
        """
        Initialize THORChainClient.
        :param network: Network type. Default is `NetworkType.MAINNET`
        :param phrase: Mnenomic phrase
        :param fee_bound: Fee bound structure. See: FeeBounds
        :param root_derivation_paths: Dictionary of derivation paths for each network type. See: ROOT_DERIVATION_PATHS
        :param client_urls: Dictionary of client urls for each network type. See: DEFAULT_CLIENT_URLS
        :param chain_ids: Dictionary of chain ids for each network type. See: DEFAULT_CHAIN_IDS
        :param explorer_providers: Dictionary of explorer providers for each network type. See: THOR_EXPLORERS
        """
        self.explorer_providers = explorer_providers.copy() if explorer_providers else THOR_EXPLORERS.copy()

        if isinstance(client_urls, NodeURL):
            client_urls = {network: client_urls}

        self.client_urls = client_urls.copy() if client_urls else DEFAULT_CLIENT_URLS.copy()
        self.fallback_client_urls = fallback_client_urls.copy() if fallback_client_urls else None

        self.chain_ids = chain_ids.copy() if chain_ids else DEFAULT_CHAIN_IDS.copy()

        root_derivation_paths = root_derivation_paths.copy() if root_derivation_paths else ROOT_DERIVATION_PATHS.copy()
        super().__init__(
            network, phrase, fee_bound, root_derivation_paths,
            self.client_urls, self.chain_ids, self.explorer_providers
        )

        # Tune for THORChain
        self.chain = Chain.THORChain
        self._prefix = get_thor_address_prefix(network)
        self.native_asset = AssetRUNE
        self._denom = DENOM_RUNE_NATIVE
        self._decimal = RUNE_DECIMAL
        self._gas_limit = DEFAULT_GAS_LIMIT_VALUE
        self._deposit_gas_limit = DEPOSIT_GAS_LIMIT_VALUE

        self._recreate_client()

    @property
    def server_url(self) -> str:
        return self.client_urls[self.network].node

    @property
    def rpc_url(self) -> str:
        return self.client_urls[self.network].rpc

    def validate_address(self, address: str) -> bool:
        if not super().validate_address(address):
            return False
        try:
            decode_address(address, self._prefix)
            return True
        except (ValueError, Bech32ChecksumError):
            return False

    def get_asset_info(self) -> AssetInfo:
        return AssetInfo(
            AssetRUNE, RUNE_DECIMAL
        )

    async def deposit(self,
                      what: Union[CryptoAmount, Amount, int, float],
                      memo: str,
                      second_asset: Optional[CryptoAmount] = None,
                      gas_limit: Optional[int] = None,
                      sequence: int = None,
                      account_number: int = None,
                      check_balance: bool = True,
                      fee=None,
                      wallet_index: int = 0,
                      return_full_response=False) -> Union[SubmittedTx, str]:
        """
        Send deposit transaction
        :param what: Amount and Asset
        :param second_asset: optional second asset if needed
        :param memo: Memo string (usually a command to the AMM)
        :param gas_limit: if not specified, we'll use the default value
        :param sequence: sequence number. If it is None, it will be fetched automatically
        :param check_balance: Flag to check the balance before sending Tx
        :param wallet_index: Wallet index, default is 0
        :param fee: string like "0rune", default is 0
        :param account_number: Your account number. If it is none, we will fetch it
        :param return_full_response: when it is not enough to have just tx hash

        :return: submitted tx hash or full response (SubmittedTt object) if requested
        """
        if isinstance(what, Amount):
            what = CryptoAmount(what, self.native_asset)
        elif isinstance(what, (int, float)):
            what = CryptoAmount(Amount.automatic(what, self._decimal), self.native_asset)

        address = self.get_address(wallet_index)

        if check_balance:
            await self.check_balance(address, what)

        if gas_limit is None:
            gas_limit = self._deposit_gas_limit

        if sequence is None or account_number is None:
            account = await self.get_account(address)
            sequence = account.sequence
            account_number = account.number

        public_key = self.get_public_key(wallet_index)

        tx = build_deposit_tx_unsigned(
            what, memo,
            public_key,
            fee=fee or self.get_amount_string(0),
            prefix=self.prefix,
            sequence_num=sequence,
            gas_limit=gas_limit,
            second_asset=second_asset,
        )

        tx.sign(
            self.get_private_key_cosmos(wallet_index),
            self.get_chain_id(),
            account_number=account_number
        )

        tx.complete()

        result = await asyncio.get_event_loop().run_in_executor(
            None,
            self._client.broadcast_tx,
            tx
        )

        return result if return_full_response else result.tx_hash

    async def fetch_transaction_from_thornode_raw(self, tx_hash: str) -> dict:
        """
        Fetch transaction from THORNode, try to use fallback client if main client is not available
        Url: https://node/thorchain/tx/{tx_hash}
        :param tx_hash: Tx Hash
        :return: Transaction data (raw, unparsed)
        """
        clients = [self.client_urls[self.network]]
        if self.fallback_client_urls:
            clients.extend(self.fallback_client_urls[self.network])

        exc = None
        for client in clients:
            try:
                url = f"{client.node}/thorchain/tx/{tx_hash}"
                j = await self._get_json(url)
                return j
            except Exception as e:
                exc = e
                continue
        if exc:
            raise exc

    async def get_transaction_data_thornode(self, tx_id: str) -> XcTx:
        """
        Fetch transaction data from THORNode (parsed to XcTx instance)
        This function is used when inbound or outbound tx is not of THORChain.
        It is called "getTransactionDataThornode" in xchainjs
        Parsing "observed_tx" object.
        Url: https://node/thorchain/tx/{tx_hash}
        :param tx_id: Tx Hash
        :return: XcTx result
        """
        if not tx_id:
            raise Exception("tx_id is not specified")

        # Remove 0x prefix if exists
        tx_id = remove_0x_prefix(tx_id)

        raw_data = await self.fetch_transaction_from_thornode_raw(tx_id)

        if not raw_data:
            raise TxLoadException(f"Could not fetch transaction data from THORNode {tx_id}")

        error = raw_data.get('error', '')
        if 'desc = internal' in error:
            raise TxInternalException(f"This transaction is internal: {tx_id}, please use cosmos RPC")
        elif error:
            raise TxLoadException(f"Could not fetch transaction data from THORNode {tx_id}. Reason: {error}")

        tx = raw_data['observed_tx']['tx']
        coin = tx['coins'][0]
        sender_asset = Asset.from_string_exc(coin['asset'])
        from_address = tx['from_address']
        decimals = coin.get('decimals', self._decimal)
        coin_amount = Amount.from_base(coin['amount'], decimals)

        transfers = [
            TokenTransfer(
                from_address, tx['to_address'],
                coin_amount, sender_asset, tx_id
            )
        ]

        split_memo = tx.get('memo', '').split(':')
        if not split_memo:
            raise TxLoadException('Could not parse memo')

        if split_memo[0] == 'OUT':
            asset = sender_asset
            address_to = tx.get('to_address', 'undefined')

            transfers.append(TokenTransfer(
                from_address, address_to,
                coin_amount, asset, tx_id, outbound=False
            ))

        else:
            asset = Asset.from_string_exc(split_memo[1])
            address = split_memo[2]
            amount = Amount.from_base(split_memo[3], self._decimal)

            transfers.append(TokenTransfer(
                from_address, address,
                coin_amount, asset, tx_id, outbound=False
            ))

        height = int(raw_data['observed_tx'].get('finalised_height', 0))

        return XcTx(
            sender_asset,
            transfers,
            datetime.datetime.fromtimestamp(0),
            TxType.TRANSFER,
            tx['id'],
            height
        )

    async def get_transaction_data(self, tx_id: str, address: str = '') -> XcTx:
        try:
            j = await self.get_transaction_data_cosmos(tx_id)
            response = j.get('tx_response')
            if not response:
                raise TxLoadException(f'Failed to get transaction logs (tx-hash: ${tx_id}): no tx_response')

            logs = load_logs(response.get('logs'))
            if not logs:
                raise TxLoadException(f'Failed to get transaction logs (tx-hash: ${tx_id})')

            transfers_event = logs[0].find_event('transfer')
            message_event = logs[0].find_event('message')
            if not transfers_event and not message_event:
                raise TxLoadException(f'Invalid transaction data, no transfer/no message (tx-hash: ${tx_id})')

            groups = defaultdict(list)
            for attr in transfers_event.attributes:
                groups[attr.key].append(attr.value)

            amt_group = groups['amount']
            amt_index = 1 if len(amt_group) >= 2 else 0
            asset_amount, denom = parse_cosmos_amount(amt_group[amt_index])
            from_asset = get_asset_from_denom(denom)

            if address:
                from_address = address
            else:
                from_address = transfers_event.find_attr_value_first('sender')

            memo = ''
            if (tx_j := j.get('tx')) and (body := tx_j.get('body')):
                memo = body['memo']
            memo_components = memo.split(':')
            n_memo = len(memo_components)
            to_address = memo_components[2] if n_memo > 2 else ''
            to_asset = Asset.from_string_exc(memo_components[1]) if n_memo > 1 else ''
            tx_date = parse_iso_date(response['timestamp'])
            tx_type = message_event.find_attr_value_first('action')
            tx_hash = response['txhash']
            height = int(response['height'])

            if not denom or not from_asset or not tx_hash or not from_address or not tx_type:
                return XcTx(
                    from_asset, [], tx_date, TxType.UNKNOWN, tx_hash, height,
                    memo=memo
                )

            tx_data = get_deposit_tx_from_logs(logs, from_address, from_asset, to_asset,
                                               self._decimal, self._denom, height)
            if not tx_data:
                raise TxLoadException('Failed to get transaction data')

            if to_asset == self.native_asset or to_asset.synth:
                return tx_data._replace(
                    date=tx_date,
                    hash=tx_hash,
                    type=tx_type,
                    asset=from_asset
                )
            else:
                to_amount = Amount.from_base(int(memo_components[3]))
                transfers = [
                    TokenTransfer(
                        from_address, to_address,
                        to_amount, to_asset, tx_hash
                    ),
                    TokenTransfer(
                        from_address, to_address,
                        Amount.from_base(asset_amount, self._decimal), from_asset, tx_hash, outbound=False
                    )
                ]
                #
                # from_txs = [
                #     TxFrom(from_address, tx_id, Amount.from_base(asset_amount, self._decimal), from_asset)
                # ],
                # to_txs = [
                #     TxTo(to_address, to_amount, to_asset)
                # ],

                return XcTx(
                    from_asset,
                    transfers=transfers,
                    date=tx_date,
                    type=TxType.TRANSFER,
                    hash=tx_hash,
                    height=height,
                    memo=memo,
                )

        except TxLoadException:
            return await self.get_transaction_data_thornode(tx_id)

    async def get_fees(self, cache=None, tc_fee_rate=None) -> Fees:
        return single_fee(FeeType.FLAT_FEE, DEFAULT_RUNE_FEE)

    def parse_denom_to_asset(self, denom: str) -> Asset:
        if SYNTH_DELIMITER in denom:
            # special case for synths
            return Asset.from_string(denom.upper())
        else:
            return super().parse_denom_to_asset(denom)

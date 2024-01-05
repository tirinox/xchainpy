import asyncio
from typing import Optional, Union

from bip_utils import Bech32ChecksumError
from cosmpy.aerial.tx import Transaction
from cosmpy.aerial.tx_helpers import SubmittedTx

from xchainpy2_client import AssetInfo, XcTx, TxType, Fees, FeeType, TokenTransfer
from xchainpy2_client import RootDerivationPaths, FeeBounds
from xchainpy2_client.fees import single_fee
from xchainpy2_cosmos import CosmosGaiaClient, TxLoadException, TxInternalException
from xchainpy2_cosmos.utils import parse_tx_response_json
from xchainpy2_crypto import decode_address
from xchainpy2_utils import Chain, NetworkType, AssetRUNE, RUNE_DECIMAL, CryptoAmount, Amount, remove_0x_prefix, \
    Asset, SYNTH_DELIMITER
from .const import NodeURL, DEFAULT_CHAIN_IDS, DEFAULT_CLIENT_URLS, DENOM_RUNE_NATIVE, ROOT_DERIVATION_PATHS, \
    THOR_EXPLORERS, DEFAULT_GAS_LIMIT_VALUE, DEPOSIT_GAS_LIMIT_VALUE, FALLBACK_CLIENT_URLS, DEFAULT_RUNE_FEE, \
    make_client_urls_from_ip_address
from .utils import get_thor_address_prefix, build_deposit_tx_unsigned, build_transfer_tx_draft


class THORChainClient(CosmosGaiaClient):
    @classmethod
    def from_node_ip(cls, ip: str):
        """
        Initialize THORChainClient from node IP address.
        :param ip: IP address of the node
        :return: THORChainClient
        """
        return cls(client_urls=make_client_urls_from_ip_address(ip))

    def __init__(self,
                 network=NetworkType.MAINNET,
                 phrase: Optional[str] = None,
                 private_key: Union[str, bytes, callable, None] = None,
                 fee_bound: Optional[FeeBounds] = None,
                 root_derivation_paths: Optional[RootDerivationPaths] = None,
                 client_urls=DEFAULT_CLIENT_URLS,
                 fallback_client_urls=FALLBACK_CLIENT_URLS,
                 chain_ids=DEFAULT_CHAIN_IDS,
                 explorer_providers=THOR_EXPLORERS,
                 wallet_index=0,
                 ):
        """
        Initialize THORChainClient.
        :param network: Network type. Default is `NetworkType.MAINNET`
        :param phrase: Mnemonic phrase
        :param private_key: Private key (if you want to use a private key instead of a mnemonic phrase)
        :param fee_bound: Fee bound structure. See: FeeBounds
        :param root_derivation_paths: Dictionary of derivation paths for each network type. See: ROOT_DERIVATION_PATHS
        :param client_urls: Dictionary of client urls for each network type. See: DEFAULT_CLIENT_URLS
        :param chain_ids: Dictionary of chain ids for each network type. See: DEFAULT_CHAIN_IDS
        :param explorer_providers: Dictionary of explorer providers for each network type. See: THOR_EXPLORERS
        :param wallet_index: int (wallet index, default 0) We can derive any number of addresses from a single seed
        """
        self.explorers = explorer_providers

        if isinstance(client_urls, NodeURL):
            client_urls = {network: client_urls}

        self.client_urls = client_urls.copy() if client_urls else DEFAULT_CLIENT_URLS.copy()
        self.fallback_client_urls = fallback_client_urls.copy() if fallback_client_urls else None

        self.chain_ids = chain_ids.copy() if chain_ids else DEFAULT_CHAIN_IDS.copy()

        root_derivation_paths = root_derivation_paths.copy() if root_derivation_paths else ROOT_DERIVATION_PATHS.copy()
        super().__init__(
            network, phrase, private_key, fee_bound, root_derivation_paths,
            self.client_urls, self.chain_ids, self.explorers,
            wallet_index
        )

        # Tune for THORChain
        self.chain = Chain.THORChain
        self._prefix = get_thor_address_prefix(network)
        self._gas_asset = AssetRUNE
        self._denom = DENOM_RUNE_NATIVE
        self._decimal = RUNE_DECIMAL
        self._gas_limit = DEFAULT_GAS_LIMIT_VALUE
        self._deposit_gas_limit = DEPOSIT_GAS_LIMIT_VALUE

        self._recreate_client()
        self._make_wallet()

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

    async def deposit(self,
                      what: Union[CryptoAmount, Amount, int, float],
                      memo: str,
                      second_asset: Optional[CryptoAmount] = None,
                      gas_limit: Optional[int] = None,
                      sequence: int = None,
                      account_number: int = None,
                      check_balance: bool = True,
                      fee=None,
                      return_full_response=False) -> Union[SubmittedTx, str]:
        """
        Send deposit transaction
        :param what: Amount and Asset
        :param second_asset: optional second asset if needed
        :param memo: Memo string (usually a command to the AMM)
        :param gas_limit: if not specified, we'll use the default value
        :param sequence: sequence number. If it is None, it will be fetched automatically
        :param check_balance: Flag to check the balance before sending Tx
        :param fee: string like "0rune", default is 0
        :param account_number: Your account number. If it is none, we will fetch it
        :param return_full_response: when it is not enough to have just tx hash

        :return: submitted tx hash or full response (SubmittedTt object) if requested
        """
        self._throw_if_empty_phrase()

        if isinstance(what, Amount):
            what = CryptoAmount(what, self._gas_asset)
        elif isinstance(what, (int, float)):
            what = CryptoAmount(Amount.automatic(what, self._decimal), self._gas_asset)

        address = self.get_address()

        if check_balance:
            await self.check_balance(address, what)

        if gas_limit is None:
            gas_limit = self._deposit_gas_limit

        if sequence is None or account_number is None:
            account = await self.get_account(address)
            sequence = account.sequence
            account_number = account.number

        public_key = self.get_public_key()

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
            self.get_private_key_cosmos(),
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
        from_address = tx.get('from_address')
        to_address = tx.get('to_address', 'undefined')
        decimals = coin.get('decimals', self._decimal)
        coin_amount = Amount.from_base(coin['amount'], decimals)
        memo = tx.get('memo', '')
        split_memo = memo.split(':')
        if not split_memo:
            raise TxLoadException('Could not parse memo')
        outbound = split_memo[0].upper() == 'OUT'

        transfers = [
            TokenTransfer(
                from_address, to_address,
                coin_amount, sender_asset, tx_id,
                outbound=outbound
            )
        ]

        height = int(raw_data.get('finalised_height', 0))
        return XcTx(sender_asset, transfers, None, TxType.TRANSFER, tx['id'], height, memo=memo,
                    original=raw_data)

    async def get_transaction_data(self, tx_id: str, address: str = '') -> XcTx:
        """
        Get transaction details by Tx Hash.
        :param tx_id:
        :param address:
        :return: XcTx
        """
        try:
            j = await self.get_transaction_data_cosmos(tx_id)
            return parse_tx_response_json(j, tx_id, address, self._decimal, self._denom, self._gas_asset)
        except TxLoadException:
            return await self.get_transaction_data_thornode(tx_id)

    async def get_fees(self, cache=None, tc_fee_rate=None) -> Fees:
        return single_fee(FeeType.FLAT_FEE, DEFAULT_RUNE_FEE)

    def parse_denom_to_asset(self, denom: str) -> Asset:
        if SYNTH_DELIMITER in denom:
            # special case for synths
            return Asset.from_string(denom.upper())
        elif denom == DENOM_RUNE_NATIVE:
            return AssetRUNE

    def get_denom(self, asset: Asset) -> str:
        if asset == AssetRUNE:
            return DENOM_RUNE_NATIVE
        else:
            return str(asset).lower()

    def build_transfer_tx(self, what: CryptoAmount, recipient: str) -> Transaction:
        tx = build_transfer_tx_draft(
            what, denom=self.get_denom(what.asset),
            sender=str(self._wallet.address()),
            recipient=recipient,
            prefix=self.prefix,
        )
        return tx

import asyncio
from typing import Optional, Union, List

from bip_utils import Bech32ChecksumError
from cosmpy.aerial.client import Coin
from cosmpy.aerial.tx import Transaction
from cosmpy.aerial.tx_helpers import SubmittedTx
from xchainpy2_mayanode import MimirApi, ApiClient

from xchainpy2_client import RootDerivationPaths, FeeBounds
from xchainpy2_client import XcTx, TxType, Fees, FeeType, TokenTransfer
from xchainpy2_client.fees import single_fee
from xchainpy2_cosmos import CosmosGaiaClient, TxLoadException, TxInternalException
from xchainpy2_cosmos.utils import parse_tx_response_json
from xchainpy2_crypto import decode_address
from xchainpy2_utils import Chain, NetworkType, CryptoAmount, Amount, remove_0x_prefix, \
    Asset, SYNTH_DELIMITER, CACAO_DECIMAL, AssetCACAO
from .const import NodeURL, DEFAULT_CHAIN_IDS, DEFAULT_CLIENT_URLS, DENOM_CACAO_NATIVE, ROOT_DERIVATION_PATHS, \
    DEFAULT_GAS_LIMIT_VALUE, DEPOSIT_GAS_LIMIT_VALUE, FALLBACK_CLIENT_URLS, make_client_urls_from_ip_address, \
    DEFAULT_MAYA_EXPLORERS, AssetMAYA, DENOM_MAYA, MAYA_DECIMAL, CACAO_DUST, \
    DEFAULT_CACAO_NETWORK_FEE
from .mrc20.api import MayaScanClient, MayaScanException
from .mrc20.const import is_mrc20, make_mrc20_asset, MRC20_DECIMALS
from .mrc20.memo import MRC20Memo, MNFTMemo
from .utils import build_deposit_tx_unsigned, get_maya_address_prefix, build_transfer_tx_draft


class MayaChainClient(CosmosGaiaClient):
    @classmethod
    def from_node_ip(cls, ip: str):
        """
        Initialize MayaChainClient from node IP address.
        :param ip: IP address of the node
        :return: MayaChainClient
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
                 explorer_providers=DEFAULT_MAYA_EXPLORERS,
                 wallet_index=0,
                 ):
        """
        Initialize MayaChainClient.
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
        self.mayanode_api_client = ApiClient()

        if isinstance(client_urls, NodeURL):
            client_urls = {network: client_urls}

        self._client_urls = client_urls.copy() if client_urls else DEFAULT_CLIENT_URLS.copy()
        self.fallback_client_urls = fallback_client_urls.copy() if fallback_client_urls else None

        self.chain_ids = chain_ids.copy() if chain_ids else DEFAULT_CHAIN_IDS.copy()

        self.explorers = explorer_providers

        root_derivation_paths = root_derivation_paths.copy() if root_derivation_paths else ROOT_DERIVATION_PATHS.copy()
        super().__init__(
            network, phrase, private_key, fee_bound, root_derivation_paths,
            self._client_urls, self.chain_ids, self.explorers, wallet_index
        )
        self._fee_minimum_gas_price = 0

        # Tune for MayaChain
        self.chain = Chain.Maya
        self._prefix = get_maya_address_prefix(network)
        self._gas_asset = AssetCACAO
        self._denom = DENOM_CACAO_NATIVE
        self._decimal = CACAO_DECIMAL
        self._gas_limit = DEFAULT_GAS_LIMIT_VALUE
        self._deposit_gas_limit = DEPOSIT_GAS_LIMIT_VALUE
        self.standard_tx_fee = DEFAULT_CACAO_NETWORK_FEE.amount

        self._recreate_client()
        self._make_wallet()

        self.maya_scan = MayaScanClient()
        self.mayanode_api_client.configuration.host = self._client_urls[self.network].node

    @property
    def server_url(self) -> str:
        return self._client_urls[self.network].node

    @property
    def rpc_url(self) -> str:
        return self._client_urls[self.network].rpc

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
        Send a deposit transaction. MsgDeposit is a special kind of transaction to invoke MayaChain protocol's action
        like swap or liquidity addition. Note! It is not on ordinary transfer of tokens. It has no destination
        address.
        For more info see: https://dev.thorchain.org/concepts/sending-transactions.html?highlight=MsgDeposit#thorchain

        :param what: Amount and Asset
        :param second_asset: optional second asset if needed
        :param memo: Memo string (usually a command to the AMM)
        :param gas_limit: if not specified, we'll use the default value
        :param sequence: sequence number. If it is None, it will be fetched automatically
        :param check_balance: Flag to check the balance before sending Tx
        :param fee: string like "0cacao", default is 0
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

    async def fetch_transaction_from_mayanode_raw(self, tx_hash: str) -> dict:
        """
        Fetch transaction from MayaNode, try to use fallback client if main client is not available
        Url: https://node/mayachain/tx/{tx_hash}
        :param tx_hash: Tx Hash
        :return: Transaction data (raw, unparsed)
        """
        clients = [self._client_urls[self.network]]
        if self.fallback_client_urls:
            clients.extend(self.fallback_client_urls[self.network])

        exc = None
        for client in clients:
            try:
                url = f"{client.node}/mayachain/tx/{tx_hash}"
                j = await self._get_json(url)
                return j
            except Exception as e:
                exc = e
                continue
        if exc:
            raise exc

    async def get_transaction_data_mayanode(self, tx_id: str) -> XcTx:
        """
        Fetch transaction data from MayaNode (parsed to XcTx instance)
        This function is used when inbound or outbound tx is not of MayaChain.
        It is called "getTransactionDataThornode" in xchainjs
        Parsing "observed_tx" object.
        Url: https://node/mayachain/tx/{tx_hash}
        :param tx_id: Tx Hash
        :return: XcTx result
        """
        if not tx_id:
            raise Exception("tx_id is not specified")

        # Remove 0x prefix if exists
        tx_id = remove_0x_prefix(tx_id)

        raw_data = await self.fetch_transaction_from_mayanode_raw(tx_id)

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
            return await self.get_transaction_data_mayanode(tx_id)

    async def get_fees(self) -> Fees:
        mimir_api = MimirApi(self.mayanode_api_client)
        mimir_params = await mimir_api.mimir()

        fee_param = mimir_params.get('NATIVETRANSACTIONFEE')
        try:
            fee_param = int(fee_param)
            if fee_param < 0:
                raise ValueError
        except ValueError:
            raise ValueError(f"Invalid native TX fee in Mimir: {fee_param}")

        return single_fee(FeeType.FLAT_FEE, Amount.from_base(fee_param, self._decimal))

    def parse_denom_to_asset(self, denom: str) -> Asset:
        if SYNTH_DELIMITER in denom:
            # special case for synths
            return Asset.from_string(denom.upper())
        elif denom == DENOM_MAYA:
            return AssetMAYA
        elif denom == DENOM_CACAO_NATIVE:
            return AssetCACAO

    def convert_coin_to_amount(self, c: Coin) -> CryptoAmount:
        if c.denom == DENOM_MAYA:
            decimal = MAYA_DECIMAL
        elif c.denom == DENOM_CACAO_NATIVE:
            decimal = CACAO_DECIMAL
        else:
            decimal = 8

        return CryptoAmount(
            Amount.from_base(c.amount, decimal),
            asset=self.parse_denom_to_asset(c.denom)
        )

    def get_denom(self, asset: Asset) -> str:
        if asset == AssetCACAO:
            return DENOM_CACAO_NATIVE
        elif asset == AssetMAYA:
            return DENOM_MAYA
        else:
            return str(asset).lower()

    def build_transfer_tx(self, what: CryptoAmount, recipient: str) -> Transaction:
        self._make_wallet()
        tx = build_transfer_tx_draft(
            what, denom=self.get_denom(what.asset),
            sender=str(self._wallet.address()),
            recipient=recipient,
            prefix=self.prefix,
        )
        return tx

    def _maya_scan_tx_value_cacao(self):
        return self.gas_amount(CACAO_DUST)

    async def transfer_mrc20(self, what: CryptoAmount, recipient: str):
        """
        Transfer MRC20 token
        Example: await maya.transfer_mrc20(CryptoAmount.automatic(100, 'MRC20.GLD'), 'maya1f4f2a4b24')
        :param what: CryptoAmount
        :param recipient: maya1Address
        :return: TX hash string
        """
        if not self.validate_address(recipient):
            raise ValueError(f"Invalid recipient address: {recipient}")

        if not is_mrc20(what.asset):
            raise ValueError(f"Asset {what.asset} is not MRC20")

        memo = MRC20Memo.transfer(what.asset.symbol, what.amount)

        return await self._mrc20_submit_tx(memo, recipient)

    async def transfer_mnft(self, symbol: str, ident: int, recipient: str):
        """
        Transfer MNFT token
        Example: await maya.transfer_mnft('PEPE', 25, 'maya1f4f2a4b24')
        :param symbol: MNFT ticker
        :param ident: MNFT token ID
        :param recipient: maya1Address
        :return: TX hash string
        """
        if not self.validate_address(recipient):
            raise ValueError(f"Invalid recipient address: {recipient}")

        memo = MNFTMemo.transfer(symbol, ident)

        return await self.transfer(
            self._maya_scan_tx_value_cacao(),
            recipient, memo=memo,
            check_balance=False,
        )

    @staticmethod
    def amount_of_mrc20(amount, asset_name: str):
        return CryptoAmount.automatic(amount, make_mrc20_asset(asset_name))

    async def close(self):
        if self.maya_scan:
            await self.maya_scan.close()

    async def transfer(self, what: CryptoAmount, recipient: str, memo: Optional[str] = None,
                       fee_rate: Optional[int] = None, check_balance: bool = True) -> str:
        if is_mrc20(what.asset):
            return await self.transfer_mrc20(what, recipient)
        else:
            return await super().transfer(what, recipient, memo, fee_rate, check_balance)

    transfer.__doc__ = CosmosGaiaClient.transfer.__doc__

    async def get_balance(self, address: str = '', include_mrc20=True) -> List[CryptoAmount]:
        if not address:
            address = self.get_address()

        on_chain_balances = await super().get_balance(address)
        if include_mrc20:
            try:
                mrc20_balances = await self.maya_scan.get_balance(address)
                mrc20_balances = [
                    CryptoAmount(Amount.from_base(b.balance, b.decimals), make_mrc20_asset(b.ticker))
                    for b in mrc20_balances
                ]
                on_chain_balances.extend(mrc20_balances)
            except MayaScanException as e:
                # "not found" means zero balances, that is OK
                if not e.is_not_found:
                    raise

        return on_chain_balances

    get_balance.__doc__ = CosmosGaiaClient.get_balance.__doc__

    async def _mrc20_submit_tx(self, memo: str, recipient=''):
        if not recipient:
            recipient = self.get_address()
        return await self.transfer(
            self._maya_scan_tx_value_cacao(),
            recipient, memo=memo,
            check_balance=False,
        )

    async def mrc20_cancel_order(self, ticker: Union[str, Asset], tx_hash: str):
        """
        Cancel MRC20 sell order
        :param ticker: ticker of MRC20 token (e.g. GLD)
        :param tx_hash: exact hash of the transaction that created the order
        :return: txid of the cancel transaction
        """
        memo = MRC20Memo.cancel(ticker, tx_hash)
        return await self._mrc20_submit_tx(memo)

    async def mrc20_sell(self, ticker: Union[str, Asset], amount: Union[CryptoAmount, Amount, int, float],
                         price: float):
        """
        Post an order to sell MRC20 token
        :param ticker: ticker of MRC20 token (e.g. GLD)
        :param amount: amount of MRC20 token to sell
        :param price: price of MRC20 token in CACAO
        :return: txid of the sell transaction
        """
        amount = Amount.automatic(amount, MRC20_DECIMALS)
        price = Amount.automatic(price, MRC20_DECIMALS)

        memo = MRC20Memo.sell(ticker, int(amount), int(price))
        return await self._mrc20_submit_tx(memo)

    async def mrc20_buy(self, ticker: Union[str, Asset],
                        amount: Union[CryptoAmount, Amount, int, float],
                        seller_address: str,
                        tx_hash: str):
        """
        Buy MRC20 token from the seller
        :param ticker: ticker of MRC20 token (e.g. GLD)
        :param amount: amount of MRC20 token to buy
        :param seller_address: seller address
        :param tx_hash: exact hash of the transaction that created the order
        :return: txid of the buy transaction
        """
        if not tx_hash:
            raise ValueError("tx_hash of the selling tx is not specified")

        if not self.validate_address(seller_address):
            raise ValueError(f"Invalid seller address: {seller_address}")
        amount = Amount.automatic(amount, MRC20_DECIMALS)
        memo = MRC20Memo.buy(ticker, amount, tx_hash)
        return await self._mrc20_submit_tx(memo, recipient=seller_address)

    async def wait_for_transaction(self, tx_id: str):
        raise NotImplemented

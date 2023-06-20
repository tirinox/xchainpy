import asyncio
from datetime import datetime
from math import ceil
from typing import Optional, List
from urllib.parse import urlencode

from cosmpy.aerial.client import LedgerClient, Account
from cosmpy.aerial.config import NetworkConfig
from cosmpy.aerial.wallet import LocalWallet
from cosmpy.crypto.address import Address

from xchainpy2_client import XChainClient, RootDerivationPaths, FeeBounds, TxParams, XcTx, \
    Fees, TxPage, AssetInfo, FeeType
from xchainpy2_client.fees import single_fee
from xchainpy2_crypto import derive_private_key, derive_address
from xchainpy2_utils import Chain, NetworkType, CryptoAmount, AssetRUNE, RUNE_DECIMAL, Asset, Amount, AssetATOM
from .const import DEFAULT_CLIENT_URLS, DEFAULT_EXPLORER_PROVIDER, COSMOS_ROOT_DERIVATION_PATHS, COSMOS_ADDR_PREFIX, \
    COSMOS_CHAIN_IDS, COSMOS_DECIMAL, TxFilterFunc, MAX_PAGES_PER_FUNCTION_CALL, MAX_TX_COUNT_PER_PAGE, \
    MAX_TX_COUNT_PER_FUNCTION_CALL, COSMOS_DENOM, DEFAULT_FEE
from .models import TxHistoryResponse, TxResponse
from .utils import parse_tx_response, get_asset


class CosmosGaiaClient(XChainClient):
    def __init__(self,
                 network=NetworkType.MAINNET,
                 phrase: Optional[str] = None,
                 fee_bound: Optional[FeeBounds] = None,
                 root_derivation_paths: Optional[RootDerivationPaths] = None,
                 client_urls=DEFAULT_CLIENT_URLS,
                 chain_ids=COSMOS_CHAIN_IDS,
                 explorer_providers=DEFAULT_EXPLORER_PROVIDER,
                 ):
        """
        Initialize CosmosClient
        :param network: Network type. Default is `NetworkType.MAINNET`
        :param phrase: Mnenomic phrase
        :param fee_bound: Fee bound structure. See: FeeBounds
        :param root_derivation_paths: Dictionary of derivation paths for each network type. See: ROOT_DERIVATION_PATHS
        :param client_urls: Dictionary of client urls for each network type.
        :param chain_ids: Dictionary of chain ids for each network type.
        :param explorer_providers: Dictionary of explorer providers for each network type.
        """
        root_derivation_paths = root_derivation_paths.copy() \
            if root_derivation_paths else COSMOS_ROOT_DERIVATION_PATHS.copy()
        super().__init__(Chain.Cosmos, network, phrase, fee_bound, root_derivation_paths)

        self.explorer_providers = explorer_providers.copy() \
            if explorer_providers else DEFAULT_EXPLORER_PROVIDER.copy()

        if isinstance(client_urls, str):
            client_urls = {NetworkType.MAINNET: client_urls}

        self.client_urls = client_urls.copy() if client_urls else DEFAULT_CLIENT_URLS.copy()
        self.chain_ids = chain_ids.copy() if chain_ids else COSMOS_CHAIN_IDS.copy()

        self._client: Optional[LedgerClient] = None
        self._recreate_client()

        self._wallet: Optional[LocalWallet] = None
        self.native_asset = AssetATOM

    def get_client(self) -> LedgerClient:
        return self._client

    @property
    def server_url(self):
        return self.client_urls[self.network]

    def _recreate_client(self):
        rest_url = f'rest+{self.server_url}'
        self._client = LedgerClient(NetworkConfig(
            chain_id=self.chain_ids[self.network],
            url=rest_url,
            fee_denomination=COSMOS_DENOM,
            staking_denomination=COSMOS_DENOM,
            fee_minimum_gas_price=0,
        ))

    def set_chain_id(self, chain_id: str):
        """
        Set/update the current chain id.
        :param chain_id:
        :return: None
        """
        # dirty check to avoid using and re-creation of same data
        if chain_id == self.chain_ids[self.network]:
            return
        self.chain_ids[self.network] = chain_id
        self._recreate_client()

    def get_chain_id(self):
        return self.chain_ids[self.network]

    def set_network(self, network: NetworkType):
        """
        Set/update the current network.
        :param network:
        :return: None
        """
        # dirty check to avoid using and re-creation of same data
        if network == self.network:
            return
        super().set_network(network)
        self._recreate_client()

    def get_network(self):
        return self.network

    def set_phrase(self, phrase: str, wallet_index: int = 0):
        super().set_phrase(phrase, wallet_index)

    def purge_client(self):
        super().purge_client()

    @property
    def explorer(self):
        return self.explorer_providers[self.network]

    def get_explorer_url(self) -> str:
        return self.explorer.explorer_url

    def get_explorer_address_url(self, address: str) -> str:
        """
        Get the explorer url for the given address.
        :param address: Address string
        :return: The explorer url for the given address.
        """
        return self.explorer.get_address_url(address)

    def get_explorer_tx_url(self, tx_id: str) -> str:
        """
        Get the explorer url for the given transaction id.
        :param tx_id: Transaction id or hash string
        :return: The explorer url for the given transaction id.
        """
        return self.explorer.get_tx_url(tx_id)

    def validate_address(self, address: str) -> bool:
        """
        Validates a Cosmos address.
        :param address: Address string
        :return: True if valid, False otherwise.
        """

        if not address:
            return False

        if not address.startswith(COSMOS_ADDR_PREFIX):
            return False

        try:
            Address(address)
            return True
        except Exception:
            return False

    def get_address(self, wallet_index=0) -> str:
        """
        Get the address for the given wallet index.
        :param wallet_index: Wallet index. Default is 0.
        :return: string address
        """
        return derive_address(self.phrase,
                              self.get_full_derivation_path(wallet_index),
                              prefix=COSMOS_ADDR_PREFIX)

    def get_private_key(self, wallet_index=0) -> str:
        """
        Get the private key for the given wallet index.
        :param wallet_index: Wallet index. Default is 0.
        :return:
        """
        return derive_private_key(self.phrase, self.get_full_derivation_path(wallet_index)).hex()

    async def get_balance(self, address: str = '') -> List[CryptoAmount]:
        """
        Get the balance of a given address.
        :param address: By default, it will return the balance of the current wallet. (optional)
        :return:
        """
        if not address:
            address = self.get_address()

        address = Address(address)
        balances = await asyncio.get_event_loop().run_in_executor(
            None,
            self._client.query_bank_all_balances,
            address
        )

        our_balances = [
            CryptoAmount(
                Amount.from_base(balance.amount, COSMOS_DECIMAL),
                Asset(Chain.Cosmos.value, balance.denom.upper())
            )
            for balance in balances
        ]

        return our_balances

    async def get_account(self, address: str) -> Optional[Account]:
        """
        Get the account information for the given address: number and sequence.
        It there is no account, it will return None.
        It will throw an exception for special addresses (like Reserve)
        :param address: By default, it will return the account of the current wallet. (optional)
        :return:
        """
        address = Address(address)

        try:
            account = await asyncio.get_event_loop().run_in_executor(
                None,
                self._client.query_account,
                address
            )
            return account
        except RuntimeError as e:
            if 'NotFound' in str(e):
                return
            raise e

    async def get_transactions(self, address: str,
                               offset: int = 0,
                               limit: int = 0,
                               start_time: Optional[datetime] = None,
                               end_time: Optional[datetime] = None,
                               asset: Optional[Asset] = None,
                               filter_function: TxFilterFunc = None) -> TxPage:
        message_action = None

        address = address if address else self.get_address()
        tx_min_height = None
        tx_max_height = None
        asset = get_asset(asset) if asset else AssetATOM

        if limit + offset > MAX_PAGES_PER_FUNCTION_CALL * MAX_TX_COUNT_PER_PAGE:
            raise ValueError(
                f"limit plus offset can not be grater than {MAX_PAGES_PER_FUNCTION_CALL * MAX_TX_COUNT_PER_PAGE}")

        if limit > MAX_TX_COUNT_PER_FUNCTION_CALL:
            raise ValueError(f"Maximum number of transaction per call is {MAX_TX_COUNT_PER_FUNCTION_CALL}")

        pages_number = int(ceil((limit + offset) / MAX_TX_COUNT_PER_PAGE))

    async def search_tx(self, message_action=None, message_sender=None, page=0, limit=50):
        if not message_action and not message_sender:
            raise ValueError('One of message_action or message_sender must be specified')

        events_param = ''
        if message_action is not None:
            events_param = f"message.action='{message_action}'"
        if message_sender is not None:
            prefix = ',' if events_param else ''
            events_param += f"{prefix}message.sender='{message_sender}'"

        query_parameter = {'events': events_param}

        if page is not None:
            query_parameter['page'] = page
        if limit is not None:
            query_parameter['limit'] = limit

        url = f"{self.server_url}/cosmos/tx/v1beta1/txs?{urlencode(query_parameter)}"
        j = await self._get_json(url)
        return TxHistoryResponse.from_rpc_json(j)

    async def get_transaction_data(self, tx_id: str, asset_address: Optional[str]) -> XcTx:
        """
        Get the transaction data for the given transaction id.
        :param tx_id:
        :param asset_address:
        :return:
        """
        url = f"{self.server_url}/cosmos/tx/v1beta1/txs/{tx_id}"
        j = await self._get_json(url)

        return parse_tx_response(TxResponse.from_rpc_json(j), self.native_asset)

    async def get_fees(self, cache=None, tc_fee_rate=None) -> Fees:
        """
        Returns fees.
        It tries to get chain fees from THORChain `inbound_addresses` first
        :param cache: THORChainCache from the query module
        :param tc_fee_rate: You can externally pass the fee rate having 8 decimals. (optional)
        :return:
        """
        if tc_fee_rate is None:
            tc_fee_rate = await cache.get_fee_rates(self.chain)
        else:
            return single_fee(FeeType.FLAT_FEE, DEFAULT_FEE)

        # convert decimal: 1e8 (THORChain) to 1e6 (COSMOS)
        # Similar to `fromCosmosToThorchain` in THORNode
        decimal_diff = COSMOS_DECIMAL - RUNE_DECIMAL
        fee_rate = Amount.from_base(tc_fee_rate * 10 ** decimal_diff, COSMOS_DECIMAL)
        return single_fee(FeeType.FLAT_FEE, fee_rate)

    async def transfer(self, params: TxParams) -> XcTx:
        pass

    async def broadcast_tx(self, tx_hex: str) -> str:
        pass

    def get_asset_info(self) -> AssetInfo:
        return AssetInfo(
            AssetRUNE, RUNE_DECIMAL
        )

    async def get_chain_id(self, server='') -> str:
        """
        Helper to get Cosmos' chain id
        :return:
        """
        url = f"{server or self.server_url}/node_info"
        j = await self._get_json(url)
        return j['node_info']['network']

    async def _get_json(self, url):
        response = await asyncio.get_event_loop().run_in_executor(
            None,
            self._client.txs.rest_client._session.get,
            url,
        )
        if response.status_code != 200:
            raise Exception(f"Error getting {url}: {response.status_code} {response.text}")
        return response.json()

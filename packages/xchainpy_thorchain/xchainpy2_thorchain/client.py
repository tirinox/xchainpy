import asyncio
from datetime import datetime
from math import ceil
from typing import Optional, List

from bip_utils import Bech32ChecksumError
from cosmpy.aerial.client import LedgerClient, Address, Account
from cosmpy.aerial.config import NetworkConfig
from cosmpy.aerial.wallet import LocalWallet

from packages.xchainpy_client.xchainpy2_client import XChainClient, RootDerivationPaths, FeeBounds, XcTx, \
    Fees, TxPage
from xchainpy2_client import AssetInfo
from xchainpy2_crypto import derive_private_key, derive_address, decode_address
from xchainpy2_utils import Chain, NetworkType, CryptoAmount, AssetRUNE, RUNE_DECIMAL, Asset
from . import ThorTxFilterFunc
from .const import NodeURL, DEFAULT_CHAIN_IDS, DEFAULT_CLIENT_URLS, DENOM_RUNE_NATIVE, ROOT_DERIVATION_PATHS, \
    THOR_EXPLORERS, MAX_TX_COUNT_PER_PAGE, MAX_PAGES_PER_FUNCTION_CALL, MAX_TX_COUNT_PER_FUNCTION_CALL
from .utils import get_thor_address_prefix, convert_coin_to_crypto_amount


class THORChainClient(XChainClient):
    def __init__(self,
                 network=NetworkType.MAINNET,
                 phrase: Optional[str] = None,
                 fee_bound: Optional[FeeBounds] = None,
                 root_derivation_paths: Optional[RootDerivationPaths] = None,
                 client_urls=DEFAULT_CLIENT_URLS,
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
        root_derivation_paths = root_derivation_paths.copy() if root_derivation_paths else ROOT_DERIVATION_PATHS.copy()
        super().__init__(Chain.THORChain, network, phrase, fee_bound, root_derivation_paths)

        if isinstance(client_urls, NodeURL):
            client_urls = {network: client_urls}

        self.explorer_providers = explorer_providers.copy() if explorer_providers else THOR_EXPLORERS.copy()
        self.client_urls = client_urls.copy() if client_urls else DEFAULT_CLIENT_URLS.copy()
        self.chain_ids = chain_ids.copy() if chain_ids else DEFAULT_CHAIN_IDS.copy()

        self._client: Optional[LedgerClient] = None
        self._recreate_client()

        self._wallet: Optional[LocalWallet] = None

    def _recreate_client(self):
        base_url = self.client_urls[self.network].node
        rest_url = f'rest+{base_url}'
        self._client = LedgerClient(NetworkConfig(
            chain_id=self.chain_ids[self.network],
            url=rest_url,
            fee_denomination=DENOM_RUNE_NATIVE,
            staking_denomination=DENOM_RUNE_NATIVE,
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
        self._client = None

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
        if not address:
            return False

        prefix = get_thor_address_prefix(self.network)

        if not address.startswith(prefix):
            return False

        try:
            decode_address(address, prefix)
        except (ValueError, Bech32ChecksumError):
            return False

        return True

    def get_address(self, wallet_index=0) -> str:
        """
        Get the address for the given wallet index.
        :param wallet_index: Wallet index. Default is 0.
        :return: string address
        """
        return derive_address(self.phrase,
                              self.get_full_derivation_path(wallet_index),
                              get_thor_address_prefix(self.network))

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
            convert_coin_to_crypto_amount(coin)
            for coin in balances
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
                               filter_function: ThorTxFilterFunc = None) -> TxPage:
        message_action = None

        offset = offset if offset is None else 0
        limit = limit if limit else 10
        address = address if address else self.get_address()
        tx_min_height = None
        tx_max_height = None

        if limit + offset > MAX_PAGES_PER_FUNCTION_CALL * MAX_TX_COUNT_PER_PAGE:
            raise ValueError(
                f"limit plus offset can not be grater than {MAX_PAGES_PER_FUNCTION_CALL * MAX_TX_COUNT_PER_PAGE}")

        if limit > MAX_TX_COUNT_PER_FUNCTION_CALL:
            raise ValueError(f"Maximum number of transaction per call is {MAX_TX_COUNT_PER_FUNCTION_CALL}")

        pages_number = int(ceil((limit + offset) / MAX_TX_COUNT_PER_PAGE))

    async def get_transaction_data(self, tx_id: str, asset_address: Optional[str]) -> XcTx:
        pass

    async def get_fees(self, **kwargs) -> Fees:
        pass

    async def transfer(self, what: CryptoAmount,
                       recipient: str,
                       memo: Optional[str] = None,
                       fee_rate: Optional[int] = None
                       ) -> XcTx:
        pass

    async def broadcast_tx(self, tx_hex: str) -> str:
        pass

    def get_asset_info(self) -> AssetInfo:
        return AssetInfo(
            AssetRUNE, RUNE_DECIMAL
        )

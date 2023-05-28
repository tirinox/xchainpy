from typing import Optional, List

from cosmpy.aerial.client import LedgerClient
from cosmpy.aerial.config import NetworkConfig
from cosmpy.aerial.wallet import LocalWallet

from packages.xchainpy_client.xchainpy2_client import XChainClient, RootDerivationPaths, FeeBounds, TxParams, XcTx, \
    Fees, TxHistoryParams, TxPage
from xchainpy2_utils import Chain, NetworkType, Address, CryptoAmount
from . import get_thor_address_prefix
from .const import NodeURL, DEFAULT_CHAIN_IDS, DEFAULT_CLIENT_URLS, DENOM_RUNE_NATIVE, ROOT_DERIVATION_PATHS, \
    THOR_EXPLORERS


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
        self._client = LedgerClient(NetworkConfig(
            chain_id=self.chain_ids[self.network],
            url=self.client_urls[self.network].node,
            fee_denomination=DENOM_RUNE_NATIVE,
            staking_denomination=DENOM_RUNE_NATIVE,
            fee_minimum_gas_price=0,
        ))

    def _recreate_wallet(self):
        self._wallet = LocalWallet(
            self.get_private_key(),
            get_thor_address_prefix(self.network)
        )

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
        self._recreate_wallet()

    def get_network(self):
        return self.network

    def set_phrase(self, phrase: str, wallet_index: int = 0):
        pass

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
        pass

    def get_address(self, wallet_index=0) -> str:
        pass

    def get_private_key(self, wallet_index=0) -> str:
        """
        Get the private key for the given wallet index.
        :param wallet_index: Wallet index. Default is 0.
        :return:
        """
        return self._wallet.signer().private_key

    async def get_balance(self, address: str) -> List[CryptoAmount]:
        pass

    async def get_transactions(self, params: Optional[TxHistoryParams]) -> TxPage:
        pass

    async def get_transaction_data(self, tx_id: str, asset_address: Optional[Address]) -> XcTx:
        pass

    async def get_fees(self) -> Fees:
        pass

    async def transfer(self, params: TxParams) -> XcTx:
        pass

    async def broadcast_tx(self, tx_hex: str) -> str:
        pass

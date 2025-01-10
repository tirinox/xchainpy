from web3.middleware import geth_poa_middleware
from web3.providers import BaseProvider

from xchainpy2_avalanche import DEFAULT_AVAX_EXPLORER_PROVIDERS
from xchainpy2_base import BASE_TOKEN_LIST, BASE_DECIMALS, BASE_CHAIN_ID, FREE_BASE_PROVIDERS
from xchainpy2_ethereum import EthereumClient
from xchainpy2_ethereum.utils import select_random_free_provider
from xchainpy2_utils import Chain, AssetBaseETH


class BaseClient(EthereumClient):
    _CHAIN = Chain.Base
    _TOKEN_LIST = BASE_TOKEN_LIST
    _GAS_ASSET = AssetBaseETH
    _DECIMAL = BASE_DECIMALS
    _CHAIN_ID_DICT = BASE_CHAIN_ID
    _EXPLORERS = DEFAULT_AVAX_EXPLORER_PROVIDERS.copy()

    def _get_default_provider(self):
        return select_random_free_provider(self.network, FREE_BASE_PROVIDERS)

    def _remake_provider(self, provider: BaseProvider):
        super()._remake_provider(provider)
        self.web3.middleware_onion.inject(geth_poa_middleware, layer=0)

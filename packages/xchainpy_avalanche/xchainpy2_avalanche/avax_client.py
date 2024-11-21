from web3.middleware import geth_poa_middleware
from web3.providers import BaseProvider

from xchainpy2_ethereum import EthereumClient
from xchainpy2_ethereum.utils import select_random_free_provider
from xchainpy2_utils import Chain, AssetAVAX
from .const import DEFAULT_AVAX_EXPLORER_PROVIDERS, AVAX_DECIMALS, AVAX_CHAIN_ID, FREE_AVAX_PROVIDERS, AVAX_TOKEN_LIST


class AvalancheClient(EthereumClient):
    _CHAIN = Chain.Avalanche
    _TOKEN_LIST = AVAX_TOKEN_LIST
    _GAS_ASSET = AssetAVAX
    _DECIMAL = AVAX_DECIMALS
    _CHAIN_ID_DICT = AVAX_CHAIN_ID
    _EXPLORERS = DEFAULT_AVAX_EXPLORER_PROVIDERS.copy()

    def _get_default_provider(self):
        return select_random_free_provider(self.network, FREE_AVAX_PROVIDERS)

    def _remake_provider(self, provider: BaseProvider):
        super()._remake_provider(provider)
        self.web3.middleware_onion.inject(geth_poa_middleware, layer=0)

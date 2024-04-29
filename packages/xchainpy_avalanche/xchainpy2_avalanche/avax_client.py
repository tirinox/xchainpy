from typing import Optional, Union

from web3.middleware import geth_poa_middleware
from web3.providers import BaseProvider

from xchainpy2_client import FeeBounds, RootDerivationPaths
from xchainpy2_ethereum import EthereumClient
from xchainpy2_ethereum.utils import select_random_free_provider
from xchainpy2_utils import NetworkType, Chain, AssetAVAX
from .const import DEFAULT_AVAX_EXPLORER_PROVIDERS, AVAX_DECIMALS, AVAX_CHAIN_ID, FREE_AVAX_PROVIDERS


class AvalancheClient(EthereumClient):
    def __init__(self,
                 network=NetworkType.MAINNET,
                 phrase: Optional[str] = None,
                 private_key: Union[str, bytes, callable, None] = None,
                 fee_bound: Optional[FeeBounds] = None,
                 root_derivation_paths: Optional[RootDerivationPaths] = None,
                 explorer_providers=DEFAULT_AVAX_EXPLORER_PROVIDERS.copy(),
                 wallet_index=0,
                 provider: Optional[BaseProvider] = None):
        super().__init__(network, phrase, private_key, fee_bound, root_derivation_paths, explorer_providers,
                         wallet_index, provider)
        self.chain = Chain.Avalanche
        self._gas_asset = AssetAVAX
        self._decimal = AVAX_DECIMALS
        self._chain_ids = AVAX_CHAIN_ID

    def _get_default_provider(self):
        return select_random_free_provider(self.network, FREE_AVAX_PROVIDERS)

    def _remake_provider(self, provider: BaseProvider):
        super()._remake_provider(provider)
        self.web3.middleware_onion.inject(geth_poa_middleware, layer=0)

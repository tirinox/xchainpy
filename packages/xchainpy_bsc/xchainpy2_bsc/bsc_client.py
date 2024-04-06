from typing import Optional, Union

from web3.providers import BaseProvider

from xchainpy2_bsc.const import FREE_BSC_PROVIDERS, BSC_CHAIN_ID, DEFAULT_BSC_EXPLORER_PROVIDERS
from xchainpy2_client import FeeBounds, RootDerivationPaths
from xchainpy2_ethereum import EthereumClient
from xchainpy2_ethereum.utils import select_random_free_provider
from xchainpy2_utils import NetworkType, Chain, AssetBSC, BSC_DECIMALS


class BinanceSmartChainClient(EthereumClient):
    def __init__(self,
                 network=NetworkType.MAINNET,
                 phrase: Optional[str] = None,
                 private_key: Union[str, bytes, callable, None] = None,
                 fee_bound: Optional[FeeBounds] = None,
                 root_derivation_paths: Optional[RootDerivationPaths] = None,
                 explorer_providers=DEFAULT_BSC_EXPLORER_PROVIDERS.copy(),
                 wallet_index=0,
                 provider: Optional[BaseProvider] = None):
        super().__init__(network, phrase, private_key, fee_bound, root_derivation_paths, explorer_providers,
                         wallet_index, provider)
        self.chain = Chain.BinanceSmartChain
        self._gas_asset = AssetBSC
        self._decimal = BSC_DECIMALS
        self._chain_ids = BSC_CHAIN_ID

    def _get_default_provider(self):
        return select_random_free_provider(self.network, FREE_BSC_PROVIDERS)

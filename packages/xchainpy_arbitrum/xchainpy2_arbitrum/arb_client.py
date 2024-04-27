from typing import Optional, Union

from web3.providers import BaseProvider

from xchainpy2_arbitrum import ARB_DECIMALS, ARB_CHAIN_ID, DEFAULT_ARB_EXPLORER_PROVIDERS, ARB_SURE_FEE, ARB_NORMAL_FEE, \
    FREE_ARB_PROVIDERS
from xchainpy2_client import FeeBounds, RootDerivationPaths, FeeOption
from xchainpy2_ethereum import EthereumClient, GasOptions
from xchainpy2_ethereum.utils import select_random_free_provider
from xchainpy2_utils import NetworkType, Chain
from .consts import AssetAETH


class ArbitrumChainClient(EthereumClient):
    def __init__(self,
                 network=NetworkType.MAINNET,
                 phrase: Optional[str] = None,
                 private_key: Union[str, bytes, callable, None] = None,
                 fee_bound: Optional[FeeBounds] = None,
                 root_derivation_paths: Optional[RootDerivationPaths] = None,
                 explorer_providers=DEFAULT_ARB_EXPLORER_PROVIDERS.copy(),
                 wallet_index=0,
                 provider: Optional[BaseProvider] = None):
        super().__init__(network, phrase, private_key, fee_bound, root_derivation_paths, explorer_providers,
                         wallet_index, provider)
        self.chain = Chain.BinanceSmartChain
        self._gas_asset = AssetAETH
        self._decimal = ARB_DECIMALS
        self._chain_ids = ARB_CHAIN_ID

    def _get_default_provider(self):
        return select_random_free_provider(self.network, FREE_ARB_PROVIDERS)

    async def _deduct_gas(self, fee_option: FeeOption, gas_limit=23000) -> GasOptions:
        # todo: make sure
        if fee_option == FeeOption.FASTEST:
            return GasOptions.legacy(ARB_SURE_FEE, gas_limit)
        else:
            return GasOptions.legacy(ARB_NORMAL_FEE, gas_limit)

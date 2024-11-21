from xchainpy2_arbitrum import ARB_DECIMALS, ARB_CHAIN_ID, DEFAULT_ARB_EXPLORER_PROVIDERS, ARB_SURE_FEE, ARB_NORMAL_FEE, \
    FREE_ARB_PROVIDERS
from xchainpy2_client import FeeOption
from xchainpy2_ethereum import EthereumClient, GasOptions
from xchainpy2_ethereum.utils import select_random_free_provider
from xchainpy2_utils import Chain
from .consts import AssetAETH, ARB_TOKEN_LIST


class ArbitrumClient(EthereumClient):
    _CHAIN = Chain.Arbitrum
    _TOKEN_LIST = ARB_TOKEN_LIST
    _GAS_ASSET = AssetAETH
    _DECIMAL = ARB_DECIMALS
    _CHAIN_ID_DICT = ARB_CHAIN_ID
    _EXPLORERS = DEFAULT_ARB_EXPLORER_PROVIDERS.copy()

    def _get_default_provider(self):
        return select_random_free_provider(self.network, FREE_ARB_PROVIDERS)

    async def _deduct_gas(self, fee_option: FeeOption, gas_limit=23000) -> GasOptions:
        # todo: make sure
        if fee_option == FeeOption.FASTEST:
            return GasOptions.legacy(ARB_SURE_FEE, gas_limit)
        else:
            return GasOptions.legacy(ARB_NORMAL_FEE, gas_limit)

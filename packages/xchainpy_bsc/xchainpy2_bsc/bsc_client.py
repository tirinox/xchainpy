from web3.middleware import geth_poa_middleware
from web3.providers import BaseProvider

from xchainpy2_bsc.const import FREE_BSC_PROVIDERS, BSC_CHAIN_ID, DEFAULT_BSC_EXPLORER_PROVIDERS, BSC_NORMAL_FEE, \
    BSC_SURE_FEE, BSC_TOKEN_LIST
from xchainpy2_client import FeeOption
from xchainpy2_ethereum import EthereumClient, GasOptions
from xchainpy2_ethereum.utils import select_random_free_provider
from xchainpy2_utils import Chain, AssetBSC, BSC_DECIMALS


class BinanceSmartChainClient(EthereumClient):
    _CHAIN = Chain.BinanceSmartChain
    _TOKEN_LIST = BSC_TOKEN_LIST
    _GAS_ASSET = AssetBSC
    _DECIMAL = BSC_DECIMALS
    _CHAIN_ID_DICT = BSC_CHAIN_ID
    _EXPLORERS = DEFAULT_BSC_EXPLORER_PROVIDERS.copy()

    def _get_default_provider(self):
        return select_random_free_provider(self.network, FREE_BSC_PROVIDERS)

    async def _deduct_gas(self, fee_option: FeeOption, gas_limit=23000) -> GasOptions:
        # last_fee = await self.get_last_fee()
        if fee_option == FeeOption.FASTEST:
            return GasOptions.eip1559_in_gwei(BSC_SURE_FEE, 1, gas_limit)
        else:
            return GasOptions.eip1559_in_gwei(BSC_NORMAL_FEE, 1, gas_limit)

    def _remake_provider(self, provider: BaseProvider):
        super()._remake_provider(provider)
        self.web3.middleware_onion.inject(geth_poa_middleware, layer=0)

from xchainpy2_client import XChainClient, FeeOption
from xchainpy2_thorchain_query import THORChainCache
from xchainpy2_utils import CryptoAmount


class EVMHelper:
    def __init__(self, evm_client: XChainClient, tc_cache: THORChainCache):
        self.evm_clinet = evm_client
        self.tc_cache = tc_cache

    async def deposit(self, amount: CryptoAmount, fee_option: FeeOption, to_address: str) -> str:
        """
        Send deposit to THORChain router
        :param amount: amount and asset you want to deposit
        :param fee_option: fee option
        :param to_address:
        :return: str (submitted transaction hash)
        """
        return ''

    async def is_tc_router_approved_to_spend(self, amount: CryptoAmount) -> bool:
        return False

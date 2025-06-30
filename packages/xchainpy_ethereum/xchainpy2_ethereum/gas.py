import asyncio
from functools import reduce
from operator import itemgetter
from typing import Optional, NamedTuple, Dict

import web3

from xchainpy2_client import FeeOption, FeeProgressive
from xchainpy2_utils import Chain, CryptoAmount


class GasOptions(NamedTuple):
    """
    Gas options for transaction invocation
    """
    fee_option: Optional[FeeOption] = None
    gas_price: Optional[int] = None  # legacy, in Wei
    max_fee_per_gas: Optional[int] = None  # EIP-1559, in Wei
    max_priority_fee_per_gas: Optional[int] = None  # EIP-1559, in Wei
    gas_limit: Optional[int] = None  # in Wei

    @classmethod
    def auto(cls, fee_option: FeeOption):
        return cls(fee_option=fee_option)

    @classmethod
    def average(cls):
        return cls.auto(FeeOption.AVERAGE)

    @classmethod
    def fast(cls):
        return cls.auto(FeeOption.FAST)

    @classmethod
    def fastest(cls):
        return cls.auto(FeeOption.FASTEST)

    @classmethod
    def legacy(cls, gas_price: int, gas_limit: int):
        return cls(gas_price=gas_price, gas_limit=gas_limit)

    @classmethod
    def legacy_in_gwei(cls, gas_price: float, gas_limit: int):
        if gas_price > 2000:
            raise ValueError("gas_price seems to be in Wei, not Gwei")
        return cls(gas_price=int(gas_price * 10 ** 9), gas_limit=gas_limit)

    @classmethod
    def eip1559(cls, max_fee_per_gas: int, max_priority_fee_per_gas: int, gas_limit: int):
        return cls(
            max_fee_per_gas=max_fee_per_gas,
            max_priority_fee_per_gas=max_priority_fee_per_gas,
            gas_limit=gas_limit
        )

    @classmethod
    def eip1559_in_gwei(cls, max_fee_per_gas: float, max_priority_fee_per_gas: float, gas_limit: int):
        if max_fee_per_gas > 2000 or max_priority_fee_per_gas > 2000:
            raise ValueError("max_fee_per_gas or max_priority_fee_per_gas seems to be in Wei, not Gwei")

        return cls(
            max_fee_per_gas=int(max_fee_per_gas * 10 ** 9),
            max_priority_fee_per_gas=int(max_priority_fee_per_gas * 10 ** 9),
            gas_limit=gas_limit
        )

    def validate(self):
        assert self.fee_option or self.gas_price or (self.max_fee_per_gas and self.max_priority_fee_per_gas), \
            "Either fee_option or gas_price or (max_fee_per_gas and max_priority_fee_per_gas) must be set"

    def updates_gas_limit(self, gas_limit: int):
        return GasOptions._replace(self, gas_limit=gas_limit)

    @property
    def is_auto(self):
        return self.fee_option is not None


class GasLimits(NamedTuple):
    approve_gas_limit: int
    transfer_gas_asset_gas_limit: int
    transfer_token_gas_limit: int
    deposit_gas_limit: int
    gas_price: int

    @classmethod
    def default(cls):
        return cls(
            approve_gas_limit=200000,
            transfer_gas_asset_gas_limit=23000,
            transfer_token_gas_limit=170000,
            deposit_gas_limit=180000,
            gas_price=30 * 10 ** 9,
        )


def mean_fee(items):
    return wei_to_gwei(round(reduce(lambda a, v: a + v, items) / len(items)))


def wei_to_gwei(wei):
    return web3.Web3.from_wei(wei, 'gwei')


class FeesEVM(FeeProgressive):
    def __init__(self, chain: Chain, fees: Dict[FeeOption, CryptoAmount],
                 priority_fee: CryptoAmount,
                 base_fee: CryptoAmount):
        """
        FeesEVM implementation for Ethereum-like chains.
        In addition to the standard fees, it includes priority and base block fees.

        :param chain: Chain instance representing the blockchain.
        :type chain: Chain
        :param fees: Fees dictionary mapping FeeOption to CryptoAmount.
        :type fees: Dict[FeeOption, CryptoAmount]
        :param priority_fee: Priority fee for the transaction, typically used in EIP-1559 transactions.
        :type priority_fee: CryptoAmount
        :param base_fee: Base fee for the transaction, typically used in EIP-1559 transactions.
        :type base_fee: CryptoAmount
        """
        super().__init__(chain, fees)
        self.priority_fee = priority_fee
        self.base_fee = base_fee


class GasEstimator:
    def __init__(self, w3: web3.Web3, chain: Chain, percentiles=(20, 50, 80), block_count=10,
                 base_fee_multiplier=1.0):
        """
        :param w3: web3 instance
        :param chain: Chain instance representing the blockchain.
        :param percentiles: A monotonically increasing list of percentile values to sample from each block's
        effective priority fees per gas in ascending order, weighted by gas used.
        :param block_count: The number of blocks to sample for the fee history.
        :param base_fee_multiplier: The multiplier to apply to the base fee to get the max fee.
        Don't worry, the unused gas will be refunded to the user.
        """
        self.web3 = w3
        self.chain = chain
        self.percentiles = percentiles
        self.block_count = block_count
        self.base_fee_multiplier = base_fee_multiplier
        assert len(percentiles) == 3, "Percentiles must have 3 values"
        assert tuple(sorted(percentiles)) == percentiles, "Percentiles must be sorted"

    async def fee_history(self):
        return await self.call_service(self.web3.eth.fee_history, self.block_count, 'pending', list(self.percentiles))

    async def base_fee(self):
        block = await self.call_service(self.web3.eth.get_block, 'pending')
        return block.baseFeePerGas

    async def max_priority_fee_safe_low(self):
        """
        Get the priority fee needed to be included in a block.
        You can consider this value as "safe-low" priority fee
        This value is returned by the RPC node
        """
        return await self.call_service(lambda: self.web3.eth.max_priority_fee)

    @staticmethod
    async def call_service(sync_method, *args):
        return await asyncio.get_event_loop().run_in_executor(None, sync_method, *args)

    async def estimate(self) -> FeesEVM:
        """
        Estimate the gas fees based on the current network conditions.
        This method fetches the fee history, base fee, and max priority fee,
        and calculates the average, fast, and fastest fees based on the reward history.

        :return: FeesEVM object containing the estimated fees
        """

        # RPC calls
        fee_history, base_fee, max_priority_fee_safe_low = await asyncio.gather(
            self.fee_history(),
            self.base_fee(),
            self.max_priority_fee_safe_low()
        )

        reward_history = fee_history['reward']

        # historic mean reward (tips) over sampled blocks for each percentile
        # E.g. for 20% has less amount of tips than this number, and the rest (80%) has more ?
        lo, mi, hi = [
            mean_fee(list(map(itemgetter(i), reward_history))) for i in range(3)
        ]

        base_fee = base_fee * self.base_fee_multiplier
        base_fee_with_margin = wei_to_gwei(base_fee)
        max_priority_fee = wei_to_gwei(max_priority_fee_safe_low)

        return FeesEVM(
            self.chain,
            fees={
                FeeOption.FASTEST: hi + base_fee_with_margin,
                FeeOption.FAST: mi + base_fee_with_margin,
                FeeOption.AVERAGE: lo + base_fee_with_margin
            },
            priority_fee=max_priority_fee,
            base_fee=base_fee_with_margin
        )

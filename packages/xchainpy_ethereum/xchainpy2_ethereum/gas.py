import asyncio
from functools import reduce
from operator import itemgetter
from typing import Optional, NamedTuple, Dict

import web3

from xchainpy2_client import FeeOption, FeeProgressive, IGasExplicitSettings
from xchainpy2_utils import Chain, CryptoAmount, Asset


class EVMGas(IGasExplicitSettings):
    """
    Gas options for transaction invocation in Ethereum-like chains.
    """

    def __init__(self,
                 gas_price: Optional[int] = None,
                 max_fee_per_gas: Optional[int] = None,
                 max_priority_fee_per_gas: Optional[int] = None,
                 gas_limit: Optional[int] = None):
        """
        Initialize EVMGas with the specified parameters.

        :param gas_price: Legacy gas price in Wei. If provided, it indicates a legacy transaction.
        :param max_fee_per_gas: EIP-1559 max fee per gas in Wei.
        :param max_priority_fee_per_gas:  EIP-1559 max priority fee per gas in Wei.
        :param gas_limit: Gas limit for the transaction in Wei.
        """
        super().__init__()
        self.gas_price = gas_price
        self.max_fee_per_gas = max_fee_per_gas
        self.max_priority_fee_per_gas = max_priority_fee_per_gas
        self.gas_limit = gas_limit

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
        """
        max_priority_fee_per_gas is your “tip” (what goes to the miner).
        base_fee_per_gas is the protocol-burned minimum fee for that block.
        max_fee_per_gas is the total ceiling you’re willing to pay per gas; it must cover both the base fee and your tip.

        In other words: maxFeePerGas ≥ baseFeePerGas + maxPriorityFeePerGas

        :param max_fee_per_gas: Maximum fee per gas you are willing to pay for the transaction in Wei.
        :param max_priority_fee_per_gas: Maximum priority fee per gas you are willing to pay for the transaction in Wei.
        :param gas_limit: Gas limit for the transaction in Wei.
        :return: EVMGas instance with EIP-1559 parameters.
        """
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
            gas_limit=gas_limit,
        )


class EVMGasLimits(NamedTuple):
    """
    Sufficient gas limits for various transaction types in Ethereum-like chains.
    """

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


def wei_to_gwei(wei):
    """
    Convert Wei to Gwei.

    :param wei: Amount in Wei to be converted to Gwei.
    :return:
    """
    return web3.Web3.from_wei(wei, 'gwei')


class EVMFees(FeeProgressive):
    def __init__(self, fees: Dict[FeeOption, CryptoAmount],
                 priority_fee: CryptoAmount,
                 base_fee: CryptoAmount):
        """
        Fees implementation for Ethereum-like chains.
        In addition to the standard fees, it includes priority and base block fees.

        :param fees: Fees dictionary mapping FeeOption to CryptoAmount.
        :type fees: Dict[FeeOption, CryptoAmount]
        :param priority_fee: Priority fee for the transaction, typically used in EIP-1559 transactions.
        :type priority_fee: CryptoAmount
        :param base_fee: Base fee for the transaction, typically used in EIP-1559 transactions.
        :type base_fee: CryptoAmount
        """
        super().__init__(fees)
        self.priority_fee = priority_fee
        self.base_fee = base_fee

    def select(self, option: FeeOption, gas_limit: int = 0) -> EVMGas:
        """
        Selects the fee amount based on the provided FeeOption.

        :param option: The FeeOption to select.
        :param gas_limit: Just to pass it through if needed, as EVMGas requires it.
        :return: The corresponding CryptoAmount for the selected fee option.
        """
        total_amt = self.fees[option]
        base_amt = self.base_fee
        max_fee = total_amt.amount.internal_amount
        max_priority_fee = (total_amt - base_amt).amount.internal_amount
        return EVMGas(
            max_fee_per_gas=max_fee,
            max_priority_fee_per_gas=max_priority_fee,
            gas_limit=gas_limit,
        )

    def __repr__(self):
        return (f"EVMFees(fees={self.fees}, "
                f"priority_fee={self.priority_fee}, "
                f"base_fee={self.base_fee})")


class EVMGasPriceEstimator:
    def __init__(self, w3: web3.Web3, chain: Chain,
                 gas_asset: Asset,
                 percentiles=(20, 50, 80), block_count=10,
                 base_fee_multiplier=1.0):
        """
        :param w3: web3 instance
        :param chain: Chain instance representing the blockchain.
        :param gas_asset: Asset instance representing the gas asset (e.g., ETH).
        :param percentiles: A monotonically increasing list of percentile values to sample from each block's
        effective priority fees per gas in ascending order, weighted by gas used.
        :param block_count: The number of blocks to sample for the fee history.
        :param base_fee_multiplier: The multiplier to apply to the base fee to get the max fee.
        Don't worry, the unused gas will be refunded to the user.
        """
        self.web3 = w3
        self.chain = chain
        self.gas_asset = gas_asset
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

    @staticmethod
    def _mean_fee(items):
        return round(reduce(lambda a, v: a + v, items) / len(items))

    def _wei_to_gas_amount(self, wei: int) -> CryptoAmount:
        return CryptoAmount.auto_base(wei, self.gas_asset)

    async def estimate(self) -> EVMFees:
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
            self._mean_fee(list(map(itemgetter(i), reward_history))) for i in range(3)
        ]

        base_fee = base_fee * self.base_fee_multiplier

        return EVMFees(
            fees={
                FeeOption.FASTEST: self._wei_to_gas_amount(hi + base_fee),
                FeeOption.FAST: self._wei_to_gas_amount(mi + base_fee),
                FeeOption.AVERAGE: self._wei_to_gas_amount(lo + base_fee),
            },
            priority_fee=self._wei_to_gas_amount(max_priority_fee_safe_low),
            base_fee=self._wei_to_gas_amount(base_fee),
        )

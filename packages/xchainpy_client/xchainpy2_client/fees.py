import asyncio
from decimal import Decimal
from enum import Enum
from typing import Callable, Dict, Union, NamedTuple

from xchainpy2_thornode import Amount


class FeeOption(Enum):
    AVERAGE = 'average'
    FAST = 'fast'
    FASTEST = 'fastest'

    _ETH_PRIORITY_FEE = 'max'
    _ETH_BASE_FEE = 'base'


FeeRates = Dict[FeeOption, float]


class FeeType(Enum):
    FLAT_FEE = 'base'
    PER_BYTE = 'byte'


Fee = Union[Amount, int, float, Decimal]
FeeRate = float  # satoshi per kilobyte in Bitcoin and other UTXO chains

INF_FEE = 1_000_000_000_000_000_000


class Fees(NamedTuple):
    type: FeeType
    fees: Dict[FeeOption, Fee]  # for EVM chains, the fee is in gwei

    @property
    def average(self):
        return self.fees[FeeOption.AVERAGE]

    @property
    def fast(self):
        return self.fees[FeeOption.FAST]

    @property
    def fastest(self):
        return self.fees[FeeOption.FASTEST]


class FeeBounds(NamedTuple):
    lower: FeeRate  # satoshi per byte
    upper: FeeRate  # satoshi per byte

    def check_fee_bounds(self, fee_rate: FeeRate, per_kb: bool = False):
        """
        Check if the given fee rate is within the bounds
        :param fee_rate: fee rate to check, in satoshi per byte
        :param per_kb: if True, the fee rate is in satoshi per kilobyte. Otherwise, it is in satoshi per byte
        """
        if per_kb:
            fee_rate /= 1000

        if fee_rate < self.lower or fee_rate > self.upper:
            raise ValueError(f"Fee outside of predetermined bounds: {fee_rate}")

    @classmethod
    def infinite(cls):
        return FeeBounds(lower=0, upper=INF_FEE)



def single_fee(fee_type: FeeType, amount: Fee) -> Fees:
    return Fees(
        type=fee_type,
        fees={
            option: amount for option in FeeOption
        }
    )


AVERAGE_FEE_MULTIPLIER = 0.5
FASTEST_FEE_MULTIPLIER = 5


def standard_fee(fee_type: FeeType, amount: Fee) -> Fees:
    fees = single_fee(fee_type, amount)
    fees.fees[FeeOption.AVERAGE] = amount * AVERAGE_FEE_MULTIPLIER
    fees.fees[FeeOption.FASTEST] = amount * FASTEST_FEE_MULTIPLIER
    return fees


def standard_fee_rates(amount: FeeRate) -> FeeRates:
    return {
        FeeOption.AVERAGE: amount * AVERAGE_FEE_MULTIPLIER,
        FeeOption.FAST: amount,
        FeeOption.FASTEST: amount * FASTEST_FEE_MULTIPLIER,
    }


def calc_fees(fee_rates: FeeRates, calc_fee: Callable[..., Fee], *args) -> Fees:
    """
    Apply calc_fee function to fee_rates to get Fees
    :param fee_rates: Fee rates
    :param calc_fee: Function like "def calc_fee(k: FeeOption, v: Amount, *args): ..."
    :param args: Arbitrary arguments for calc_fee (optional)
    :return:
    """
    fees = {
        k: calc_fee(k, v, *args)
        for k, v in fee_rates.items()
    }
    return Fees(
        fees=fees,
        type=FeeType.PER_BYTE
    )


async def calc_fees_async(fee_rates: FeeRates, calc_fee: Callable, *args) -> Fees:
    """
    Apply async calc_fee function to fee_rates to get Fees
    :param fee_rates: Fee rates
    :param calc_fee: Function like "async def calc_fee(k: FeeOption, v: Amount, *args): ..."
    :param args: Arbitrary arguments for calc_fee (optional)
    :return:
    """
    all_fees = await asyncio.gather(
        *[calc_fee(k, v, *args) for k, v in fee_rates.items()]
    )

    fees = {
        k: fee
        for k, fee in zip(fee_rates.keys(), all_fees)
    }

    return Fees(
        fees=fees,
        type=FeeType.PER_BYTE
    )

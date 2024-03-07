import asyncio
from typing import Callable, Awaitable

from .models import FeeType, Fee, Fees, FeeOption, FeeBounds, FeeRate, FeeRates


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

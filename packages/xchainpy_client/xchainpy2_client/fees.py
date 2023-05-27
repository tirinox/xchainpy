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


def standard_fee(fee_type: FeeType, amount: Fee) -> Fees:
    fees = single_fee(fee_type, amount)
    fees.fees[FeeOption.AVERAGE] = amount * 0.5
    fees.fees[FeeOption.FASTEST] = amount * 5
    return fees


def calc_fees(fee_rates: FeeRates, calc_fee: Callable[..., Fee], *args) -> Fees:
    fees = {
        k: calc_fee(k, v, *args)
        for k, v in fee_rates.items()
    }
    return Fees(
        fees=fees,
        type=FeeType.PER_BYTE
    )


async def calc_fees_async(fee_rates: FeeRates, calc_fee: Callable[..., Awaitable[...]], *args) -> Fees:
    all_fees = await asyncio.gather(
        calc_fee(v, *args) for v in fee_rates.values()
    )

    fees = {
        k: fee
        for k, fee in zip(fee_rates.keys(), all_fees)
    }

    return Fees(
        fees=fees,
        type=FeeType.PER_BYTE
    )


def check_fee_bounds(fee_bounds: FeeBounds, fee_rate: FeeRate) -> None:
    if fee_rate < fee_bounds.lower or fee_rate > fee_bounds.upper:
        raise ValueError(f"Fee outside of predetermined bounds: {str(fee_rate)}")

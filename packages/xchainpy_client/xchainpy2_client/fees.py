from enum import Enum
from typing import NamedTuple, Optional

from xchainpy2_utils import Chain


class FeeOption(Enum):
    """
    Enum representing different automatic fee options for transaction invocation.
    """

    AVERAGE = 'average'
    """
    Average fee option, typically used for standard transactions.
    """

    FAST = 'fast'
    """
    Fast fee option, used for transactions that need to be processed quickly.
    """

    FASTEST = 'fastest'
    """
    Fastest fee option, used for transactions that require immediate processing. 
    Are you in an ape mood?
    """


GasUnits = int
"""
Gas units for transaction invocation, typically in base units (e.g., satoshi, wei).
"""

INF_FEE = 10 ** 21
"""
Arbitrary large number for infinite fee bounds (in base units).
"""


class FeeBounds(NamedTuple):
    """
    Fee bounds for transaction invocation specified in base units (e.g., satoshi, wei and so on).
    This is a safety measure to ensure that the fee rate does not exceed predetermined limits.
    """

    lower: GasUnits  # in base units
    """Lower bound for the fee in base units (e.g., satoshi, wei). Typically, this is zero."""

    upper: GasUnits  # in base units
    """Upper bound for the fee in base units (e.g., satoshi, wei). Typically, this is an arbitrary large number."""

    def check_fee_bounds(self, fee_amount: GasUnits):
        """
        Check if the given fee rate is within the bounds
        :param fee_amount: Fee amount in base units (e.g., satoshi, wei).
        """
        if fee_amount < self.lower or fee_amount > self.upper:
            raise ValueError(f"Fee outside of predetermined bounds: {fee_amount}")

    @classmethod
    def infinite(cls):
        """
        Create infinite fee bounds, which means no limits on the fee rate.
        :return:
        """
        return FeeBounds(lower=0, upper=INF_FEE)


class IGasExplicitOptions:
    """
    Chain specific gas options for transaction invocation.
    This is an interface that should be implemented by chain-specific gas options classes.
    See the corresponding client package for specific implementations.
    """

    def __init__(self, chain: Chain):
        self.chain = chain


class IFees:
    """
    Interface for fees.
    This is an interface that should be implemented by chain-specific fees classes.
    See the corresponding client package for specific implementations.
    """

    def __init__(self, chain: Chain):
        self.chain = chain


class Gas(NamedTuple):
    """
    Gas options for transaction invocation. Gas fees can be either automatic or explicitly set.
    In automatic mode, you choose a fee option (average, fast, fastest) and optionally set bounds.
    In explicit mode, you provide specific gas options like gas price or EIP-1559 parameters.
    Explicit options defined in the corresponding client package.
    """

    is_automatic: bool
    """
    Whether the gas options are automatic or explicitly set.
    """

    bounds: Optional[FeeBounds]
    """
    Optional bounds for the fee rate. If not set, defaults to infinite bounds.
    """

    fee_option: FeeOption = FeeOption.FAST
    """
    The fee option to use if the gas options are automatic.
    """

    explicit_options: Optional[IGasExplicitOptions] = None
    """
    Explicit gas options if the gas options are not automatic.
    """

    @classmethod
    def auto(cls, fee_option: FeeOption, bounds: Optional[FeeBounds] = None):
        """
        Create automatic gas options with a specified fee option and optional bounds.

        :param fee_option: Fee option to use (average, fast, fastest).
        :param bounds: Optional bounds for the fee rate. If not set, defaults to infinite bounds.
        :return:
        """
        return cls(is_automatic=True, bounds=bounds or FeeBounds.infinite(), fee_option=fee_option)

    @classmethod
    def explicit(cls, options: IGasExplicitOptions, bounds: Optional[FeeBounds] = None):
        """
        Create explicit gas options with specified options and optional bounds.
        Chain specific options should be provided in the corresponding client package.

        :param options: IGasExplicitOptions instance containing explicit gas options.
        :param bounds: Optional bounds for the fee rate. If not set, defaults to infinite bounds.
        :return:
        """
        return cls(is_automatic=False, bounds=bounds or FeeBounds.infinite(), explicit_options=options)

# def single_fee(fee_type: FeeType, amount: Fee) -> Fees:
#     return Fees(
#         type=fee_type,
#         fees={
#             option: amount for option in FeeOption
#         }
#     )
#
#
# AVERAGE_FEE_MULTIPLIER = 0.5
# FASTEST_FEE_MULTIPLIER = 5
#
#
# def standard_fee(fee_type: FeeType, amount: Fee) -> Fees:
#     fees = single_fee(fee_type, amount)
#     fees.fees[FeeOption.AVERAGE] = amount * AVERAGE_FEE_MULTIPLIER
#     fees.fees[FeeOption.FASTEST] = amount * FASTEST_FEE_MULTIPLIER
#     return fees
#
#
# def standard_fee_rates(amount: FeeRate) -> FeeRates:
#     return {
#         FeeOption.AVERAGE: amount * AVERAGE_FEE_MULTIPLIER,
#         FeeOption.FAST: amount,
#         FeeOption.FASTEST: amount * FASTEST_FEE_MULTIPLIER,
#     }
#
#
# def calc_fees(fee_rates: FeeRates, calc_fee: Callable[..., Fee], *args) -> Fees:
#     """
#     Apply calc_fee function to fee_rates to get Fees
#     :param fee_rates: Fee rates
#     :param calc_fee: Function like "def calc_fee(k: FeeOption, v: Amount, *args): ..."
#     :param args: Arbitrary arguments for calc_fee (optional)
#     :return:
#     """
#     fees = {
#         k: calc_fee(k, v, *args)
#         for k, v in fee_rates.items()
#     }
#     return Fees(
#         fees=fees,
#         type=FeeType.PER_BYTE
#     )
#
#
# async def calc_fees_async(fee_rates: FeeRates, calc_fee: Callable, *args) -> Fees:
#     """
#     Apply async calc_fee function to fee_rates to get Fees
#     :param fee_rates: Fee rates
#     :param calc_fee: Function like "async def calc_fee(k: FeeOption, v: Amount, *args): ..."
#     :param args: Arbitrary arguments for calc_fee (optional)
#     :return:
#     """
#     all_fees = await asyncio.gather(
#         *[calc_fee(k, v, *args) for k, v in fee_rates.items()]
#     )
#
#     fees = {
#         k: fee
#         for k, fee in zip(fee_rates.keys(), all_fees)
#     }
#
#     return Fees(
#         fees=fees,
#         type=FeeType.PER_BYTE
#     )

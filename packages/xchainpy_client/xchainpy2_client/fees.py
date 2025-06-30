from enum import Enum
from typing import NamedTuple, Optional, Dict

from xchainpy2_utils import Chain, CryptoAmount


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
    Instances of subclasses are returned by the `get_fees` method of the client.
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


class FlatFee(IFees):
    """
    Flat fee implementation.
    This class is used to represent a flat fee structure for transactions.
    """

    def __init__(self, chain: Chain, amount: CryptoAmount):
        super().__init__(chain)
        self.amount = amount

    def __repr__(self):
        return f"FlatFee(chain={self.chain}, amount={self.amount})"


class FeeWithOptions(IFees):
    """
    Fee with options implementation.
    This class is used to represent a fee structure with options for different fee types.
    """

    def __init__(self, chain: Chain, fees: Dict[FeeOption, CryptoAmount]):
        super().__init__(chain)
        self.fees = fees

    def __repr__(self):
        return f"FeeWithOptions(chain={self.chain}, fees={self.fees})"

    @property
    def average(self):
        """
        Get the average fee option.

        :return: The average fee option.
        """
        return self.fees.get(FeeOption.AVERAGE)

    @property
    def fast(self):
        """
        Get the fast fee option.

        :return: The fast fee option.
        """
        return self.fees.get(FeeOption.FAST)

    @property
    def fastest(self):
        """
        Get the fastest fee option.

        :return: The fastest fee option.
        """
        return self.fees.get(FeeOption.FASTEST)

    @classmethod
    def from_flat_with_mult(cls, flat_fee: FlatFee, avg_mult=1.0, fast_mult=2.0, fastest_mult=5.0):
        """
        Construct FeeWithOptions from a FlatFee and multipliers for different fee options.

        :param flat_fee: A FlatFee instance containing the base fee amount.
        :param avg_mult: Multiplier for the average fee option (default is 1.0).
        :param fast_mult: Multiplier for the fast fee option (default is 2.0).
        :param fastest_mult: Multiplier for the fastest fee option (default is 5.0).
        :return: FeeWithOptions instance with calculated fees based on the multipliers.
        """
        return cls(
            flat_fee.chain,
            fees={
                FeeOption.AVERAGE: flat_fee.amount * avg_mult,
                FeeOption.FAST: flat_fee.amount * fast_mult,
                FeeOption.FASTEST: flat_fee.amount * fastest_mult,
            }
        )


class FeeProgressive(FeeWithOptions):
    """
    FeeProgressive implementation.
    For some chains, the fee can be progressive, meaning that the fee increases with the size of the transaction.
    """
    def __repr__(self):
        return f"FeeProgressive(chain={self.chain}, fees={self.fees})"

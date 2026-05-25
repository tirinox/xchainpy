from abc import abstractmethod, ABCMeta
from enum import Enum
from typing import NamedTuple, Optional, Dict

from xchainpy2_utils import CryptoAmount


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

PEEK_REASONABLE_FEE_RATE = 10 ** 4
"""
A reasonable fee rate to peek at, used for checking if the fee rate is within bounds.
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


class IGasExplicitSettings(metaclass=ABCMeta):
    """
    Chain specific gas settings for transaction invocation.
    This is an interface that should be implemented by chain-specific gas settings classes.
    See the corresponding client package for specific implementations.
    """

    @property
    @abstractmethod
    def is_valid(self) -> bool:
        """
        Check if the gas settings are valid.
        :return: True if the gas settings are valid, otherwise False.
        """
        pass


class GasFeePerByte(IGasExplicitSettings):
    def __init__(self, satoshi_per_byte: int):
        """
        Gas settings for transaction invocation with a specific fee per byte.

        :param satoshi_per_byte: The fee in satoshi per byte.
        """
        self.satoshi_per_byte = satoshi_per_byte

    @property
    def is_valid(self) -> bool:
        return PEEK_REASONABLE_FEE_RATE > self.satoshi_per_byte > 0


class IFees(metaclass=ABCMeta):
    """
    Interface for fees.
    This is an interface that should be implemented by chain-specific fees classes.
    Instances of subclasses are returned by the `get_fees` method of the client.
    See the corresponding client package for specific implementations.
    """
    pass


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

    settings: Optional[IGasExplicitSettings] = None
    """
    Explicit gas settings if the gas options are not automatic.
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
    def explicit(cls, settings: IGasExplicitSettings, bounds: Optional[FeeBounds] = None):
        """
        Create explicit gas settings and optional bounds.
        Chain specific options should be provided in the corresponding client package.

        :param settings: IGasExplicitSettings instance containing explicit gas settings.
        :param bounds: Optional bounds for the fee rate. If not set, defaults to infinite bounds.
        :return:
        """
        return cls(is_automatic=False, bounds=bounds or FeeBounds.infinite(), settings=settings)

    @property
    def gas_limit(self) -> Optional[int]:
        """
        Get the gas limit from the settings if available.

        :return: The gas limit if available, otherwise None.
        """
        if self.settings and hasattr(self.settings, "gas_limit"):
            return self.settings.gas_limit

    @property
    def has_valid_explicit_settings(self) -> bool:
        """
        Check if the gas options have valid explicit settings.

        :return: True if explicit settings are provided, otherwise False.
        """
        return self.settings is not None and isinstance(self.settings, IGasExplicitSettings) and self.settings.is_valid

    @property
    def is_valid(self) -> bool:
        """
        Check if the gas options are valid.
        If the gas options are automatic, they are valid if no explicit settings are provided.
        If the gas options are explicit, they are valid if the explicit settings are valid.

        :return: bool
        """
        if self.is_automatic:
            return self.settings is None
        else:
            return self.has_valid_explicit_settings

    @classmethod
    def validate(cls, gas: Optional['Gas'] = None, type_of_gas: Optional[type] = None) -> 'Gas':
        """
        Validate the gas options. If gas is None, it will use the default auto settings with FAST fee option.
        If the gas options are not valid, it raises a ValueError.

        :param gas: Optional gas options to validate.
        :param type_of_gas: Optional type of explicit gas to validate against. If provided, it must match the type of gas.
        :return: Gas instance if valid, otherwise raises ValueError.
        """
        if not gas:
            gas = cls.auto(FeeOption.FAST)

        if not gas.is_valid:
            raise ValueError("Gas options are not valid. Please check the gas settings or fee option.")

        if gas.has_valid_explicit_settings and type_of_gas and not isinstance(gas.settings, type_of_gas):
            raise ValueError(
                f"Gas settings must be of type {type_of_gas.__name__}, but got {type(gas.settings).__name__}.")

        return gas


class FlatFee(IFees):
    """
    Flat fee implementation.
    This class is used to represent a flat fee structure for transactions.
    """

    def __init__(self, amount: CryptoAmount):
        super().__init__()
        self.amount = amount

    def __repr__(self):
        return f"FlatFee(amount={self.amount})"

    @property
    def is_valid(self) -> bool:
        return self.amount >= 0


class FeeWithOptions(IFees):
    """
    Fee with options implementation.
    This class is used to represent a fee structure with options for different fee types.
    """

    def __init__(self, fees: Dict[FeeOption, CryptoAmount]):
        self.fees = fees

    def __repr__(self):
        return f"FeeWithOptions(fees={self.fees})"

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
            fees={
                FeeOption.AVERAGE: flat_fee.amount * avg_mult,
                FeeOption.FAST: flat_fee.amount * fast_mult,
                FeeOption.FASTEST: flat_fee.amount * fastest_mult,
            }
        )

    @property
    def is_valid(self) -> bool:
        """
        Check if the fee options are valid.
        A fee option is considered valid if it is not None and greater than or equal to zero.

        :return: True if all fee options are valid, otherwise False.
        """
        # todo write tests for this method
        if not self.fees:
            return False
        if self.average is None or self.fast is None or self.fastest is None:
            return False
        return all(fee >= 0 for fee in self.fees.values() if fee is not None)

    def select(self, option: FeeOption) -> CryptoAmount:
        """
        Select a fee option based on the provided FeeOption enum.

        :param option: The FeeOption to select (average, fast, fastest).
        :return: The selected fee amount or None if the option is not available.
        """
        return self.fees[option]

    def select_as_int(self, option: FeeOption) -> Optional[int]:
        """
        Select a fee option as an integer base amount based on the provided FeeOption enum.

        :param option: The FeeOption to select (average, fast, fastest).
        :return: The selected fee amount as an integer or None if the option is not available.
        """
        return int(self.select(option))


class FeeProgressive(FeeWithOptions):
    """
    FeeProgressive implementation.
    For some chains, the fee can be progressive, meaning that the fee increases with the size of the transaction.
    """

    def __repr__(self):
        return f"FeeProgressive(fees={self.fees})"

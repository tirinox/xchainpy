from decimal import Decimal, Context
from typing import NamedTuple, Union, List

from .asset import Asset
from .decimals import guess_decimals

DECIMAL_CONTEXT = Context(prec=100)
"""
    Default decimal context for all Amount and CryptoAmount operations.
"""

DC = DECIMAL_CONTEXT
"""
    Just a shortcut for the default decimal context.
"""

DEFAULT_ASSET_DECIMAL = 8
"""
    Default number of decimals for asset amounts. Widely used in THORChain, Maya, Cosmos. 
"""

AmountLike = Union['Amount', Decimal, float, int, str]
"""
    Either an Amount instance or a number (int, float, Decimal, str) that can be converted to Amount.
"""

CryptoAmountLike = Union['CryptoAmount', AmountLike]
"""
    Either a CryptoAmount instance or an AmountLike that can be converted to CryptoAmount.
"""


def decimal_power_10(x, context=DC):
    """
    Return 10 ** x as Decimal.

    :param x: number
    :param context: Decimal context
    """
    return Decimal(10, context) ** Decimal(x, context)


class Amount(NamedTuple):
    """
    Represents an amount of an asset with a specific number of decimal places.
    Internal amount is always in base units (no decimal, integer number).
    """

    internal_amount: int
    """The amount in base units (no decimal). Always an integer."""

    decimals: int = DEFAULT_ASSET_DECIMAL
    """The number of decimal places for the amount. Default is 8."""

    @property
    def ten_power(self):
        """
        Return 10 ** decimals as an integer.

        :return: int
        """
        return 10 ** self.decimals

    def _guard_decimals_equal(self, other):
        if isinstance(other, Amount) and other.decimals != self.decimals:
            raise ValueError(f"Decimal contexts do not match {self} != {other}.")

    def __str__(self):
        """
        Return a string representation of the amount.

        :return: A string e.g. "1.34 (D:8)"
        """
        return f"{self.format()} (D:{self.decimals})"

    def __repr__(self):
        """
        Return a string representation of the amount for debugging.

        :return: A string e.g. "Amount(100000000, 8)"
        """
        return f"Amount({int(self.internal_amount)}, {self.decimals})"

    def __add__(self, other: AmountLike) -> 'Amount':
        """
        Perform addition with another Amount or a number.
        If the other is an Amount, it must have the same number of decimals.
        If the other is a number (int, float, Decimal), it is assumed to be in the same decimals as self.

        :param other: Another Amount or a number (int, float, Decimal)
        :return:
        """
        if isinstance(other, (int, float, str, Decimal)):
            return Amount(self.internal_amount + int(Decimal(other) * self.ten_power), self.decimals)
        elif isinstance(other, Amount):
            self._guard_decimals_equal(other)
            return Amount(self.internal_amount + other.internal_amount, self.decimals)
        else:
            raise TypeError(f'Cannot add {self} with {type(other)}')

    def __sub__(self, other: AmountLike):
        """
        Perform subtraction with another Amount or a number.
        If the other is an Amount, it must have the same number of decimals.
        If the other is a number (int, float, Decimal), it is assumed to be in the same decimals as self.

        :param other: Another Amount or a number (int, float, Decimal)
        :return: Amount
        """
        if isinstance(other, (int, float, str, Decimal)):
            return Amount(self.internal_amount - int(Decimal(other) * self.ten_power), self.decimals)
        elif isinstance(other, Amount):
            self._guard_decimals_equal(other)
            return Amount(self.internal_amount - other.internal_amount, self.decimals)
        else:
            raise TypeError(f'Cannot subtract {self} with {type(other)}')

    def __mul__(self, other: AmountLike) -> 'Amount':
        """
        Multiply the amount by another amount or a number.
        If the other is a number (int, float, Decimal), it is assumed to be in the same decimals as self.
        If the other is an Amount, it returns an Amount with the left operand's (self) decimals.

        :param other: Another Amount or a number (int, float, Decimal)
        :return: Amount
        """
        if isinstance(other, (int, float, Decimal)):
            return Amount(int(self.internal_amount * other), self.decimals)
        elif isinstance(other, Amount):
            return Amount.auto(self.as_decimal * other.as_decimal, self.decimals)
        else:
            raise TypeError(f'Cannot multiply {self} with {type(other)}')

    def __truediv__(self, other: AmountLike) -> 'Amount':
        """
        Divide the amount by another amount or a number. True division.
        In case of Amount/Amount division, it returns a dimensionless Amount with thd dividend's decimals.

        :param other: Another Amount or a number (int, float, Decimal)
        :return: Decimal or Amount
        """
        if isinstance(other, (int, float, Decimal)):
            return Amount(int(self.internal_amount / other), self.decimals)
        elif isinstance(other, Amount):
            # Useful for price calculation, returns a dimensionless quantity of type Decimal
            ratio = self.as_decimal / other.as_decimal
            # If the other amount has different decimals, it will return an Amount with the dividend's decimals
            return Amount.auto(ratio, self.decimals)
        else:
            raise TypeError(f'Cannot divide {self} with {type(other)}')

    def __floordiv__(self, other: AmountLike) -> 'Amount':
        """
        Floor divide the amount by another amount or a number.
        In case of Amount // Amount division, returns a dimensionless Amount with the dividend's decimals.

        :param other: Another Amount or a number (int, float, Decimal)
        :return: Amount
        """
        if isinstance(other, (int, float, Decimal)):
            return Amount(int(self.internal_amount // Decimal(other)), self.decimals)
        elif isinstance(other, Amount):
            # Returns a floored ratio with the dividend's decimals
            ratio = self.as_decimal // other.as_decimal
            return Amount.auto(ratio, self.decimals)
        else:
            raise TypeError(f'Cannot floor divide {self} with {type(other)}')

    def __eq__(self, other):
        """
        Check if two Amount instances are equal.
        They must have the same internal amount and the same number of decimals to be considered equal.

        :param other: Another Amount instance or a value that can be converted to Amount
        :return: bool
        """
        if not isinstance(other, Amount):
            return self == self.like_me(other)

        return self.internal_amount == other.internal_amount and self.decimals == other.decimals

    def like_me(self, x):
        """
        Convert x to an Amount instance with the same decimals and decimals as self.

        :param x: Any value suitable for Amount.auto
        :return: Amount
        """
        return self.auto(x, self.decimals)

    def __lt__(self, other: AmountLike):
        """
        Check if this Amount is less than another Amount or a number.
        If the other is an Amount, automatically converts it to the same decimals as self.

        :param other: Amount or a number (int, float, Decimal)
        :return: True if self is less than other, False otherwise.
        """
        return self.internal_amount < self.like_me(other).internal_amount

    def __le__(self, other: AmountLike):
        """
        Check if this Amount is less than or equal to another Amount or a number.
        If the other is an Amount, automatically converts it to the same decimals as self.

        :param other: Amount or a number (int, float, Decimal)
        :return: True if self is less than or equal to other, False otherwise.
        """
        return self.internal_amount <= self.like_me(other).internal_amount

    def __gt__(self, other: AmountLike):
        """
        Check if this Amount is greater than another Amount or a number.
        If the other is an Amount, automatically converts it to the same decimals as self.

        :param other: Amount or a number (int, float, Decimal)
        :return: True if self is greater than other, False otherwise.
        """
        return self.internal_amount > self.like_me(other).internal_amount

    def __ge__(self, other):
        """
        Check if this Amount is greater than or equal to another Amount or a number.
        If the other is an Amount, automatically converts it to the same decimals as self.

        :param other: Amount or a number (int, float, Decimal)
        :return: True if self is greater than or equal to other, False otherwise.
        """
        return self.internal_amount >= self.like_me(other).internal_amount

    @classmethod
    def zero(cls, decimals=DEFAULT_ASSET_DECIMAL):
        """
        Create a zero amount with the specified number of decimals

        :param decimals: Number of decimals (default 8)
        :return: Amount
        """
        return cls(0, decimals)

    def converted_decimals(self, new_decimals, context=DC) -> 'Amount':
        """
        Change the decimals of the amount. Non-destructive. Returns a new instance.

        :param new_decimals: New number of decimals
        :param context: Decimal context (optional)
        :return: Amount
        """
        if new_decimals == self.decimals:
            return self

        a = Decimal(self.internal_amount) * decimal_power_10(new_decimals - self.decimals, context)
        return Amount(int(a), new_decimals)

    @classmethod
    def auto(cls, x, decimals=DEFAULT_ASSET_DECIMAL, context=DC):
        """
        Convert any type to an Amount instance.
        .. warning::  This method uses "asset" amount, e.g. 1 BTC is 1, not 100000000 (satoshi). See also: auto_base.

        :param x: Input value (int, float, str, Decimal, Amount)
        :param decimals: Number of decimals (default 8)
        :param context: Decimal context (optional)
        :return: Amount
        """
        if isinstance(x, Amount):
            if decimals is not None and x.decimals != decimals:
                # If the decimals are different, convert to the new decimals
                return x.converted_decimals(decimals, context)
            return x
        elif isinstance(x, (Decimal, float, str, int)):
            v = int(
                Decimal(x, context) *
                decimal_power_10(decimals, context)
            )
            return cls(v, decimals)
        else:
            raise ValueError(f'Cannot convert {x} to Amount')

    @classmethod
    def auto_base(cls, x, decimals=DEFAULT_ASSET_DECIMAL):
        """
        Convert any type to an Amount instance in base denomination.

        :param x: Input value (int, float, str, Decimal, Amount)
        :param decimals: Number of decimals (default 8)
        :return: Amount
        """
        if isinstance(x, Amount):
            return x
        elif isinstance(x, (float, int, Decimal)):
            return cls(int(x), decimals)
        elif isinstance(x, str):
            return cls(int(Decimal(x)), decimals)
        else:
            raise ValueError(f'Cannot convert {x} to Amount')

    @property
    def integer_part(self):
        """
        Return the integer part of the amount.

        :return: int
        """
        return self.internal_amount // self.ten_power

    @property
    def decimal_part(self):
        """
        Return the decimal part of the amount.

        :return: int
        """
        return self.internal_amount % self.ten_power

    @property
    def decimal_part_str(self):
        """
        Return the decimal part as a string.

        :return: str
        """
        return f'{self.decimal_part:0>{self.decimals}}'

    def format(self, trailing_zeros=False):
        """
        Format the amount as a string.

        :param trailing_zeros: If keeping zeros than it will be like 1.0000, otherwise. e.g. 1
        :return: str
        """
        decimal_part = self.decimal_part_str
        if not trailing_zeros:
            decimal_part = decimal_part.rstrip('0')
        if not decimal_part:
            decimal_part = '0'
        return f'{self.integer_part}.{decimal_part}'

    def __int__(self):
        """
        Extract the integer value of the amount. Same as self.internal_amount.

        :return: int
        """
        return self.internal_amount

    @property
    def as_decimal(self):
        """
        Convert the amount to Decimal with default context DC.

        :return: Decimal
        """
        return self.as_decimal_ctx()

    def as_decimal_ctx(self, context=DC):
        """
        Convert the amount to Decimal with the specified context

        :param context: Decimal context
        :return: Decimal
        """
        return Decimal(self.internal_amount, context) / decimal_power_10(self.decimals, context)

    def __float__(self):
        """
        Convert the amount to float. Returns the asset amount not the base amount.

        :return: float
        """
        return float(self.as_decimal)

    def __bool__(self):
        """
        Check if the amount is non-zero.

        :return: bool
        """
        return bool(self.internal_amount)

    @property
    def is_zero(self):
        """
        Check if the amount is zero.

        :return: bool
        """
        return self.internal_amount == 0

    def __lshift__(self, shifter: int):
        """
        Shift the decimals to the left by the specified number of places.
        If shifter is positive, it will decrease the number of decimals.
        Example: Amount(100000000, 8) << 2 will return Amount(1000000, 6).

        This is useful for converting the amount to a different decimal representation.

        :param shifter: Number of places to shift
        :return: Amount
        """
        if not isinstance(shifter, int):
            raise TypeError(f'Cannot shift {self} with {type(shifter)}')
        return self.converted_decimals(self.decimals - shifter)

    def __rshift__(self, shifter: int):
        """
        Shift the decimals to the right by the specified number of places.
        If shifter is positive, it will increase the number of decimals.
        Example: Amount(1000000, 6) >> 2 will return Amount(100000000, 8).

        This is useful for converting the amount to a different decimal representation.

        :param shifter: Number of places to shift
        :return: Amount
        """
        if not isinstance(shifter, int):
            raise TypeError(f'Cannot shift {self} with {type(shifter)}')
        return self.converted_decimals(self.decimals + shifter)


class CryptoAmount(NamedTuple):
    """
    Represents an amount of a cryptocurrency asset. Basically a combination of an Amount and an Asset.
    """

    amount: Amount
    """The amount of the asset with decimals. Amount Object"""

    asset: Asset
    """The asset itself. Asset Object"""

    @classmethod
    def auto(cls, _amount: AmountLike, asset: Union[Asset, str], decimals=None) -> 'CryptoAmount':
        """˚
        Create a CryptoAmount instance from an amount and an asset.
        The amount can be a number, string, or an Amount instance.
        The amount is treated as an asset amount, e.g. 1 BTC is 1, not 100000000 (satoshi).
        The asset can be an Asset instance or a string.
        The decimals can be specified, otherwise, it will be guessed automatically. But it is recommended to specify it.

        :param _amount: Amount of asset
        :param asset: an asset name or Asset instance
        :param decimals: Decimals for this asset, if None, then it will be guessed automatically
        :return: CryptoAmount
        """
        if decimals is None:
            decimals = guess_decimals(asset)

        return cls(
            Amount.auto(_amount, decimals),
            Asset.auto(asset),
        )

    @classmethod
    def auto_base(cls, _amount: AmountLike, asset: Union[Asset, str], decimals=None) -> 'CryptoAmount':
        """
        Create a CryptoAmount instance from an amount and an asset.
        The amount can be a number, string, or an Amount instance.
        The amount is treated as a base amount, e.g. if you pass 100000000, that will be 1 BTC (in satoshi).
        The asset can be an Asset instance or a string.
        The decimals can be specified, otherwise, it will be guessed automatically. But it is recommended to specify it.

        :param _amount: Amount of asset
        :param asset: an asset name or Asset instance
        :param decimals: Decimals for this asset, if None, then it will be guessed automatically
        :return: CryptoAmount
        """
        if decimals is None:
            decimals = guess_decimals(asset)

        return cls(
            Amount.auto_base(_amount, decimals), Asset.auto(asset),
        )

    def __add__(self, other: CryptoAmountLike) -> 'CryptoAmount':
        """
        Add another CryptoAmount or a number to this CryptoAmount.
        You can only add CryptoAmounts with the same asset.
        If you add a number, it is treated as an "asset" amount in the same decimals as this CryptoAmount.

        :param other: Another CryptoAmount or a number (int, float, Decimal)
        :return: CryptoAmount
        """
        self._guard_asset(other)
        right = other.amount if isinstance(other, CryptoAmount) else other
        return CryptoAmount(self.amount + right, self.asset)

    def __sub__(self, other: CryptoAmountLike) -> 'CryptoAmount':
        """
        Subtract another CryptoAmount or a number from this CryptoAmount.
        You can only subtract CryptoAmounts with the same asset.
        If you subtract a number, it is treated as an "asset" amount in the same decimals as this CryptoAmount.

        :param other: Another CryptoAmount or a number (int, float, Decimal)
        :return: CryptoAmount
        """
        self._guard_asset(other)
        right = other.amount if isinstance(other, CryptoAmount) else other
        return CryptoAmount(self.amount - right, self.asset)

    def __mul__(self, other: Union[int, float, Decimal, str]) -> 'CryptoAmount':
        """
        Multiply this CryptoAmount by a number (int, float, Decimal, or str).
        Strings are converted to Decimal.

        :param other: A number to multiply by (int, float, Decimal, or str)
        :return: CryptoAmount
        """
        if isinstance(other, CryptoAmount):
            raise TypeError("You re trying to multiply two CryptoAmount, can not determine the resulting asset")
        if not isinstance(other, (int, float, Decimal, str)):
            raise TypeError(f'Cannot multiply {self} with {type(other)}')
        return CryptoAmount(self.amount * other, self.asset)

    def __truediv__(self, other: CryptoAmountLike) -> 'CryptoAmount':
        """
        Divide this CryptoAmount by a number (int, float, Decimal, or str).
        See Amount.__truediv__ for more details.
        If other is a CryptoAmount, it returns a dimensionless CryptoAmount with the dividend's decimals.
        Otherwise, it returns a CryptoAmount with the same asset.

        :param other: CryptoAmount or Amount or a number (int, float, Decimal, or str)
        :return: CryptoAmount
        """
        if isinstance(other, CryptoAmount):
            divisor = other.amount
            asset = Asset.dimensionless()
        else:
            divisor = other
            asset = self.asset
        return CryptoAmount(self.amount / divisor, asset)

    def __floordiv__(self, other: CryptoAmountLike) -> 'CryptoAmount':
        """
        Floor divide this CryptoAmount by a number (int, float, Decimal, or str).
        See Amount.__floordiv__ for more details.
        If you divide by another CryptoAmount, it returns a dimensionless CryptoAmount with the dividend's decimals.
        Otherwise, it returns a CryptoAmount with the same asset.

        :param other: CryptoAmount or Amount or a number (int, float, Decimal, or str)
        :return: CryptoAmount
        """
        if isinstance(other, CryptoAmount):
            divisor = other.amount
            asset = Asset.dimensionless()
        else:
            divisor = other
            asset = self.asset
        return CryptoAmount(self.amount // divisor, asset)

    def __eq__(self, other: 'CryptoAmount'):
        """
        Check if two CryptoAmount instances are equal.
        Two CryptoAmounts are considered equal if they have the same asset and the same amount.

        :param other: another CryptoAmount instance
        :return: bool
        """
        return self.asset == other.asset and self.amount == other.amount

    def __lt__(self, other: 'CryptoAmount'):
        """
        Check if this CryptoAmount is less than another CryptoAmount.
        You can only compare CryptoAmounts with the same asset.

        :param other: Another CryptoAmount instance
        :return: bool
        """
        self._guard_asset(other)
        return self.amount < other.amount

    def __le__(self, other: 'CryptoAmount'):
        """
        Check if this CryptoAmount is less than or equal to another CryptoAmount.
        You can only compare CryptoAmounts with the same asset.

        :param other: Another CryptoAmount instance
        :return: bool
        """
        self._guard_asset(other)
        return self.amount <= other.amount

    def __gt__(self, other: 'CryptoAmount'):
        """
        Check if this CryptoAmount is greater than another CryptoAmount.
        You can only compare CryptoAmounts with the same asset.

        :param other: Another CryptoAmount instance
        :return: bool
        """
        self._guard_asset(other)
        return self.amount > other.amount

    def __ge__(self, other: 'CryptoAmount'):
        """
        Check if this CryptoAmount is greater than or equal to another CryptoAmount.
        You can only compare CryptoAmounts with the same asset.

        :param other: Another CryptoAmount instance
        :return: bool
        """
        self._guard_asset(other)
        return self.amount >= other.amount

    def __str__(self):
        """
        Return a string representation of the CryptoAmount.
        Example: "100.5 THOR.RUNE"

        :return: str
        """
        return f'{self.amount.format()} {self.asset}'

    def __repr__(self):
        """
        Return a string representation of the CryptoAmount for debugging.
        Example: CryptoAmount(Amount(100000000, 8), Asset('BTC~BTC'))

        :return: str
        """
        return f'CryptoAmount({self.amount!r}, {self.asset!r})'

    def __int__(self):
        """
        Convert the CryptoAmount to an integer. Returns the amount in base units (no decimal, e.g. sathoshi).

        :return: int
        """
        return int(self.amount)

    def changed_amount(self, new_amount: Union[int, float, Decimal]) -> 'CryptoAmount':
        """
        Change the amount only of this CryptoAmount. The asset remains the same.
        Non-destructive. Returns a new instance.

        :param new_amount: New amount
        :return: CryptoAmount
        """
        a = Amount.auto(new_amount, decimals=self.amount.decimals)
        return CryptoAmount(a, self.asset)

    def changed_amount_base(self, new_amount: int) -> 'CryptoAmount':
        """
        Change the amount only of this CryptoAmount. Sets the base amount (integer)
        The asset remains the same.
        Non-destructive. Returns a new instance.

        :param new_amount: New amount
        :return: CryptoAmount
        """
        return CryptoAmount(Amount(new_amount, self.amount.decimals), self.asset)

    def _guard_asset(self, a: 'CryptoAmount'):
        """
        Check if the asset of the other CryptoAmount is the same as this one.

        :param a: other CryptoAmount
        :raises ValueError: if the assets are different
        :return: None
        """
        if isinstance(a, CryptoAmount):
            if a.asset != self.asset:
                raise ValueError(f"Cannot perform math on 2 different assets: {self.asset} and {a.asset}")

    @classmethod
    def zero(cls, asset: Union[str, Asset], decimals=None):
        """
        Create a zero CryptoAmount with the specified asset and decimals.
        If decimals is None, it will be guessed automatically based on the asset.

        :param asset: Asset instance or asset name
        :param decimals: Decimals for this asset (optional)
        :return: CryptoAmount
        """
        asset = Asset.auto(asset)
        if decimals is None:
            decimals = guess_decimals(asset)
        return cls(Amount.zero(decimals), asset)

    @classmethod
    def zero_from(cls, amount: 'CryptoAmount') -> 'CryptoAmount':
        """
        Create a zero CryptoAmount with the same asset and decimals as the given amount.

        :param amount: Reference amount
        :return: CryptoAmount
        """
        return cls.zero(amount.asset, amount.amount.decimals)

    @classmethod
    def pick(cls, balances: List['CryptoAmount'], asset: Asset) -> 'CryptoAmount':
        """
        Pick an amount from the list of balances. Search by asset.
        If not found, return zero CryptoAmount.

        :param balances: List of CryptoAmount instances
        :param asset: Asset to search for
        :return: CryptoAmount
        """
        for b in balances:
            if b.asset == asset:
                return b
        else:
            return cls.zero(asset)

    def converted_decimals(self, new_decimals, context=DC) -> 'CryptoAmount':
        """
        Change the decimals of the amount. Non-destructive. Returns a new instance.

        :param new_decimals: New number of decimals
        :param context: Decimal context (optional)
        :return: CryptoAmount
        """
        return CryptoAmount(self.amount.converted_decimals(new_decimals, context), self.asset)

    @property
    def decimals(self):
        """
        Return the number of decimals for the amount. Shortcut for self.amount.decimals.

        :return: int
        """
        return self.amount.decimals

    @property
    def base_amount(self):
        """
        Return the amount in base units (no decimal, e.g. satoshi).

        :return: int
        """
        return self.amount.internal_amount

from decimal import Decimal, Context
from enum import Enum
from typing import NamedTuple, Union, List

from .asset import Asset
from .decimals import guess_decimals

DECIMAL_CONTEXT = Context(prec=100)
DC = DECIMAL_CONTEXT


def decimal_power_10(x, context=DC):
    """
    Return 10 ** x as Decimal
    :param x: number
    :param context: Decimal context
    """
    return Decimal(10, context) ** Decimal(x, context)


class Denomination(Enum):
    """
    Enum representing the different denominations for amounts.

    :param BASE: values for asset amounts in base units (no decimal)
    :param ASSET: values of asset amounts (w/ decimal)
    """
    BASE = 'base'
    ASSET = 'asset'


DEFAULT_ASSET_DECIMAL = 8


class Amount(NamedTuple):
    """
    Represents an amount of an asset with a specific denomination and number of decimal places.
    """

    internal_amount: int
    """The amount in base units (no decimal). Always an integer regardless of the denomination."""
    decimals: int = DEFAULT_ASSET_DECIMAL
    """The number of decimal places for the amount. Default is 8."""
    denom: Denomination = Denomination.ASSET
    """The denomination of the amount. Default is Denomination.ASSET."""

    @property
    def ten_power(self):
        """
        Return 10 ** decimals
        :return:
        """
        return 10 ** self.decimals

    @property
    def amount(self) -> Union[int, float]:
        """
        Return the amount as an integer (in base mode) or float (in asset mode)
        :return:
        """
        if self.denom == Denomination.BASE:
            return self.internal_amount
        else:
            return self.internal_amount / self.ten_power

    def __str__(self):
        flag = 'B' if self.denom == self.denom.BASE else 'A'
        return f"{float(self)} {flag}/{self.decimals}"

    def __repr__(self):
        return f"Amount({self!s})"

    def __add__(self, other):
        if self.denom != other.denom:
            raise ValueError(f'Cannot add {self.denom.name} with {other.denom.name}')
        return Amount(self.internal_amount + other.internal_amount, self.decimals, self.denom)

    def __sub__(self, other):
        if self.denom != other.denom:
            raise ValueError(f'Cannot subtract {self.denom.name} with {other.denom.name}')
        return Amount(self.internal_amount - other.internal_amount, self.decimals, self.denom)

    def __mul__(self, other) -> 'Amount':
        if isinstance(other, (int, float, Decimal)):
            return Amount(int(self.internal_amount * other), self.decimals, self.denom)
        else:
            raise TypeError(f'Cannot multiply {self} with {type(other)}')

    def __truediv__(self, other) -> 'Amount':
        if isinstance(other, (int, float, Decimal)):
            return Amount(int(self.internal_amount / other), self.decimals, self.denom)
        else:
            raise TypeError(f'Cannot divide {self} with {type(other)}')

    def __div__(self, other) -> 'Amount':
        if isinstance(other, (int, float, Decimal)):
            return Amount(int(self.internal_amount // other), self.decimals, self.denom)
        else:
            raise TypeError(f'Cannot divide {self} with {type(other)}')

    def __eq__(self, other):
        if not isinstance(other, Amount):
            return self == self.like_me(other)

        return self.internal_amount == other.internal_amount and \
            self.decimals == other.decimals and self.denom == other.denom

    def like_me(self, x):
        """
        Convert x to an Amount instance with the same decimals and denomination as self
        :param x: Any value suitable for Amount.automatic
        :return: Amount
        """
        return self.automatic(x, self.decimals)

    def __lt__(self, other):
        return self.internal_amount < self.like_me(other).internal_amount

    def __le__(self, other):
        return self.internal_amount <= self.like_me(other).internal_amount

    def __gt__(self, other):
        return self.internal_amount > self.like_me(other).internal_amount

    def __ge__(self, other):
        return self.internal_amount >= self.like_me(other).internal_amount

    @classmethod
    def zero(cls, decimals=DEFAULT_ASSET_DECIMAL, denom=Denomination.ASSET):
        """
        Create a zero amount with the specified number of decimals and denomination
        :param decimals: Number of decimals (default 8)
        :param denom: Denomination
        :return: Amount
        """
        return cls(0, decimals, denom)

    @classmethod
    def from_base(cls, base_amount: Union[str, int, Decimal], decimals=DEFAULT_ASSET_DECIMAL):
        """
        Create an amount from a base amount
        :param base_amount: A number in base units (no decimal)
        :param decimals: Number of decimals (default 8)
        :return: Amount
        """
        base_amount = int(base_amount)
        return cls(base_amount, decimals, Denomination.BASE)

    def changed_decimals(self, new_decimals, context=DC) -> 'Amount':
        """
        Change the decimals of the amount. Non-destructive. Returns a new instance.
        :param new_decimals: New number of decimals
        :param context: Decimal context (optional)
        :return: Amount
        """
        if new_decimals == self.decimals:
            return self

        a = Decimal(self.internal_amount) * decimal_power_10(new_decimals - self.decimals, context)
        return Amount(int(a), new_decimals, self.denom)

    @classmethod
    def from_asset(cls, asset_amount: Union[float, str, int, Decimal], decimals=DEFAULT_ASSET_DECIMAL, context=DC):
        """
        Create an amount from an asset amount. Like 1.2345 BTC
        :param asset_amount: A number in asset units (with decimal)
        :param decimals: Number of decimals (default 8)
        :param context: Decimal context (optional)
        :return: Amount
        """
        v = int(
            Decimal(asset_amount, context) *
            decimal_power_10(decimals, context)
        )
        return cls(v, decimals)

    @classmethod
    def automatic(cls, x, decimals=DEFAULT_ASSET_DECIMAL, context=DC):
        """
        Convert any type to an Amount instance
        .. warning::  Integers are considered base amounts, floats are considered asset amounts.
        :param x: Input value (int, float, str, Decimal, Amount)
        :param decimals: Number of decimals (default 8)
        :param context: Decimal context (optional)
        :return: Amount
        """
        if isinstance(x, Amount):
            # return x if x.decimals == decimals else cls(x.internal_amount, decimals, x.denom)
            return x
        elif isinstance(x, int):
            return cls.from_base(x, decimals)
        elif isinstance(x, (float, str)):
            return cls.from_asset(x, decimals)
        elif isinstance(x, Decimal):
            d = x / decimal_power_10(decimals, context)
            return cls(int(d), decimals)
        else:
            raise ValueError(f'Cannot convert {x} to Amount')

    def same_denom(self, other: 'Amount') -> 'Amount':
        """
        Return a new Amount instance (of self) with the same denomination as the other one.
        The "other" argument only provides the denomination, not the value! The value is unchanged compared to self
        :param other: Amount to take denomination from
        :return: Amount
        """
        if self.denom == other.denom:
            return self
        return self.as_base if other.denom == Denomination.BASE else self.as_asset

    @property
    def as_base(self):
        """
        Convert this amount to base denomination. Non-destructive. Returns a new instance.
        :return: Amount
        """
        return self.from_base(self.internal_amount, self.decimals)

    @property
    def as_asset(self):
        """
        Convert this amount to asset denomination. Non-destructive. Returns a new instance.
        :return: Amount
        """
        return Amount(self.internal_amount, self.decimals)

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
        Return the decimal part as a string
        :return: str
        """
        return f'{self.decimal_part:0>{self.decimals}}'

    def format(self, trailing_zeros=False):
        """
        Format the amount as a string
        :param trailing_zeros: If keeping zeros than it will be like 1.0000, otherwise. e.g. 1
        :return: str
        """
        decimal_part = self.decimal_part_str
        if not trailing_zeros:
            decimal_part = decimal_part.rstrip('0')
        return f'{self.integer_part}.{decimal_part}'

    def __int__(self):
        """
        Extract the integer value of the amount. Same as self.internal_amount
        :return:
        """
        return self.internal_amount

    @property
    def as_decimal(self):
        """
        Convert the amount to Decimal with default context DC
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
        Check if the amount is non-zero
        :return: bool
        """
        return bool(self.internal_amount)

    @property
    def is_zero(self):
        """
        Check if the amount is zero
        :return: bool
        """
        return self.internal_amount == 0


class CryptoAmount(NamedTuple):
    """
    Represents an amount of a cryptocurrency asset. Basically a combination of an Amount and an Asset.
    """
    amount: Amount
    """The amount of the asset with decimals. Amount Object"""
    asset: Asset
    """The asset itself. Asset Object"""

    @classmethod
    def automatic(cls, _amount: Union[Amount, str, int, float], asset: Union[Asset, str], decimals=None):
        """
        Create a CryptoAmount instance from an amount and an asset.
        The amount can be a number, string, or an Amount instance. Asset can be an Asset instance or a string.
        The decimals can be specified, otherwise, it will be guessed automatically. But it is recommended to specify it.
        :param _amount: Amount of asset
        :param asset: an asset name or Asset instance
        :param decimals: Decimals for this asset, if None, then it will be guessed automatically
        :return:
        """
        if decimals is None:
            decimals = guess_decimals(asset)

        return cls(
            Amount.automatic(_amount, decimals),
            Asset.automatic(asset),
        )

    def __add__(self, other) -> 'CryptoAmount':
        self.check(other)
        return CryptoAmount(self.amount + other.amount, self.asset)

    def __sub__(self, other) -> 'CryptoAmount':
        self.check(other)
        return CryptoAmount(self.amount - other.amount, self.asset)

    def __mul__(self, other) -> 'CryptoAmount':
        self.check(other)
        multiplier = self._get_multiplier(other)
        return CryptoAmount(self.amount * multiplier, self.asset)

    def __truediv__(self, other) -> 'CryptoAmount':
        self.check(other)
        multiplier = self._get_multiplier(other)
        return CryptoAmount(self.amount / multiplier, self.asset)

    def __div__(self, other) -> 'CryptoAmount':
        self.check(other)
        multiplier = self._get_multiplier(other)
        return CryptoAmount(self.amount // multiplier, self.asset)

    def _get_multiplier(self, other):
        if isinstance(other, (int, float, Decimal)):
            return other
        else:
            raise TypeError(f'Cannot multiply or divide {self} with {type(other)}')

    def __eq__(self, other):
        self.check(other)
        return self.amount == other.amount

    def __lt__(self, other):
        self.check(other)
        return self.amount < other.amount

    def __le__(self, other):
        self.check(other)
        return self.amount <= other.amount

    def __gt__(self, other):
        self.check(other)
        return self.amount > other.amount

    def __ge__(self, other):
        self.check(other)
        return self.amount >= other.amount

    def __str__(self):
        return f'{self.amount} {self.asset}'

    def __repr__(self):
        return f'CryptoAmount({self!s})'

    def __int__(self):
        return int(self.amount)

    def change_amount(self, new_amount: Union[int, float, Decimal]) -> 'CryptoAmount':
        """
        Change the amount only of this CryptoAmount. The asset remains the same.
        Non-destructive. Returns a new instance.
        :param new_amount: New amount
        :return: CryptoAmount
        """
        a = Amount.automatic(new_amount, decimals=self.amount.decimals)
        return CryptoAmount(a.same_denom(self.amount), self.asset)

    def check(self, a: 'CryptoAmount'):
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
    def zero(cls, asset: Union[str, Asset], decimals=DEFAULT_ASSET_DECIMAL):
        """
        Create a zero CryptoAmount with the specified asset and decimals
        :param asset: Asset instance or asset name
        :param decimals: Decimals for this asset
        :return: CryptoAmount
        """
        return cls(Amount.zero(decimals), Asset.automatic(asset))

    @classmethod
    def zero_from(cls, amount: 'CryptoAmount') -> 'CryptoAmount':
        """
        Create a zero CryptoAmount with the same asset and decimals as the given amount
        :param amount: Reference amount
        :return: CryptoAmount
        """
        return cls.zero(amount.asset, amount.amount.decimals)

    @classmethod
    def from_base(cls, amount, asset: Asset = None, decimals=DEFAULT_ASSET_DECIMAL, ) -> 'CryptoAmount':
        """
        Create a CryptoAmount from a base amount
        :param amount: Amount in base units (no decimal)
        :param asset: Asset instance or asset name
        :param decimals: Decimals for this asset
        :return: CryptoAmount
        """
        return CryptoAmount(Amount.from_base(amount, decimals), asset.automatic(asset))

    @property
    def as_asset(self):
        """
        Convert this CryptoAmount to asset denomination. Non-destructive. Returns a new instance.
        :return: CryptoAmount
        """
        return CryptoAmount(self.amount.as_asset, self.asset)

    @property
    def as_base(self):
        """
        Convert this CryptoAmount to base denomination. Non-destructive. Returns a new instance.
        :return:
        """
        return CryptoAmount(self.amount.as_base, self.asset)

    @classmethod
    def pick(cls, balances: List['CryptoAmount'], asset: Asset):
        """
        Pick an amount from the list of balances. Search by asset.
        If not found, return zero.
        """
        for b in balances:
            if b.asset == asset:
                return b.as_asset
        else:
            return cls.zero(asset)

    def changed_decimals(self, new_decimals, context=DC) -> 'CryptoAmount':
        """
        Change the decimals of the amount. Non-destructive. Returns a new instance.
        :param new_decimals: New number of decimals
        :param context: Decimal context (optional)
        :return: CryptoAmount
        """
        return CryptoAmount(self.amount.changed_decimals(new_decimals, context), self.asset)

    @property
    def decimals(self):
        """
        Return the number of decimals for the amount. Instead of calling self.amount.decimals
        :return:
        """
        return self.amount.decimals

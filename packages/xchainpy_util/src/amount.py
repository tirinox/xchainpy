from enum import Enum
from typing import NamedTuple, Union


class Denomination(Enum):
    BASE = 'base'
    ASSET = 'asset'


ASSET_DECIMAL = 8


class Amount(NamedTuple):
    internal_amount: int
    decimal: int
    denom: Denomination = Denomination.ASSET

    @property
    def ten_power(self):
        return 10 ** self.decimal

    @property
    def amount(self) -> Union[int, float]:
        if self.denom == Denomination.BASE:
            return self.internal_amount
        else:
            return self.internal_amount / self.ten_power

    def __str__(self):
        return f'{self.internal_amount} [{self.denom.name}]'

    def __add__(self, other):
        if self.denom != other.denom:
            raise ValueError(f'Cannot add {self.denom.name} with {other.denom.name}')
        return Amount(self.internal_amount + other.internal_amount, self.decimal, self.denom)

    def __sub__(self, other):
        if self.denom != other.denom:
            raise ValueError(f'Cannot subtract {self.denom.name} with {other.denom.name}')
        return Amount(self.internal_amount - other.internal_amount, self.decimal, self.denom)

    def __mul__(self, other):
        if self.denom != Denomination.BASE:
            raise ValueError(f'Cannot multiply {self.denom.name} with {other.denom.name}')
        return Amount(self.internal_amount * other.internal_amount, self.decimal, self.denom)

    def __truediv__(self, other):
        if self.denom != Denomination.BASE:
            raise ValueError(f'Cannot divide {self.denom.name} with {other.denom.name}')
        return Amount(self.internal_amount // other.internal_amount, self.decimal, self.denom)

    def __eq__(self, other):
        return self.internal_amount == other.internal_amount and \
            self.decimal == other.decimal and self.denom == other.denom

    def __lt__(self, other):
        return self.internal_amount < other.internal_amount

    def __le__(self, other):
        return self.internal_amount <= other.internal_amount

    def __gt__(self, other):
        return self.internal_amount > other.internal_amount

    def __ge__(self, other):
        return self.internal_amount >= other.internal_amount

    @classmethod
    def zero(cls, decimals=ASSET_DECIMAL, denom=Denomination.ASSET):
        return cls(0, decimals, denom)

    @classmethod
    def from_base(cls, base_amount: int, decimals=ASSET_DECIMAL):
        return cls(base_amount, decimals, Denomination.BASE)

    @classmethod
    def from_asset(cls, asset_amount: float, decimals=ASSET_DECIMAL):
        return cls(int(asset_amount * 10 ** decimals), decimals)

    @classmethod
    def automatic(cls, x):
        if isinstance(x, Amount):
            return x
        elif isinstance(x, int):
            return cls.from_base(x)
        elif isinstance(x, float):
            return cls.from_asset(x)
        elif isinstance(x, str):
            return cls.from_base(int(x))
        else:
            raise ValueError(f'Cannot convert {x} to Amount')

    @classmethod
    def to_base(cls, a: 'Amount'):
        return cls.from_base(a.internal_amount, a.decimal)

    @classmethod
    def to_asset(cls, a: 'Amount'):
        return cls(a.internal_amount, a.decimal)

    @property
    def integer_part(self):
        return self.internal_amount // self.ten_power

    @property
    def decimal_part(self):
        return self.internal_amount % self.ten_power

    def format(self, trailing_zeros=False):
        if trailing_zeros:
            decimal_part = f'{self.decimal_part:0>{self.decimal}}'
        else:
            decimal_part = f'{self.decimal_part}'.rstrip('0')
        return f'{self.integer_part}.{decimal_part}'


def amount(x) -> Amount:
    return Amount.automatic(x)


def format_big_int(x: int, decimals: int, trailing_zeros=False, prefix='$', postfix='') -> str:
    s = Amount.from_base(x, decimals).format(trailing_zeros)
    return f'{prefix}{s}{postfix}'

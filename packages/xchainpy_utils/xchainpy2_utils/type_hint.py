from decimal import Decimal
from typing import Union

from .amount import Amount
from .asset import Asset

AssetTypes = Union[Asset, str]
AmountInitTypes = Union[int, float, Decimal, str]
AmountTypes = Union[Amount, AmountInitTypes]

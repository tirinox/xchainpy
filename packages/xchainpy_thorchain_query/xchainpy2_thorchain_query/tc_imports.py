"""
This module tries to import some useful constants and types from the THORChain client package if available.
Otherwise, it provides its own definitions to ensure compatibility and functionality.
ToDo: think about more elegant solution, like using a common package for shared types and constants.
"""
import warnings
from decimal import Decimal

from xchainpy2_utils import CryptoAmount, RUNE_DECIMAL, AssetRUNE, Amount, CACAO_DECIMAL, AssetCACAO

try:
    from xchainpy2_thorchain.const import THOR_BLOCK_TIME_SEC, THOR_BLOCK_TIME_SEC, THOR_BASIS_POINT_MAX
    from xchainpy2_thorchain.memo import THORMemo, ActionType
    from xchainpy2_thorchain.const import DEFAULT_RUNE_NETWORK_FEE
except ModuleNotFoundError:
    warnings.warn(f"xchainpy2_thorchain is not installed, using default constants for THORChain.", ImportWarning)

    THOR_BLOCK_TIME_SEC = 6.0
    """Typical time in seconds for a block to be produced in THORChain."""

    DEFAULT_RUNE_NETWORK_FEE = CryptoAmount(Amount.automatic(Decimal("0.02"), RUNE_DECIMAL), AssetRUNE)


    class THORMemo:
        def __new__(cls, *args, **kwargs):
            warnings.warn("THORMemo is not available. Using a placeholder class.", ImportWarning)
            return super().__new__(cls)

        @classmethod
        def __getattribute__(cls, name):
            warnings.warn(f"THORMemo.{name} is not available. Using a placeholder.", ImportWarning)
            return super().__getattribute__(name)

try:
    from xchainpy2_mayachain.const import DEFAULT_CACAO_NETWORK_FEE
except ModuleNotFoundError:
    DEFAULT_CACAO_NETWORK_FEE = CryptoAmount(Amount.automatic(Decimal("0.5"), CACAO_DECIMAL), AssetCACAO)

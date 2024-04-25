from xchainpy2_utils import RUNE_DECIMAL

RUNE_IDEAL_SUPPLY = 500_000_000
RUNE_SUPPLY_AFTER_SWITCH = 486_051_059
THOR_BASIS_POINT_MAX = 10_000
THOR_DIVIDER = float(10 ** RUNE_DECIMAL)
THOR_DIVIDER_INV = 1.0 / THOR_DIVIDER

DEFAULT_EXPIRY = 15 * 60  # 15 minute

DEFAULT_TOLERANCE_BPS = 500  # 0.5%

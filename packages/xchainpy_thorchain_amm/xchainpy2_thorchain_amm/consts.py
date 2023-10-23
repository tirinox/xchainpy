from enum import Enum

from xchainpy2_utils import RUNE_DECIMAL

RUNE_IDEAL_SUPPLY = 500_000_000
RUNE_SUPPLY_AFTER_SWITCH = 486_051_059
THOR_BASIS_POINT_MAX = 10_000
THOR_DIVIDER = float(10 ** RUNE_DECIMAL)
THOR_DIVIDER_INV = 1.0 / THOR_DIVIDER


class ActionType(Enum):
    # Standard
    ADD_LIQUIDITY = 'addLiquidity'
    SWAP = 'swap'
    WITHDRAW = 'withdraw'
    DONATE = 'donate'

    # Name service
    THORNAME = 'thorname'

    # Lending
    LOAN_OPEN = 'loan+'
    LOAN_CLOSE = 'loan-'

    # Node operator/bond provider
    BOND = 'bond'
    UNBOND = 'unbond'
    LEAVE = 'leave'

    # Prospective
    LIMIT_ORDER = 'limit_order'

    # Outbounds
    REFUND = 'refund'
    OUTBOUND = 'out'

    # Special/dev-centric
    RESERVE = 'reserve'
    NOOP = 'noop'

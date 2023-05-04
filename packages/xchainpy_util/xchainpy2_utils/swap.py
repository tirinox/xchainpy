from decimal import Decimal

from xchainpy2_thorchain_query.models import LiquidityPool
from xchainpy2_utils import CryptoAmount


def get_base_amount_with_diff_decimals(amount: CryptoAmount, out_decimals: int) -> Decimal:
    ...


def get_swap_fee(input_amount: CryptoAmount, pool: LiquidityPool, to_rune: bool) -> CryptoAmount:
    ...

from decimal import Decimal

from xchainpy2_utils import CryptoAmount, Amount, AssetRUNE, Asset, DEFAULT_ASSET_DECIMAL
from .models import LiquidityPool, LPAmount, UnitData
from .swap import get_base_amount_with_diff_decimals, get_base_asset_decimals


def get_liquidity_units(liquidity: LPAmount, pool: LiquidityPool) -> int:
    """
    See: https://dev.thorchain.org/thorchain-dev/interface-guide/math#lp-units-add
    :param liquidity: asset amount added
    :param pool: pool depths
    :return: liquidity units - ownership of pool
    """
    base_amount_8_decimals = get_base_amount_with_diff_decimals(liquidity.asset, DEFAULT_ASSET_DECIMAL)
    P = Decimal(pool.pool.liquidity_units)
    r = liquidity.rune.amount.as_decimal
    a = base_amount_8_decimals
    R = pool.rune_balance.as_decimal
    A = pool.asset_balance.as_decimal
    result = P * ((R * a) + (r * A)) / (R * A * 2)
    return result


def get_pool_share(unit_data: UnitData, pool: LiquidityPool,
                   base_asset: Asset = AssetRUNE) -> LPAmount:
    """
    Get pool share of both asset and rune
    formula: (rune * part) / total; (asset * part) / total
    :param base_asset: AssetRUNE or AssetCACAO
    :param unit_data: units for both asset and rune
    :param pool: pool that the asset is bound to
    :return: pool share of both asset and rune in percentage
    """
    units = unit_data.liquidity_units
    total = unit_data.total_units
    R = pool.rune_balance.as_decimal
    T = pool.asset_balance.as_decimal
    asset = T * units / total
    rune = R * units / total
    return LPAmount(
        rune=CryptoAmount(Amount.from_base(rune, get_base_asset_decimals(base_asset)), base_asset),
        asset=CryptoAmount(Amount.from_base(asset, pool.thornode_details.decimals), pool.asset)
    )


def get_slip_on_liquidity(stake: LPAmount, pool: LiquidityPool) -> Decimal:
    """
    Get slip percentage when adding liquidity.
    Formula: (t * R - T * r)/ (T*r + R*T).

    :param stake: the share of asset and rune added to the pool
    :param pool: Pool that the asset is attached to
    :return: returns bignumber representing a slip percentage
    """
    base_amount_8_decimals = get_base_amount_with_diff_decimals(stake.asset, DEFAULT_ASSET_DECIMAL)
    r = stake.rune.amount.as_decimal
    t = base_amount_8_decimals
    R = pool.rune_balance.as_decimal
    T = pool.asset_balance.as_decimal
    numerator = (t * R) - (T * r)
    denominator = (T * r) + (R * T)
    result = numerator / denominator
    return result


def get_pool_ownership(liquidity: LPAmount, pool: LiquidityPool) -> Decimal:
    """
    Calculate liquidity units - % ownership of pool.

    See: https://docs.thorchain.org/thorchain-finance/continuous-liquidity-pools#calculating-pool-ownership
    :param liquidity: asset amount added
    :param pool: pool depths
    :return: liquidity units - % ownership of pool
    """
    P = Decimal(pool.pool.liquidity_units)
    r = liquidity.rune.amount.as_decimal
    a = liquidity.asset.amount.as_decimal
    R = pool.rune_balance.as_decimal + r  # Must add r first
    A = pool.asset_balance.as_decimal + a  # Must add t first
    part1 = R + a
    part2 = r * A
    numerator = P * (part1 + part2)
    denominator = R * A * 2
    lp_units = numerator / denominator
    percent = lp_units / P
    return percent

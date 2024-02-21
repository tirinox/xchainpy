from decimal import Decimal

from xchainpy2_thorchain_query.models import LiquidityPool, LPAmount, UnitData, Block, ILProtectionData, \
    PositionDepositValue
from xchainpy2_utils import CryptoAmount, Amount, AssetRUNE, Asset, calculate_days_from_blocks, DEFAULT_ASSET_DECIMAL
from .swap import get_base_amount_with_diff_decimals, get_decimal


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
        rune=CryptoAmount(Amount.from_base(rune, get_decimal(base_asset)), base_asset),
        asset=CryptoAmount(Amount.from_base(asset, pool.thornode_details.decimals), pool.asset)
    )


def get_slip_on_liquidity(stake: LPAmount, pool: LiquidityPool) -> Decimal:
    """
    Get slip percentage when adding liquidity
    formula: (t * R - T * r)/ (T*r + R*T)
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


def get_liquidity_protection_data(deposit_value: PositionDepositValue,
                                  pool_share:
                                  LPAmount,
                                  block: Block) -> ILProtectionData:
    """
    Get impermanent loss protection data
    Blocks for full protection 1440000 // 100 days
    https://docs.thorchain.org/thorchain-finance/continuous-liquidity-pools#impermanent-loss-protection
    Coverage formula coverage=((A0∗P1)+R0)−((A1∗P1)+R1)=>((A0∗R1/A1)+R0)−(R1+R1)
    protectionProgress = (currentHeight-heightLastAdded)/BlocksForFullProtection
    :param deposit_value: Deposit value
    :param pool_share: the share of asset and rune added to the pool
    :param block: Block object with current, last added and the constant BlocksForFullProtection
    :return:
    """
    R0 = deposit_value.rune.as_decimal  # rune deposit value
    A0 = deposit_value.asset.as_decimal  # asset deposit value
    R1 = pool_share.rune.amount.as_decimal  # rune amount to redeem
    A1 = pool_share.asset.amount.as_decimal  # asset amount to redeem
    P1 = R1 / A1  # Pool ratio at withdrawal
    part1 = A0 * P1 + R0 - (A1 * P1 + R1)  # start position minus end position
    part2 = A0 * (R1 / A1) + R0 - (R1 + R1)  # different way to check position

    coverage = part1 if part1 >= part2 else part2

    height_last_added = block.last_added or 0
    protection_progress = (block.current - height_last_added) / block.full_protection

    total_days_full_protection = calculate_days_from_blocks(block.full_protection)

    return ILProtectionData(
        il_protection=coverage,
        total_days=float(protection_progress * total_days_full_protection),
    )


def get_pool_ownership(liquidity: LPAmount, pool: LiquidityPool) -> Decimal:
    """
    Calculate liquidity units - % ownership of pool
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

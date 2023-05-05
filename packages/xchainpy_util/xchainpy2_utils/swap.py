from decimal import Decimal

from xchainpy2_thorchain_query.models import LiquidityPool, SwapOutput
from xchainpy2_utils import CryptoAmount, AssetRUNE, Asset, Amount, RUNE_DECIMAL, AssetCACAO, \
    CACAO_DECIMAL


def get_base_amount_with_diff_decimals(amount: CryptoAmount, out_decimals: int) -> Decimal:
    new_amount = amount.amount.changed_decimals(out_decimals)
    return new_amount.as_decimal


def get_decimal(base_asset: Asset) -> int:
    if base_asset == AssetRUNE:
        return RUNE_DECIMAL
    elif base_asset == AssetCACAO:
        return CACAO_DECIMAL
    else:
        raise ValueError('Invalid base asset. Must be RUNE or CACAO')


def get_swap_fee(input_amount: CryptoAmount, pool: LiquidityPool, to_rune: bool,
                 rune_units: Asset = AssetRUNE) -> CryptoAmount:
    """
    :param input_amount: amount to swap
    :param pool: Pool Data, RUNE and ASSET Depths
    :param to_rune: Direction of Swap. True if swapping to RUNE/CACAO.
    :param rune_units: AssetRUNE for TC, AssetCacao for Maya
    :return:
    """
    # formula: (x * x * Y) / (x + X) ^ 2
    base_decimals = get_decimal(rune_units)
    decimal_out = pool.thornode_details.decimals
    if decimal_out == -1:
        decimal_out = input_amount.amount.decimals
    x = get_base_amount_with_diff_decimals(input_amount, base_decimals)
    X = pool.asset_balance.as_decimal if to_rune else pool.rune_balance.as_decimal
    Y = pool.rune_balance.as_decimal if not to_rune else pool.asset_balance.as_decimal
    units = rune_units if to_rune else pool.asset
    numerator = x * x * Y
    denominator = (x + X) ** 2
    result = numerator / denominator
    result8 = CryptoAmount(Amount.from_base(result), units)
    decimals = base_decimals if to_rune else decimal_out
    base_out = get_base_amount_with_diff_decimals(result8, decimals)
    swap_fee = CryptoAmount(Amount.automatic(base_out, decimals), units)
    return swap_fee


def get_swap_slip(input_amount: CryptoAmount, pool: LiquidityPool, to_rune: bool,
                  rune_units: Asset = AssetRUNE) -> Decimal:
    """
    Works out the swap slip for a given swap.
    :param input_amount: amount to swap
    :param pool: Pool Data, RUNE and ASSET Depths
    :param to_rune: Direction of Swap. True if swapping to RUNE.
    :param rune_units: AssetRUNE for TC, AssetCacao for Maya
    :return: The amount of slip. Needs to * 100 to get percentage.
    """
    # formula: (x) / (x + X)
    base_decimals = get_decimal(rune_units)
    x = get_base_amount_with_diff_decimals(input_amount, base_decimals)
    X = pool.asset_balance.as_decimal if to_rune else pool.rune_balance.as_decimal
    result = x / (x + X)
    return result


def get_swap_output(input_amount: CryptoAmount, pool: LiquidityPool, to_rune: bool,
                    rune_units: Asset = AssetRUNE) -> CryptoAmount:
    """
    :param input_amount: amount to swap
    :param pool: Pool Data, RUNE and ASSET Depths
    :param to_rune: Direction of Swap. True if swapping to RUNE.
    :param rune_units: AssetRUNE for TC, AssetCacao for Maya
    :return: The output amount
    """
    # formula: (x * X * Y) / (x + X) ^ 2
    base_decimals = get_decimal(rune_units)
    decimal_out = pool.thornode_details.decimals
    if decimal_out == -1:
        decimal_out = input_amount.amount.decimals
    x = get_base_amount_with_diff_decimals(input_amount, base_decimals)
    X = pool.asset_balance.as_decimal if to_rune else pool.rune_balance.as_decimal
    Y = pool.rune_balance.as_decimal if not to_rune else pool.asset_balance.as_decimal
    units = AssetRUNE if to_rune else pool.asset
    numerator = x * X * Y
    denominator = (x + X) ** 2
    result = numerator / denominator
    result8 = CryptoAmount(Amount.from_base(result), units)
    decimals = base_decimals if to_rune else decimal_out
    base_out = get_base_amount_with_diff_decimals(result8, decimals)
    output_amount = CryptoAmount(Amount.automatic(base_out, decimals), units)
    return output_amount


def get_swap_input(input_amount: CryptoAmount,
                   pool1: LiquidityPool,
                   pool2: LiquidityPool,
                   rune_units: Asset = AssetRUNE) -> CryptoAmount:
    # formula: getSwapOutput(pool1) => getSwapOutput(pool2)
    r = get_swap_output(input_amount, pool1, True, rune_units)
    output = get_swap_output(r, pool2, False, rune_units)
    return output


def get_single_swap(input_amount: CryptoAmount, pool: LiquidityPool, to_rune: bool,
                    rune_units: Asset = AssetRUNE) -> SwapOutput:
    """
    :param input_amount: amount to swap
    :param pool: Pool Data, RUNE and ASSET Depths
    :param to_rune: To Rune or not to Rune
    :param rune_units: AssetRUNE for TC, AssetCacao for Maya
    :return: swap output object - output - fee - slip
    """
    output = get_swap_output(input_amount, pool, to_rune, rune_units)
    fee = get_swap_fee(input_amount, pool, to_rune, rune_units)
    slip = get_swap_slip(input_amount, pool, to_rune, rune_units)
    swap_output = SwapOutput(output, fee, slip)
    return swap_output


def get_double_swap_slip(input_amount: CryptoAmount, pool1: LiquidityPool, pool2: LiquidityPool,
                         rune_units: Asset = AssetRUNE) -> Decimal:
    # formula: getSwapSlip1(input1) + getSwapSlip2(getSwapOutput1 => input2)
    swap_output = get_single_swap(input_amount, pool1, True, rune_units)
    swap_output2 = get_single_swap(swap_output.output, pool2, False, rune_units)
    result = swap_output2.slip + swap_output.slip
    return result

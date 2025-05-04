from decimal import Decimal
from typing import Union

from xchainpy2_utils import Asset, AssetRUNE, AssetCACAO, CryptoAmount, Amount, RUNE_DECIMAL, CACAO_DECIMAL
from .models import LiquidityPool, SwapOutput


def get_base_amount_with_diff_decimals(amount: Union[CryptoAmount, Amount], out_decimals: int) -> Decimal:
    """
    Helper function to get convert an amount to a Decimal with different decimal places.

    :param amount: Input amount
    :param out_decimals: Number of decimal places to convert to
    :return: Decimal value
    """
    if isinstance(amount, CryptoAmount):
        amount = amount.amount
    new_amount = amount.changed_decimals(out_decimals)
    return Decimal(new_amount.internal_amount)


def get_base_asset_decimals(base_asset: Asset) -> int:
    """
    Helper function to get the base asset decimals.

    :param base_asset: RUNE or CACAO depending on the protocol used
    :return: int decimal places
    """
    if base_asset == AssetRUNE:
        return RUNE_DECIMAL
    elif base_asset == AssetCACAO:
        return CACAO_DECIMAL
    else:
        raise ValueError('Invalid base asset. Must be RUNE or CACAO')


def get_swap_fee(input_amount: CryptoAmount, pool: LiquidityPool, to_rune: bool,
                 base_asset: Asset = AssetRUNE) -> CryptoAmount:
    """
    Get the swap slip-based fee (slip * output) for a given swap.

    :param input_amount: amount to swap
    :param pool: Pool Data, RUNE and ASSET Depths
    :param to_rune: Direction of Swap. True if swapping to RUNE/CACAO.
    :param base_asset: AssetRUNE for TC, AssetCacao for Maya
    :return:
    """
    # formula: (x * x * Y) / (x + X) ^ 2
    base_decimals = get_base_asset_decimals(base_asset)
    decimal_out = pool.thornode_details.decimals
    if decimal_out == -1:
        decimal_out = input_amount.amount.decimals
    x = get_base_amount_with_diff_decimals(input_amount, base_decimals)
    X = pool.asset_balance.as_decimal if to_rune else pool.rune_balance.as_decimal
    Y = pool.rune_balance.as_decimal if not to_rune else pool.asset_balance.as_decimal
    units = base_asset if to_rune else pool.asset
    numerator = x * x * Y
    denominator = (x + X) ** 2
    result = numerator / denominator
    result8 = CryptoAmount(Amount.from_base(result), units)
    decimals = base_decimals if to_rune else decimal_out
    base_out = get_base_amount_with_diff_decimals(result8, decimals)
    swap_fee = CryptoAmount(Amount.automatic(base_out, decimals), units)
    return swap_fee


def get_swap_slip(input_amount: CryptoAmount, pool: LiquidityPool, to_rune: bool,
                  base_asset: Asset = AssetRUNE) -> Decimal:
    """
    Works out the swap slip for a given swap.

    :param input_amount: amount to swap
    :param pool: Pool Data, RUNE and ASSET Depths
    :param to_rune: Direction of Swap. True if swapping to RUNE.
    :param base_asset: AssetRUNE for TC, AssetCacao for Maya
    :return: The amount of slip. Needs to * 100 to get percentage.
    """
    # formula: (x) / (x + X)
    base_decimals = get_base_asset_decimals(base_asset)
    x = get_base_amount_with_diff_decimals(input_amount, base_decimals)
    X = pool.asset_balance.as_decimal if to_rune else pool.rune_balance.as_decimal
    result = x / (x + X)
    return result


def get_swap_output(input_amount: CryptoAmount, pool: LiquidityPool, to_rune: bool,
                    base_asset: Asset = AssetRUNE) -> CryptoAmount:
    """
    Works out locally the output amount for a given single swap (a single pool engaged).

    :param input_amount: amount to swap
    :param pool: Pool Data, RUNE and ASSET Depths
    :param to_rune: Direction of Swap. True if swapping to RUNE.
    :param base_asset: AssetRUNE for TC, AssetCacao for Maya
    :return: The output amount
    """
    # formula: (x * X * Y) / (x + X) ^ 2
    base_decimals = get_base_asset_decimals(base_asset)
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


def get_single_swap(input_amount: CryptoAmount, pool: LiquidityPool, to_rune: bool,
                    base_asset: Asset = AssetRUNE) -> SwapOutput:
    """
    Calculates the output for a single swap (from Rune to Asset or Asset to Rune).

    :param input_amount: amount to swap
    :param pool: Pool Data, RUNE and ASSET Depths
    :param to_rune: To Rune or not to Rune
    :param base_asset: AssetRUNE for TC, AssetCacao for Maya
    :return: swap output object - output - fee - slip
    """
    output = get_swap_output(input_amount, pool, to_rune, base_asset)
    fee = get_swap_fee(input_amount, pool, to_rune, base_asset)
    slip = get_swap_slip(input_amount, pool, to_rune, base_asset)
    swap_output = SwapOutput(output, fee, slip)
    return swap_output


def get_double_swap_slip(input_amount: CryptoAmount, pool1: LiquidityPool, pool2: LiquidityPool,
                         base_asset: Asset = AssetRUNE) -> Decimal:
    """
    Works out the slippage fee for a double swap (Asset1 of pool1 -> Asset2 of pool2).
    Assets can not be RUNE. For Rune swaps please use get_swap_slip.

    :param input_amount: CryptoAmount to swap from pool1 to pool2
    :param pool1: source LiquidityPool
    :param pool2: target LiquidityPool
    :param base_asset: AssetRUNE for TC, AssetCacao for Maya
    :return:
    """
    # formula: getSwapSlip1(input1) + getSwapSlip2(getSwapOutput1 => input2)
    swap_output = get_single_swap(input_amount, pool1, True, base_asset)
    swap_output2 = get_single_swap(swap_output.output, pool2, False, base_asset)
    result = swap_output2.slip + swap_output.slip
    return result


def get_double_swap_output(input_amount: CryptoAmount, pool1: LiquidityPool, pool2: LiquidityPool) -> CryptoAmount:
    """
    This function locally estimates the output amount of a double swap.

    :param input_amount: Input amount to swap from pool1 to pool2
    :param pool1: First pool
    :type pool1: LiquidityPool
    :param pool2: Second pool
    :type pool2: LiquidityPool
    :return: CryptoAmount of output
    """

    # formula: getSwapOutput(pool1) => getSwapOutput(pool2)
    r = get_swap_output(input_amount, pool1, True)
    output = get_swap_output(r, pool2, False)
    return output

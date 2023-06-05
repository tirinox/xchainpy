from decimal import Decimal
from typing import Union

from xchainpy2_thorchain_query.const import RUNE_NETWORK_FEE, CACAO_NETWORK_FEE, ETH_DECIMALS, AVAX_DECIMALS
from xchainpy2_thorchain_query.models import LiquidityPool, SwapOutput, InboundDetail
from .amount import CryptoAmount, Amount
from .asset import Asset, AssetRUNE, AssetCACAO, AssetETH, AssetBSC, AssetAVAX, AssetATOM, AssetBCH, AssetBNB, \
    AssetBTC, AssetDOGE, AssetLTC
from .consts import RUNE_DECIMAL, CACAO_DECIMAL, Chain


def get_base_amount_with_diff_decimals(amount: Union[CryptoAmount, Amount], out_decimals: int) -> Decimal:
    if isinstance(amount, CryptoAmount):
        amount = amount.amount
    new_amount = amount.changed_decimals(out_decimals)
    return Decimal(new_amount.internal_amount)


def get_decimal(base_asset: Asset) -> int:
    if base_asset == AssetRUNE:
        return RUNE_DECIMAL
    elif base_asset == AssetCACAO:
        return CACAO_DECIMAL
    else:
        raise ValueError('Invalid base asset. Must be RUNE or CACAO')


def get_swap_fee(input_amount: CryptoAmount, pool: LiquidityPool, to_rune: bool,
                 base_asset: Asset = AssetRUNE) -> CryptoAmount:
    """
    :param input_amount: amount to swap
    :param pool: Pool Data, RUNE and ASSET Depths
    :param to_rune: Direction of Swap. True if swapping to RUNE/CACAO.
    :param base_asset: AssetRUNE for TC, AssetCacao for Maya
    :return:
    """
    # formula: (x * x * Y) / (x + X) ^ 2
    base_decimals = get_decimal(base_asset)
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
    base_decimals = get_decimal(base_asset)
    x = get_base_amount_with_diff_decimals(input_amount, base_decimals)
    X = pool.asset_balance.as_decimal if to_rune else pool.rune_balance.as_decimal
    result = x / (x + X)
    return result


def get_swap_output(input_amount: CryptoAmount, pool: LiquidityPool, to_rune: bool,
                    base_asset: Asset = AssetRUNE) -> CryptoAmount:
    """
    :param input_amount: amount to swap
    :param pool: Pool Data, RUNE and ASSET Depths
    :param to_rune: Direction of Swap. True if swapping to RUNE.
    :param base_asset: AssetRUNE for TC, AssetCacao for Maya
    :return: The output amount
    """
    # formula: (x * X * Y) / (x + X) ^ 2
    base_decimals = get_decimal(base_asset)
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
                   base_asset: Asset = AssetRUNE) -> CryptoAmount:
    # formula: getSwapOutput(pool1) => getSwapOutput(pool2)
    r = get_swap_output(input_amount, pool1, True, base_asset)
    output = get_swap_output(r, pool2, False, base_asset)
    return output


def get_single_swap(input_amount: CryptoAmount, pool: LiquidityPool, to_rune: bool,
                    base_asset: Asset = AssetRUNE) -> SwapOutput:
    """
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
    # formula: getSwapSlip1(input1) + getSwapSlip2(getSwapOutput1 => input2)
    swap_output = get_single_swap(input_amount, pool1, True, base_asset)
    swap_output2 = get_single_swap(swap_output.output, pool2, False, base_asset)
    result = swap_output2.slip + swap_output.slip
    return result


def get_double_swap_output(input_amount: CryptoAmount, pool1: LiquidityPool, pool2: LiquidityPool) -> CryptoAmount:
    # formula: getSwapOutput(pool1) => getSwapOutput(pool2)
    r = get_swap_output(input_amount, pool1, True)
    output = get_swap_output(r, pool2, False)
    return output


def calc_network_fee(asset: Asset, inbound: InboundDetail,
                     base_asset: Asset = AssetRUNE) -> CryptoAmount:
    """
    Works out the required inbound fee based on the chain.
    Call getInboundDetails to get the current gasRate
    https://dev.thorchain.org/thorchain-dev/thorchain-and-fees#fee-calcuation-by-chain
    :param asset: source asset
    :param inbound: inbound detail to get gas rates
    :return: amount of network fee
    """
    if asset.synth:
        if base_asset == AssetRUNE:
            return RUNE_NETWORK_FEE
        elif base_asset == AssetCACAO:
            return CACAO_NETWORK_FEE
        else:
            raise ValueError("Invalid Base Asset, expected RUNE or CACAO")

    if asset.chain == Chain.Bitcoin:
        return CryptoAmount(Amount.from_base(inbound.gas_rate * inbound.outbound_tx_size), AssetBTC)
    elif asset.chain == Chain.BitcoinCash:
        return CryptoAmount(Amount.from_base(inbound.gas_rate * inbound.outbound_tx_size), AssetBCH)
    elif asset.chain == Chain.Litecoin:
        return CryptoAmount(Amount.from_base(inbound.gas_rate * inbound.outbound_tx_size), AssetLTC)
    elif asset.chain == Chain.Doge:
        return CryptoAmount(Amount.from_base(inbound.gas_rate * inbound.outbound_tx_size), AssetDOGE)
    elif asset.chain == Chain.Binance:
        return CryptoAmount(Amount.from_base(inbound.gas_rate), AssetBNB)
    elif asset.chain == Chain.Ethereum:
        gas_rate_in_gwei = Decimal(inbound.gas_rate)
        gas_rate_in_wei = Amount.from_base(gas_rate_in_gwei * Decimal(10 ** 9), ETH_DECIMALS)
        if asset == AssetETH:
            return CryptoAmount(Amount.from_base(gas_rate_in_wei * 21000), AssetETH)
        else:
            return CryptoAmount(Amount.from_base(gas_rate_in_wei * 70000), AssetETH)
    elif asset.chain == Chain.Avax:
        gas_rate_in_gwei = Decimal(inbound.gas_rate)
        gas_rate_in_wei = Amount.from_base(gas_rate_in_gwei * Decimal(10 ** 9), AVAX_DECIMALS)
        if asset == AssetAVAX:
            return CryptoAmount(Amount.from_base(gas_rate_in_wei * 21000), AssetAVAX)
        else:
            return CryptoAmount(Amount.from_base(gas_rate_in_wei * 70000), AssetAVAX)
    elif asset.chain == Chain.Cosmos:
        return CryptoAmount(Amount.from_base(inbound.gas_rate), AssetATOM)
    elif asset.chain == Chain.BinanceSmartChain:
        # fixme: is this true?
        return CryptoAmount(Amount.from_base(inbound.gas_rate), AssetBSC)
    elif asset.chain == Chain.THORChain:
        return RUNE_NETWORK_FEE
    elif asset.chain == Chain.Maya:
        return CACAO_NETWORK_FEE
    else:
        raise ValueError(f"Could not calculate inbound fee for {asset.chain} Chain")


def calc_outbound_fee(asset: Asset, inbound: InboundDetail, base_asset=AssetRUNE) -> CryptoAmount:
    if asset.synth:
        if base_asset == AssetRUNE:
            return RUNE_NETWORK_FEE
        elif base_asset == AssetCACAO:
            return CACAO_NETWORK_FEE
        else:
            raise ValueError("Invalid Base Asset, expected RUNE or CACAO")

    if asset.chain == Chain.Bitcoin:
        return CryptoAmount(Amount.from_base(inbound.outbound_fee), AssetBTC)
    elif asset.chain == Chain.BitcoinCash:
        return CryptoAmount(Amount.from_base(inbound.outbound_fee), AssetBCH)
    elif asset.chain == Chain.Litecoin:
        return CryptoAmount(Amount.from_base(inbound.outbound_fee), AssetLTC)
    elif asset.chain == Chain.Doge:
        return CryptoAmount(Amount.from_base(inbound.outbound_fee), AssetDOGE)
    elif asset.chain == Chain.Binance:
        return CryptoAmount(Amount.from_base(inbound.outbound_fee), AssetBNB)
    elif asset.chain == Chain.Ethereum:
        wei = Decimal(inbound.outbound_fee) * Decimal(10 ** 9)
        return CryptoAmount(Amount.from_base(wei, ETH_DECIMALS), AssetETH)
    elif asset.chain == Chain.Avax:
        wei = Decimal(inbound.outbound_fee) * Decimal(10 ** 9)
        return CryptoAmount(Amount.from_base(wei, ETH_DECIMALS), AssetAVAX)
    elif asset.chain == Chain.Cosmos:
        return CryptoAmount(Amount.from_base(inbound.outbound_fee), AssetATOM)
    elif asset.chain == Chain.BinanceSmartChain:
        return CryptoAmount(Amount.from_base(inbound.outbound_fee), AssetBSC)
    elif asset.chain == Chain.THORChain:
        return RUNE_NETWORK_FEE
    elif asset.chain == Chain.Maya:
        return CACAO_NETWORK_FEE
    else:
        raise ValueError(f"Could not calculate outbound fee for {asset.chain} chain")


def get_chain_gas_asset(chain: Union[Chain, str]) -> Asset:
    if isinstance(chain, str):
        chain = Chain(chain)

    if chain == Chain.Bitcoin:
        return AssetBTC
    elif chain == Chain.BitcoinCash:
        return AssetBCH
    elif chain == Chain.Litecoin:
        return AssetLTC
    elif chain == Chain.Doge:
        return AssetDOGE
    elif chain == Chain.Binance:
        return AssetBNB
    elif chain == Chain.Ethereum:
        return AssetETH
    elif chain == Chain.Avax:
        return AssetAVAX
    elif chain == Chain.Cosmos:
        return AssetATOM
    elif chain == Chain.BinanceSmartChain:
        return AssetBSC
    elif chain == Chain.THORChain:
        return AssetRUNE
    elif chain == Chain.Maya:
        return AssetCACAO
    else:
        raise ValueError(f"Could not get gas asset for {chain} chain")


def is_gas_asset(asset: Asset) -> bool:
    # todo: should we check for synth?
    return get_chain_gas_asset(Chain(asset.chain)) == asset

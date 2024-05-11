from typing import Union

from xchainpy2_utils.asset import Asset, Chain, AssetCACAO

RUNE_DECIMAL = 8
CACAO_DECIMAL = 10
ATOM_DECIMALS = 6

ETH_DECIMALS = 18
AVAX_DECIMALS = 18
BSC_DECIMALS = 18

CUSTOM_DECIMALS = {
    Asset.from_string('ETH.USDC-0XA0B86991C6218B36C1D19D4A2E9EB0CE3606EB48'): 6,
    Asset.from_string('ETH.USDT-0XDAC17F958D2EE523A2206206994597C13D831EC7'): 6,
    Asset.from_string('ETH.UOS-0XD13C7342E1EF687C5AD21B27C2B65D772CAB5C8C'): 4,
    Asset.from_string('AVAX.USDC-0XB97EF9EF8734C71904D8002F8B6BC66DD9C48A6E'): 6,
    Asset.from_string('ETH.GUSD-0X056FD409E1D7A124BD7017459DFEA2F387B6D5CD'): 2,
    Asset.from_string('KUJI.KUJI'): 6,
}


def guess_decimals(a: Union[Asset, str]):
    """
    Guess the number of decimals for an asset.
    Don't blindly trust this function, it may return wrong values for exotic assets.
    You are encouraged to specify the number of decimals explicitly.
    :param a: Asset or asset string
    :return: Number of decimals
    """
    if isinstance(a, str):
        a = Asset.from_string(a)

    chain = Chain(a.chain)

    # may be predefined
    if custom_decimals := CUSTOM_DECIMALS.get(a):
        return custom_decimals

    # deduct from Chain
    if chain == Chain.THORChain:
        return RUNE_DECIMAL
    elif chain == Chain.Maya:
        if a == AssetCACAO:
            return CACAO_DECIMAL
        else:
            return RUNE_DECIMAL
    elif chain == Chain.Cosmos:
        return ATOM_DECIMALS
    elif chain == Chain.Binance:
        return 8
    elif chain.is_utxo:
        return 8
    elif chain.is_evm:
        return 18
    else:
        raise ValueError("Cannot guess asset decimals. Specify it explicitly")

from typing import Union

from xchainpy2_utils.asset import Asset, Chain, AssetCACAO

RUNE_DECIMAL = 8
CACAO_DECIMAL = 10
ATOM_DECIMALS = 6
UTXO_DECIMALS = 8

ETH_DECIMALS = 18
AVAX_DECIMALS = 18
BSC_DECIMALS = 18
RIPPLE_DECIMALS = 6
SOLANA_DECIMALS = 9

CUSTOM_DECIMALS = {
    Asset.from_string('ETH.USDC-0XA0B86991C6218B36C1D19D4A2E9EB0CE3606EB48'): 6,
    Asset.from_string('ETH.USDT-0XDAC17F958D2EE523A2206206994597C13D831EC7'): 6,
    Asset.from_string('ETH.UOS-0XD13C7342E1EF687C5AD21B27C2B65D772CAB5C8C'): 4,
    Asset.from_string('AVAX.USDC-0XB97EF9EF8734C71904D8002F8B6BC66DD9C48A6E'): 6,
    Asset.from_string('AVAX.USDT-0X9702230A8EA53601F5CD2DC00FDBC13D4DF4A8C7'): 6,
    Asset.from_string('ETH.GUSD-0X056FD409E1D7A124BD7017459DFEA2F387B6D5CD'): 2,
    Asset.from_string('BASE.USDC-0X833589FCD6EDB6E08F4C7C32D4F71B54BDA02913'): 6,
    Asset.from_string('BSC.USDC-0X8AC76A51CC950D9822D68B83FE1AD97B32CD580D'): 18,
    Asset.from_string('BSC.USDT-0X55D398326F99059FF775485246999027B3197955'): 18,
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

    try:
        chain = Chain(a.chain)
    except ValueError:
        raise ValueError(f"Unknown chain for asset {a}. Cannot guess decimals.")

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
    elif chain == Chain.Ripple:
        return RIPPLE_DECIMALS
    elif chain == Chain.Solana:
        return SOLANA_DECIMALS
    elif chain.is_utxo:
        return UTXO_DECIMALS
    elif chain.is_evm:
        return ETH_DECIMALS
    else:
        raise ValueError("Cannot guess asset decimals. Specify it explicitly")

from xchainpy2_utils import Asset

MRC20_DECIMALS = 10
"""The number of decimals for MRC20 tokens"""

MRC20_CHAIN = 'MRC20'
"""Special Chain identifier for MRC20 assets on chain"""

MNFT_CHAIN = 'MNFT'
"""Special Chain identifier for MNFT assets on chain"""


def is_mrc20(asset: Asset):
    """
    Check if the asset is a MRC20 asset

    :param asset: Asset
    :return: bool
    """
    return asset.chain == MRC20_CHAIN


def is_mnft(asset: Asset):
    """
    Check if the asset is a MNFT asset

    :param asset: Asset
    :return: bool
    """
    return asset.chain == MNFT_CHAIN


def make_mrc20_asset(symbol):
    """
    Create an Asset object from a MRC20 symbol

    :param symbol: Symbol of the asset
    :return: Asset
    """
    return Asset(MRC20_CHAIN, symbol)


def make_mnft_asset(symbol):
    """
    Create an Asset object from a MNFT symbol

    :param symbol: Symbol of the asset
    :return: Asset
    """
    return Asset(MNFT_CHAIN, symbol)


AssetGLD = make_mrc20_asset('GLD')
"""Asset object for GLD"""


class SendsType:
    """
    Enum for the type of MRC20 transactions
    """

    SEND = 'SEND'
    STAKING = 'STAKING'
    MRC20 = 'MRC-20'
    MNFT = 'M-NFT'
    PERPS = 'PERPS'
    ORDERBOOK = 'ORDERBOOK'
    MSG = 'MSG'
    TALK = 'TALK'
    ALL = None

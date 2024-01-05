from xchainpy2_utils import Asset

MRC20_DECIMALS = 10

MRC20_CHAIN = 'MRC20'
MNFT_CHAIN = 'MNFT'


def is_mrc20(asset: Asset):
    return asset.chain == MRC20_CHAIN


def is_mnft(asset: Asset):
    return asset.chain == MNFT_CHAIN


def make_mrc20_asset(symbol):
    return Asset(MRC20_CHAIN, symbol)


def make_mnft_asset(symbol):
    return Asset(MNFT_CHAIN, symbol)


AssetGLD = make_mrc20_asset('GLD')


class SendsType:
    SEND = 'SEND'
    STAKING = 'STAKING'
    MRC20 = 'MRC-20'
    MNFT = 'M-NFT'
    PERPS = 'PERPS'
    ORDERBOOK = 'ORDERBOOK'
    MSG = 'MSG'
    TALK = 'TALK'
    ALL = None

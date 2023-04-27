from enum import Enum
from typing import NamedTuple

from .asset import Asset


class Chain(Enum):
    Binance = "BNB"
    Bitcoin = "BTC"
    Ethereum = "ETH"
    THORChain = "THOR"
    Cosmos = "GAIA"
    BitcoinCash = "BCH"
    Litecoin = "LTC"
    Doge = "DOGE"
    Avax = "AVAX"
    Maya = "MAYA"
    BinanceSmartChain = "BSC"


RUNE_TICKER = 'RUNE'

AssetBTC = Asset('BTC', 'BTC', 'BTC', False)
AssetETH = Asset('ETH', 'ETH', 'ETH', False)
AssetBNB = Asset('BNB', 'BNB', 'BNB', False)
AssetBCH = Asset('BCH', 'BCH', 'BCH', False)
AssetLTC = Asset('LTC', 'LTC', 'LTC', False)
AssetDOGE = Asset('DOGE', 'DOGE', 'DOGE', False)
AssetAVAX = Asset('AVAX', 'AVAX', 'AVAX', False)
AssetRune = Asset('THOR', 'RUNE', 'RUNE', False)
AssetATOM = Asset('GAIA', 'ATOM', 'ATOM', False)
AssetMaya = Asset('MAYA', 'CACAO', 'CACAO', False)

XCHAINPY_IDENTIFIER = 'xchainpy-client'
NINE_REALMS_CLIENT_HEADER = 'x-client-id'

RAIDO_GLYPH = 'ᚱ'
DOLLAR_SIGN = '$'

RUNE_DECIMAL = 8
CACAO_DECIMAL = 10


class ChainAttributes(NamedTuple):
    block_reward: float
    avg_block_time: float

DEFAULT_CHAIN_ATTRS = {
    Chain.BitcoinCash: ChainAttributes(6.25, 600),
    Chain.Bitcoin: ChainAttributes(6.25, 600),
    Chain.Ethereum: ChainAttributes(2, 13),
    Chain.Avax: ChainAttributes(2, 3),
    Chain.Litecoin: ChainAttributes(12.5, 150),
    Chain.Doge: ChainAttributes(10000, 60),
    Chain.Cosmos: ChainAttributes(0, 6),
    Chain.Binance: ChainAttributes(0, 6),
    Chain.THORChain: ChainAttributes(0, 6),
    Chain.BinanceSmartChain: ChainAttributes(0, 3),
    Chain.Maya: ChainAttributes(0, 6),
}

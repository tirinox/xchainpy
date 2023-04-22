from enum import Enum

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

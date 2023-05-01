from enum import Enum
from typing import NamedTuple


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

Address = str


class XChainProtocol(Enum):
    THORCHAIN = 'THORCHAIN'
    MAYA = 'MAYA'

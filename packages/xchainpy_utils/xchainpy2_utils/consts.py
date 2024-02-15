from decimal import Decimal
from enum import Enum

from .amount import CryptoAmount, Amount, DEFAULT_ASSET_DECIMAL
from .asset import *
from .decimals import *

PACKAGE_VERSION = '0.0.11'  # fixme: is there a way to get this automatically?

RAIDO_GLYPH = 'ᚱ'
DOLLAR_SIGN = '$'

RUNE_TICKER = 'RUNE'


class DustAmount(NamedTuple):
    asset: CryptoAmount
    rune: CryptoAmount = CryptoAmount.zero(AssetRUNE)
    cacao: CryptoAmount = CryptoAmount.zero(AssetCACAO)


class ChainAttributes(NamedTuple):
    block_reward: float
    avg_block_time: float
    dust: DustAmount


AMOUNT_10K_SAT = Amount.from_asset(Decimal("0.0001"), DEFAULT_ASSET_DECIMAL)

DEFAULT_CHAIN_ATTRS = {
    Chain.Bitcoin: ChainAttributes(
        6.25, 600,
        DustAmount(AMOUNT_10K_SAT, AssetBTC)
    ),
    Chain.Litecoin: ChainAttributes(
        12.5, 150,
        DustAmount(AMOUNT_10K_SAT, AssetLTC)
    ),
    Chain.BitcoinCash: ChainAttributes(
        6.25, 600,
        DustAmount(AMOUNT_10K_SAT, AssetBCH)
    ),
    Chain.Doge: ChainAttributes(
        10000, 60,
        DustAmount(Amount.from_asset(Decimal("0.01")), AssetDOGE)  # 1 million sat
    ),

    Chain.Ethereum: ChainAttributes(
        2, 13,
        DustAmount(Amount.zero(decimals=ETH_DECIMALS), AssetETH)
    ),
    Chain.Avalanche: ChainAttributes(
        2, 3,
        DustAmount(Amount.zero(decimals=AVAX_DECIMALS), AssetAVAX)
    ),
    Chain.BinanceSmartChain: ChainAttributes(
        0, 3,
        DustAmount(Amount.zero(decimals=BSC_DECIMALS), AssetBSC),
    ),

    Chain.Cosmos: ChainAttributes(
        0, 6,
        DustAmount(Amount.zero(decimals=ATOM_DECIMALS), AssetATOM)
    ),
    Chain.Binance: ChainAttributes(
        0, 6,
        DustAmount(Amount.from_asset(Decimal("0.000001")), AssetBNB)
    ),
    Chain.THORChain: ChainAttributes(
        0, 6,
        DustAmount(Amount.zero(decimals=RUNE_DECIMAL), AssetRUNE)
    ),
    Chain.Maya: ChainAttributes(
        0, 6,
        DustAmount(Amount.zero(decimals=CACAO_DECIMAL), AssetCACAO),
    ),
}

Address = str

MAX_BASIS_POINTS = 10_0000

DAY = 24 * 60 * 60
YEAR = 365 * DAY


def calculate_time_from_blocks(blocks: int, chain: Chain = Chain.THORChain) -> float:
    return blocks * DEFAULT_CHAIN_ATTRS[chain].avg_block_time


def calculate_days_from_blocks(blocks: int, chain: Chain = Chain.THORChain) -> float:
    return calculate_time_from_blocks(blocks, chain) / DAY


class NetworkType(Enum):
    TESTNET = 'testnet'
    STAGENET = 'stagenet'
    MAINNET = 'mainnet'

    DEVNET = 'devnet'


XCHAINJS_IDENTIFIER = 'xchainjs-client'
XCHAINPY_IDENTIFIER = 'xchainpy-client'
NINE_REALMS_CLIENT_HEADER = 'x-client-id'

DEFAULT_USER_AGENT = f'XChainPy2/{PACKAGE_VERSION}/python'

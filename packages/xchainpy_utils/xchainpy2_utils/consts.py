from decimal import Decimal
from enum import Enum
from typing import NamedTuple

from .amount import CryptoAmount, Amount, DEFAULT_ASSET_DECIMAL
from .asset import AssetBNB, AssetBTC, AssetLTC, AssetBCH, AssetETH, AssetRUNE, AssetATOM, AssetDOGE, AssetAVAX, \
    AssetBSC, AssetCACAO

PACKAGE_VERSION = '0.0.6'


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
    Dash = "DASH"
    Kujira = "KUJI"

    UNKNOWN = 'Unknown'

    @property
    def is_utxo(self):
        return self in UTXO_CHAINS

    @property
    def is_evm(self):
        return self in EVM_CHAINS

    @property
    def is_cosmos(self):
        return self in COSMOS_CHAINS


UTXO_CHAINS = {Chain.Bitcoin, Chain.Litecoin, Chain.BitcoinCash, Chain.Doge, Chain.Dash}
EVM_CHAINS = {Chain.Ethereum, Chain.BinanceSmartChain, Chain.Maya, Chain.Avax}
COSMOS_CHAINS = {Chain.Cosmos, Chain.THORChain}

RUNE_TICKER = 'RUNE'

RAIDO_GLYPH = 'ᚱ'
DOLLAR_SIGN = '$'

RUNE_DECIMAL = 8
CACAO_DECIMAL = 10

ETH_DECIMALS = 18
AVAX_DECIMALS = 18
BSC_DECIMALS = 18

ZERO_RUNE = CryptoAmount.zero(AssetRUNE)
ZERO_CACAO = CryptoAmount.zero(AssetCACAO)


class DustAmount(NamedTuple):
    asset: CryptoAmount
    rune: CryptoAmount = ZERO_RUNE
    cacao: CryptoAmount = ZERO_CACAO


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
    Chain.Ethereum: ChainAttributes(
        2, 13,
        DustAmount(Amount.zero(decimals=18), AssetETH)
    ),
    Chain.Avax: ChainAttributes(
        2, 3,
        DustAmount(Amount.zero(decimals=18), AssetAVAX)
    ),
    Chain.Doge: ChainAttributes(
        10000, 60,
        DustAmount(Amount.from_asset(Decimal("0.01"), 8), AssetDOGE)  # 1 million sat
    ),
    Chain.Cosmos: ChainAttributes(
        0, 6,
        DustAmount(Amount.zero(decimals=8), AssetATOM)
    ),
    Chain.Binance: ChainAttributes(
        0, 6,
        DustAmount(Amount.from_asset(Decimal("0.000001")), AssetBNB)
    ),
    Chain.THORChain: ChainAttributes(
        0, 6,
        DustAmount(Amount.zero(decimals=RUNE_DECIMAL), AssetRUNE)
    ),
    Chain.BinanceSmartChain: ChainAttributes(
        0, 3,
        DustAmount(Amount.zero(decimals=8), AssetBSC),
    ),
    Chain.Maya: ChainAttributes(
        0, 6,
        DustAmount(Amount.zero(decimals=8), AssetCACAO),
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

from decimal import Decimal
from enum import Enum

from .amount import CryptoAmount, Amount, DEFAULT_ASSET_DECIMAL
from .asset import *
from .decimals import *
from .versions import PACKAGE_VERSION

"""RAIDO_GLYPH is the unicode character for the Raido rune."""
RAIDO_GLYPH = 'ᚱ'

"""DOLLAR_SIGN is the unicode character for the dollar sign."""
DOLLAR_SIGN = '$'

"""RUNE ticker symbol."""
RUNE_TICKER = 'RUNE'


class DustAmount(NamedTuple):
    """
    DustAmount is used to represent the smallest amount of an asset that can be used by a protocol.
    """

    asset: CryptoAmount
    """The asset that the dust amount represents."""
    rune: CryptoAmount = CryptoAmount.zero(AssetRUNE)
    """The Rune amount that the dust amount represents. It is used in case of THORChain."""
    cacao: CryptoAmount = CryptoAmount.zero(AssetCACAO)
    """The Cacao amount that the dust amount represents. It is used in case of MayaProtocol."""


class ChainAttributes(NamedTuple):
    """
    ChainAttributes is used to represent some attributes of a blockchain.
    """
    block_reward: float
    """The reward for each block in the blockchain."""

    avg_block_time: float
    """The average time in seconds it takes to mine a block in the blockchain."""

    dust: DustAmount
    """Typically, the smallest amount of an asset that can be used by a protocol."""


AMOUNT_10K_SAT = Amount.auto(Decimal("0.0001"), DEFAULT_ASSET_DECIMAL)
"""AMOUNT_10K_SAT is an Amount object that represents 10,000 satoshis."""


def _dust(asset: Asset, amount: Amount) -> DustAmount:
    """Build a DustAmount entry with the chain asset value populated as a CryptoAmount."""
    return DustAmount(CryptoAmount(amount, asset))

"""
DEFAULT_CHAIN_ATTRS is a dictionary that contains the default attributes for each chain supported by THORChain.
"""
DEFAULT_CHAIN_ATTRS = {
    Chain.Bitcoin: ChainAttributes(
        6.25, 600,
        _dust(AssetBTC, AMOUNT_10K_SAT)
    ),
    Chain.Litecoin: ChainAttributes(
        12.5, 150,
        _dust(AssetLTC, AMOUNT_10K_SAT)
    ),
    Chain.BitcoinCash: ChainAttributes(
        6.25, 600,
        _dust(AssetBCH, AMOUNT_10K_SAT)
    ),
    Chain.Doge: ChainAttributes(
        10000, 60,
        _dust(AssetDOGE, Amount.auto(Decimal("0.01")))  # 1 million sat
    ),

    Chain.Ethereum: ChainAttributes(
        2, 13,
        _dust(AssetETH, Amount.zero(decimals=ETH_DECIMALS))
    ),
    Chain.Avalanche: ChainAttributes(
        2, 3,
        _dust(AssetAVAX, Amount.zero(decimals=AVAX_DECIMALS))
    ),
    Chain.BinanceSmartChain: ChainAttributes(
        0, 3,
        _dust(AssetBSC, Amount.zero(decimals=BSC_DECIMALS)),
    ),

    Chain.Cosmos: ChainAttributes(
        0, 6,
        _dust(AssetATOM, Amount.zero(decimals=ATOM_DECIMALS))
    ),
    Chain.THORChain: ChainAttributes(
        0, 6,
        _dust(AssetRUNE, Amount.zero(decimals=RUNE_DECIMAL))
    ),
    Chain.Maya: ChainAttributes(
        0, 6,
        _dust(AssetCACAO, Amount.zero(decimals=CACAO_DECIMAL)),
    ),

    # todo: verify this
    Chain.Solana: ChainAttributes(
        0, 0.4,
        _dust(AssetSOL, Amount.zero(decimals=SOLANA_DECIMALS)),
    ),
    # todo: verify this
    Chain.Ripple: ChainAttributes(
        0, 3.5,
        _dust(AssetXRP, Amount.zero(decimals=RIPPLE_DECIMALS)),
    )
}

Address = str

"""
    MAX_BASIS_POINTS is the maximum number of basis points.
"""
MAX_BASIS_POINTS = 10_0000

"""
    DAY is the number of seconds in a day.
"""
DAY = 24 * 60 * 60

"""
    YEAR is the number of seconds in a year.
"""
YEAR = 365 * DAY


def calculate_time_from_blocks(blocks: int, chain: Chain = Chain.THORChain) -> float:
    """
    Calculate the time in seconds from the given number of blocks for the specified chain.
    :param blocks: The number of blocks
    :param chain: The chain to calculate the time for
    :return: The time in seconds
    """
    return blocks * DEFAULT_CHAIN_ATTRS[chain].avg_block_time


def calculate_days_from_blocks(blocks: int, chain: Chain = Chain.THORChain) -> float:
    """
    Calculate the time in days from the given number of blocks for the specified chain.
    :param blocks: The number of blocks
    :param chain: The chain to calculate the time for
    :return: The time in days float
    """
    return calculate_time_from_blocks(blocks, chain) / DAY


class NetworkType(Enum):
    """
    Enum representing the different networks types supported by THORChain.
    """
    TESTNET = 'testnet'
    """Testnet network type can be used for some Chain clients but not for THORChain. Try STAGENET instead."""

    STAGENET = 'stagenet'
    """
        THORChain has introduced a stagenet with real-value tokens to attract more developers so they can test security 
        features for the platform's new blockchains.
    """

    MAINNET = 'mainnet'
    """
        Mainnet is the production network where real transactions are processed.
    """

    DEVNET = 'devnet'
    """This one is rarely used for some development purposes."""


NINE_REALMS_CLIENT_HEADER = 'x-client-id'
"""Nine Reamls Client Header"""

"""
    XCHAINJS_IDENTIFIER is the identifier for the xchainjs-client. 
    It is used in the *x-client-id* header when connecting to 9R servers.
"""
XCHAINJS_IDENTIFIER = 'xchainjs-client'

"""
    XCHAINPY_IDENTIFIER is the identifier for the xchainpy-client. 
    It is used in the *x-client-id* header when connecting to 9R servers.
"""
XCHAINPY_IDENTIFIER = 'xchainpy-client'

"""
    DEFAULT_USER_AGENT is the default user agent for the xchainpy2-client.
"""
DEFAULT_USER_AGENT = f'XChainPy2/{PACKAGE_VERSION}/python'

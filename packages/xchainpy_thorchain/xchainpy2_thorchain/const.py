from decimal import Decimal

from xchainpy2_client import ExplorerProvider
from xchainpy2_utils import Asset, Amount, CryptoAmount, AssetRUNE
from xchainpy2_utils.consts import NetworkType, RUNE_DECIMAL
from .models import NodeURL

DEFAULT_GAS_LIMIT_VALUE = 6_000_000
"""Default gas limit for transactions. Refers to Cosmos SDK"""

DEPOSIT_GAS_LIMIT_VALUE = 600_000_000
"""Default gas limit for deposit transactions. Refers to Cosmos SDK"""

MAX_TX_COUNT_PER_PAGE = 100
"""Maximum number of transactions per page."""

MAX_TX_COUNT_PER_FUNCTION_CALL = 500
"""Maximum number of transactions per function call."""

MAX_PAGES_PER_FUNCTION_CALL = 15
"""Maximum number of pages per function call."""

RUNE_DISPLAY_SYMBOL = 'ᚱ'
"""Display symbol for the RUNE token. Raido glyph from the Elder Futhark alphabet."""

RUNE_TICKER = 'RUNE'
"""Ticker symbol for the RUNE token."""

DEFAULT_RUNE_FEE = Amount.from_asset(0.02, RUNE_DECIMAL)
"""Default fee for RUNE transactions. Subject to change."""

DEFAULT_EXPLORER_URL = 'https://runescan.io{path}{network_tag}'
"""Default explorer URL for the THORChain network."""

THOR_BASIS_POINT_MAX = 10_000
"""Maximum basis point value for THORChain."""

THOR_AFFILIATE_BASIS_POINT_MAX = 1_000
"""Affiliate cannot receive more than 10% of the trade value."""


def make_explorer_object(network_tag: str):
    """
    Make an explorer object.

    :param network_tag: Query string to append to the base URL
    :return: ExplorerProvider object
    """
    return ExplorerProvider(
        DEFAULT_EXPLORER_URL.format(network_tag=network_tag, path=''),
        DEFAULT_EXPLORER_URL.format(network_tag=network_tag, path='/address/{address}'),
        DEFAULT_EXPLORER_URL.format(network_tag=network_tag, path='/tx/{tx_id}'),
    )


THOR_EXPLORERS = {
    NetworkType.MAINNET: make_explorer_object(''),
    NetworkType.TESTNET: make_explorer_object('?network=testnet'),
    NetworkType.STAGENET: make_explorer_object('?network=stagenet')
}
"""Explorer objects for the THORChain network."""

ROOT_DERIVATION_PATH = "44'/931'/0'/0/"
"""Root derivation path of crypto-keys for THORChain network."""

ROOT_DERIVATION_PATHS = {
    NetworkType.MAINNET: ROOT_DERIVATION_PATH,
    NetworkType.STAGENET: ROOT_DERIVATION_PATH,
    NetworkType.TESTNET: ROOT_DERIVATION_PATH,
}
"""Root derivation paths for the THORChain network."""

DEFAULT_CHAIN_IDS = {
    NetworkType.MAINNET: 'thorchain-1',  # todo: watch out for hard fork
    NetworkType.STAGENET: 'thorchain-stagenet-2',  # todo: watch out for hard fork
    NetworkType.TESTNET: 'deprecated',
}
"""Default chain IDs for the THORChain network. Subject to change."""

THORNODE_PORT = 1317
"""Default API port for THORNode."""

RPC_PORTS = {
    NetworkType.MAINNET: 27147,
    NetworkType.STAGENET: 26657,
    NetworkType.TESTNET: 26657,
}
"""Cosmos SDK RPC ports for the THORChain network."""


def make_client_urls_from_ip_address(ip_address: str, network=NetworkType.MAINNET, protocol='http'):
    """
    Make client URLs dict from an IP address.

    :param ip_address: THORNode IP address
    :param network: Network type
    :param protocol: HTTP or HTTPS
    :return: dict of client URLs
    """
    rpc_port = RPC_PORTS[network]
    return {
        network: NodeURL.from_ip_address(ip_address, THORNODE_PORT, rpc_port, protocol)
    }


DEFAULT_CLIENT_URLS = {
    NetworkType.MAINNET: NodeURL(
        'https://thornode.ninerealms.com',
        'https://rpc.ninerealms.com'
    ),
    NetworkType.STAGENET: NodeURL(
        'https://stagenet-thornode.ninerealms.com',
        'https://stagenet-rpc.ninerealms.com'
    ),
    NetworkType.TESTNET: NodeURL('deprecated', 'deprecated'),
}
"""Default client URLs for the THORChain network."""

FALLBACK_CLIENT_URLS = {
    NetworkType.MAINNET: [
        NodeURL('https://thornode-v1.ninerealms.com', 'https://rpc-v1.ninerealms.com'),
        NodeURL('https://thornode.thorswap.net/', 'https://rpc.thorswap.net'),
        NodeURL('https://thornode-v0.ninerealms.com', 'https://rpc-v0.ninerealms.com'),
    ],
    NetworkType.STAGENET: [DEFAULT_CLIENT_URLS[NetworkType.STAGENET]],
    NetworkType.TESTNET: []
}
"""Fallback client URLs for the THORChain network."""

AssetRuneBNBTestnet = Asset.from_string('BNB.RUNE-67C')
"""BEP2 RUNE asset on Binance testnet. No longer used."""

AssetRuneBNBMainnet = Asset.from_string('BNB.RUNE-B1A')
"""BEP2 RUNE asset on Binance mainnet. No longer used."""

AssetRuneERC20Mainnet = Asset.from_string('ETH.RUNE-0x3155ba85d5f96b2d030a4966af206230e46849cb')
"""ERC20 RUNE asset on Ethereum mainnet. No longer used."""

# Base "chain" asset for RUNE on ethereum test net.
AssetRuneERC20Testnet = Asset.from_string('ETH.RUNE-0xd601c6A3a36721320573885A8d8420746dA3d7A0')
"""ERC20 RUNE asset on Ethereum testnet. No longer used."""

DENOM_RUNE_NATIVE = 'rune'
"""Denomination for RUNE on THORChain (COSMOS demon)."""

THOR_BLOCK_TIME_SEC = 6.0
"""Typical time in seconds for a block to be produced in THORChain."""

DEFAULT_RUNE_NETWORK_FEE = CryptoAmount(Amount.from_asset(Decimal("0.02"), RUNE_DECIMAL), AssetRUNE)
"""
    Default network fee for RUNE transactions. 
    This may be overridden by the network constants. 
    Please check the network constants for the actual network fee.
"""

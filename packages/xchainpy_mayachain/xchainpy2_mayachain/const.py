from decimal import Decimal

from xchainpy2_client import ExplorerProvider
from xchainpy2_utils import Asset, Amount, CryptoAmount, AssetCACAO
from xchainpy2_utils.consts import NetworkType, CACAO_DECIMAL
from .models import NodeURL

DEFAULT_GAS_LIMIT_VALUE = 4_000_000
"""Default gas limit for transactions. Related to Cosmos SDK"""

DEPOSIT_GAS_LIMIT_VALUE = 600_000_000
"""Default gas limit for deposit transactions. Related to Cosmos SDK"""

MAX_TX_COUNT_PER_PAGE = 100
"""Maximum number of transactions per page."""

MAX_TX_COUNT_PER_FUNCTION_CALL = 500
"""Maximum number of transactions per function call."""

MAX_PAGES_PER_FUNCTION_CALL = 15
"""Maximum number of pages per function call."""

CACAO_DISPLAY_SYMBOL = 'C'
"""Display symbol for the Cacao token."""

CACAO_TICKER = 'CACAO'
"""Ticker symbol for the Cacao token."""

DENOM_CACAO_NATIVE = 'cacao'
"""Cosmos denomination for the Cacao token."""

MAYA_DECIMAL = 4
"""Decimal places for the Maya token."""

DENOM_MAYA = 'maya'
"""Cosmos denomination for the Maya token."""

AssetMAYA = Asset.from_string('MAYA.MAYA')
"""Asset object for the Maya token. Maya token collects fees in Cacao for its holders."""

DEFAULT_CACAO_NETWORK_FEE = CryptoAmount(Amount.from_asset(Decimal("0.5"), CACAO_DECIMAL), AssetCACAO)
"""Default Cacao fee for transactions. Subject to change."""


DEFAULT_EXPLORER_URL = 'https://explorer.mayachain.info{path}{network_tag}'
"""Default explorer URL for the Maya network."""

MAYASCAN_EXPLORER_URL = 'https://mayascan.org{path}'
"""Explorer URL for the Maya network by MayaScan."""


def make_explorer_object(network_tag: str, base_url=MAYASCAN_EXPLORER_URL):
    """
    Make an explorer object.

    :param network_tag: Query string to append to the base URL
    :param base_url: Base URL of the explorer
    :return: Explorer object
    """
    return ExplorerProvider(
        base_url.format(network_tag=network_tag, path=''),
        base_url.format(network_tag=network_tag, path='/address/{address}'),
        base_url.format(network_tag=network_tag, path='/tx/{tx_id}'),
    )


DEFAULT_MAYA_EXPLORERS = {
    NetworkType.MAINNET: make_explorer_object(''),
    NetworkType.TESTNET: make_explorer_object('?network=testnet'),
    NetworkType.STAGENET: make_explorer_object('?network=stagenet')
}
"""Explorer URLs for the Maya network."""

MAYASCAN_EXPLORERS = {
    NetworkType.MAINNET: make_explorer_object('', base_url=MAYASCAN_EXPLORER_URL),
    NetworkType.TESTNET: make_explorer_object('?network=testnet', base_url=MAYASCAN_EXPLORER_URL),
    NetworkType.STAGENET: make_explorer_object('?network=stagenet', base_url=MAYASCAN_EXPLORER_URL)
}
"""Explorer URLs for the Maya network by MayaScan."""

ROOT_DERIVATION_PATH = "44'/931'/0'/0/"
"""Root derivation path of crypto-keys for the Maya network."""

ROOT_DERIVATION_PATHS = {
    NetworkType.MAINNET: ROOT_DERIVATION_PATH,
    NetworkType.STAGENET: ROOT_DERIVATION_PATH,
    NetworkType.TESTNET: ROOT_DERIVATION_PATH,
}
"""Root derivation paths of crypto-keys for the Maya network."""

DEFAULT_CHAIN_IDS = {
    NetworkType.MAINNET: 'mayachain-mainnet-v1',
    NetworkType.STAGENET: 'mayachain-stagenet-v1',
    NetworkType.TESTNET: 'deprecated',
}
"""Default chain IDs for the Maya network. Subject to change."""


MAYANODE_PORT = 1317
"""API port for the Maya network."""


RPC_PORTS = {
    NetworkType.MAINNET: 27147,
    NetworkType.STAGENET: 26657,
    NetworkType.TESTNET: 26657,
}
"""RPC ports for the Maya network."""


def make_client_urls_from_ip_address(ip_address: str, network=NetworkType.MAINNET, protocol='http'):
    """
    Make client URLs from an IP address.

    :param ip_address: IP address of MayaNode
    :param network: Network type
    :param protocol: Protocol to use HTTP or HTTPS
    :return: dict of MayaNode URLs to pass to the client constructor
    """
    rpc_port = RPC_PORTS[network]
    return {
        network: NodeURL.from_ip_address(ip_address, MAYANODE_PORT, rpc_port, protocol)
    }


DEFAULT_CLIENT_URLS = {
    NetworkType.MAINNET: NodeURL(
        'https://mayanode.mayachain.info',
        'https://tendermint.mayachain.info/'
    ),
    NetworkType.STAGENET: NodeURL(
        'https://stagenet.mayanode.mayachain.info',
        'https://stagenet.mayachain.info/'
    ),
    NetworkType.TESTNET: NodeURL('deprecated', 'deprecated'),
}
"""Default client URLs for the Maya network."""

MAYA_LIQUIFY_NODE_URL = NodeURL(
    "https://api-maya.liquify.com/",
    "https://rpc-maya.liquify.com/"
)
"""MayaNode URL for the Maya network by Liquify."""

MAYA_LIQUIFY_MIDGARD_URL = "https://midgard-maya.liquify.com"
"""Midgard URL for the Maya network by Liquify."""

FALLBACK_CLIENT_URLS = {
    NetworkType.MAINNET: [],
    NetworkType.STAGENET: [],
    NetworkType.TESTNET: []
}
"""Fallback client URLs for the Maya network."""

MAYA_BLOCK_TIME_SEC = 6.0
"""The block time in seconds for the Maya network."""

CACAO_DUST = 0.0001
"""Minimum non-zero Cacao amount to be sent in MRC20 and M-NFT transactions."""

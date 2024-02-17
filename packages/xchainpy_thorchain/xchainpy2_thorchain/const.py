from decimal import Decimal

from xchainpy2_client import ExplorerProvider
from xchainpy2_utils import Asset, Amount, CryptoAmount, AssetRUNE
from xchainpy2_utils.consts import NetworkType, RUNE_DECIMAL
from .models import NodeURL

DEFAULT_GAS_ADJUSTMENT = 2

DEFAULT_GAS_LIMIT_VALUE = 6_000_000

DEPOSIT_GAS_LIMIT_VALUE = 600_000_000

MAX_TX_COUNT_PER_PAGE = 100

MAX_TX_COUNT_PER_FUNCTION_CALL = 500

MAX_PAGES_PER_FUNCTION_CALL = 15

RUNE_SYMBOL = 'ᚱ'
RUNE_TICKER = 'RUNE'

DEFAULT_RUNE_FEE = Amount.from_asset(0.02, RUNE_DECIMAL)

DEFAULT_EXPLORER_URL = 'https://viewblock.io/thorchain{path}{network_tag}'

THOR_BASIS_POINT_MAX = 10_000


def make_explorer_object(network_tag: str):
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

ROOT_DERIVATION_PATH = "44'/931'/0'/0/"

ROOT_DERIVATION_PATHS = {
    NetworkType.MAINNET: ROOT_DERIVATION_PATH,
    NetworkType.STAGENET: ROOT_DERIVATION_PATH,
    NetworkType.TESTNET: ROOT_DERIVATION_PATH,
}

DEFAULT_CHAIN_IDS = {
    NetworkType.MAINNET: 'thorchain-mainnet-v1',
    NetworkType.STAGENET: 'thorchain-stagenet-v2',
    NetworkType.TESTNET: 'deprecated',
}

THORNODE_PORT = 1317

RPC_PORTS = {
    NetworkType.MAINNET: 27147,
    NetworkType.STAGENET: 26657,
    NetworkType.TESTNET: 26657,
}


def make_client_urls_from_ip_address(ip_address: str, network=NetworkType.MAINNET, protocol='http'):
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

FALLBACK_CLIENT_URLS = {
    NetworkType.MAINNET: [
        NodeURL('https://thornode-v1.ninerealms.com', 'https://rpc-v1.ninerealms.com'),
        NodeURL('https://thornode.thorswap.net/', 'https://rpc.thorswap.net'),
        NodeURL('https://thornode-v0.ninerealms.com', 'https://rpc-v0.ninerealms.com'),
    ],
    NetworkType.STAGENET: [DEFAULT_CLIENT_URLS[NetworkType.STAGENET]],
    NetworkType.TESTNET: []
}

# Base "chain" asset for RUNE-67C on Binance test net.
AssetRuneBNBTestnet = Asset.from_string('BNB.RUNE-67C')

# Base "chain" asset for RUNE-B1A on Binance main net.
AssetRuneBNBMainnet = Asset.from_string('BNB.RUNE-B1A')

# Base "chain" asset for RUNE on ethereum main net.
AssetRuneERC20Mainnet = Asset.from_string('ETH.RUNE-0x3155ba85d5f96b2d030a4966af206230e46849cb')

# Base "chain" asset for RUNE on ethereum test net.
AssetRuneERC20Testnet = Asset.from_string('ETH.RUNE-0xd601c6A3a36721320573885A8d8420746dA3d7A0')

DENOM_RUNE_NATIVE = 'rune'

THOR_BLOCK_TIME_SEC = 6.0

DEFAULT_RUNE_NETWORK_FEE = CryptoAmount(Amount.from_asset(Decimal("0.02"), RUNE_DECIMAL), AssetRUNE)

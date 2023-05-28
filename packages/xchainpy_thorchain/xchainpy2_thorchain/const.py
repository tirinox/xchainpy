from packages.xchainpy_client.xchainpy2_client import ExplorerProvider
from packages.xchainpy_thorchain.xchainpy2_thorchain.models import NodeURL
from xchainpy2_utils import Asset
from xchainpy2_utils.consts import NetworkType

DEFAULT_GAS_ADJUSTMENT = 2

DEFAULT_GAS_LIMIT_VALUE = '4000000'

DEPOSIT_GAS_LIMIT_VALUE = '600000000'

MAX_TX_COUNT_PER_PAGE = 100

MAX_TX_COUNT_PER_FUNCTION_CALL = 500

MAX_PAGES_PER_FUNCTION_CALL = 15

RUNE_SYMBOL = 'ᚱ'
RUNE_TICKER = 'RUNE'

DEFAULT_EXPLORER_URL = 'https://viewblock.io/thorchain{path}{network_tag}'


def make_explorer_object(network_tag: str):
    return ExplorerProvider(
        DEFAULT_EXPLORER_URL.format(network_tag=network_tag, path=''),
        DEFAULT_EXPLORER_URL.format(network_tag=network_tag, path='/tx/{address}'),
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

# Base "chain" asset for RUNE-67C on Binance test net.
AssetRuneBNBTestnet = Asset.from_string('BNB.RUNE-67C')

# Base "chain" asset for RUNE-B1A on Binance main net.
AssetRuneBNBMainnet = Asset.from_string('BNB.RUNE-B1A')

# Base "chain" asset for RUNE on ethereum main net.
AssetRuneERC20Mainnet = Asset.from_string('ETH.RUNE-0x3155ba85d5f96b2d030a4966af206230e46849cb')

# Base "chain" asset for RUNE on ethereum test net.
AssetRuneERC20Testnet = Asset.from_string('ETH.RUNE-0xd601c6A3a36721320573885A8d8420746dA3d7A0')

DENOM_RUNE_NATIVE = 'rune'

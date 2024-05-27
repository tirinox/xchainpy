from decimal import Decimal

from xchainpy2_client import ExplorerProvider
from xchainpy2_utils import Asset, Amount, CryptoAmount, AssetCACAO
from xchainpy2_utils.consts import NetworkType, CACAO_DECIMAL
from .models import NodeURL

DEFAULT_GAS_ADJUSTMENT = 2
DEFAULT_GAS_LIMIT_VALUE = 4_000_000
DEPOSIT_GAS_LIMIT_VALUE = 600_000_000

MAX_TX_COUNT_PER_PAGE = 100

MAX_TX_COUNT_PER_FUNCTION_CALL = 500

MAX_PAGES_PER_FUNCTION_CALL = 15

RUNE_SYMBOL = 'C'
CACAO_TICKER = 'CACAO'
DENOM_CACAO_NATIVE = 'cacao'

MAYA_DECIMAL = 4
DENOM_MAYA = 'maya'

AssetMAYA = Asset.from_string('MAYA.MAYA')

DEFAULT_CACAO_NETWORK_FEE = CryptoAmount(Amount.from_asset(Decimal("0.5"), CACAO_DECIMAL), AssetCACAO)

DEFAULT_CACAO_FEE = Amount.from_asset(0.5, CACAO_DECIMAL)

DEFAULT_EXPLORER_URL = 'https://explorer.mayachain.info{path}{network_tag}'
MAYASCAN_EXPLORER_URL = 'https://mayascan.org{path}'


def make_explorer_object(network_tag: str, base_url=MAYASCAN_EXPLORER_URL):
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

MAYASCAN_EXPLORERS = {
    NetworkType.MAINNET: make_explorer_object('', base_url=MAYASCAN_EXPLORER_URL),
    NetworkType.TESTNET: make_explorer_object('?network=testnet', base_url=MAYASCAN_EXPLORER_URL),
    NetworkType.STAGENET: make_explorer_object('?network=stagenet', base_url=MAYASCAN_EXPLORER_URL)
}

ROOT_DERIVATION_PATH = "44'/931'/0'/0/"

ROOT_DERIVATION_PATHS = {
    NetworkType.MAINNET: ROOT_DERIVATION_PATH,
    NetworkType.STAGENET: ROOT_DERIVATION_PATH,
    NetworkType.TESTNET: ROOT_DERIVATION_PATH,
}

DEFAULT_CHAIN_IDS = {
    NetworkType.MAINNET: 'mayachain-mainnet-v1',
    NetworkType.STAGENET: 'mayachain-stagenet-v1',
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
        'https://mayanode.mayachain.info',
        'https://tendermint.mayachain.info/'
    ),
    NetworkType.STAGENET: NodeURL(
        'https://stagenet.mayanode.mayachain.info',
        'https://stagenet.mayachain.info/'
    ),
    NetworkType.TESTNET: NodeURL('deprecated', 'deprecated'),
}

MAYA_LIQUIFY_NODE_URL = NodeURL(
    "https://api-maya.liquify.com/",
    "https://rpc-maya.liquify.com/"
)

MAYA_LIQUIFY_MIDGARD_URL = "https://midgard-maya.liquify.com"

FALLBACK_CLIENT_URLS = {
    NetworkType.MAINNET: [],
    NetworkType.STAGENET: [],
    NetworkType.TESTNET: []
}

MAYA_BLOCK_TIME_SEC = 6.0

CACAO_DUST = 0.0001

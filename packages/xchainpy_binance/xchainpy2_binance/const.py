from xchainpy2_client import ExplorerProvider
from xchainpy2_utils.consts import NetworkType

BNB_DECIMAL = 8

MAX_TX_COUNT_PER_PAGE = 100
MAX_TX_COUNT_PER_FUNCTION_CALL = 500
MAX_PAGES_PER_FUNCTION_CALL = 15

DEFAULT_EXPLORER_URL = 'https://explorer.bnbchain.org{path}'
DEFAULT_EXPLORER_TESTNET_URL = 'https://testnet-explorer.bnbchain.org{path}'


def make_explorer_object(net: NetworkType):
    base_url = DEFAULT_EXPLORER_TESTNET_URL if net == NetworkType.TESTNET else DEFAULT_EXPLORER_URL
    return ExplorerProvider(
        base_url.format(path=''),
        base_url.format(path='/address/{address}'),
        base_url.format(path='/tx/{tx_id}'),
    )


BNB_EXPLORERS = {
    NetworkType.MAINNET: make_explorer_object(NetworkType.MAINNET),
    NetworkType.TESTNET: make_explorer_object(NetworkType.TESTNET),
    NetworkType.STAGENET: make_explorer_object(NetworkType.STAGENET)
}

LEGACY_XCHAIN_JS_DERIVATION_PATH = "44'/931'/0'/0/"  # that one is used in xchainjs-lib to the date (2023-11-24)
DEFAULT_ROOT_DERIVATION_PATH = "44'/714'/0'/0/"  # the correct one

DEFAULT_ROOT_DERIVATION_PATHS = {
    NetworkType.MAINNET: DEFAULT_ROOT_DERIVATION_PATH,
    NetworkType.STAGENET: DEFAULT_ROOT_DERIVATION_PATH,
    NetworkType.TESTNET: DEFAULT_ROOT_DERIVATION_PATH,
}

LEGACY_XCHAIN_JS_ROOT_DERIVATION_PATHS = {
    NetworkType.MAINNET: LEGACY_XCHAIN_JS_DERIVATION_PATH,
    NetworkType.STAGENET: LEGACY_XCHAIN_JS_DERIVATION_PATH,
    NetworkType.TESTNET: LEGACY_XCHAIN_JS_DERIVATION_PATH,
}

DEFAULT_CLIENT_URLS = {
    NetworkType.MAINNET: 'https://dex.binance.org',
    NetworkType.STAGENET: 'https://dex.binance.org',
    NetworkType.TESTNET: 'https://testnet-dex.binance.org',
}

FALLBACK_CLIENT_URLS = {
    NetworkType.MAINNET: [],
    NetworkType.STAGENET: [],
    NetworkType.TESTNET: []
}

# The decimal for cosmos chain.
from typing import Optional, Callable

from xchainpy2_client import Fees, FeeType, FeeOption, ExplorerProvider
from xchainpy2_utils import Amount, NetworkType

COSMOS_DECIMAL = 6

# Default gas limit
# As same as definition in Cosmosstation's web wallet
DEFAULT_GAS_LIMIT = 90_000

FEE_MINIMUM_GAS_PRICE = 0.006

# Default fee
# As same as definition in Cosmosstation's web wallet
DEFAULT_FEE = Amount.from_base(int(DEFAULT_GAS_LIMIT * FEE_MINIMUM_GAS_PRICE), COSMOS_DECIMAL)

# Chain identifier for Cosmos chain
GAIA_CHAIN_KEY = 'GAIA'

# Cosmos denomination
COSMOS_DENOM = 'uatom'

# Default derivation path for Cosmos chain
DEFAULT_DERIVATION_PATH = "44'/118'/0'/0/"

COSMOS_ROOT_DERIVATION_PATHS = {
    NetworkType.MAINNET: DEFAULT_DERIVATION_PATH,
    NetworkType.TESTNET: DEFAULT_DERIVATION_PATH,
    NetworkType.STAGENET: DEFAULT_DERIVATION_PATH,
}

# Prefix
COSMOS_ADDR_PREFIX = 'cosmos'


def get_default_fees() -> Fees:
    return Fees(
        type=FeeType.FLAT_FEE,
        fees={
            FeeOption.FAST: Amount.from_base(750, COSMOS_DECIMAL),
            FeeOption.FASTEST: Amount.from_base(2500, COSMOS_DECIMAL),
            FeeOption.AVERAGE: Amount.from_base(0, COSMOS_DECIMAL),
        }
    )


CLIENT_URL_KEPLR = 'https://lcd-cosmoshub.keplr.app'
CLIENT_URL_COSMOSTATION = 'https://lcd-cosmos.cosmostation.io/'
# The only one that works for me
CLIENT_URL_COSMOS_DIRECTORY = 'https://rest.cosmos.directory/cosmoshub'

DEFAULT_CLIENT_URLS = {
    NetworkType.MAINNET: CLIENT_URL_KEPLR,
    NetworkType.STAGENET: CLIENT_URL_KEPLR,
    # Note: In case anyone facing into CORS issue, try the following URLs
    #   // https://lcd-cosmos.cosmostation.io/
    #   // https://lcd-cosmoshub.keplr.app/
    #   // @see (Discord #xchainjs) https://discord.com/channels/838986635756044328/988096545926828082/988103739967688724
    NetworkType.TESTNET: 'https://rest.sentry-02.theta-testnet.polypore.xyz',
}

COSMOS_CHAIN_IDS = {
    NetworkType.MAINNET: 'cosmoshub-4',
    NetworkType.STAGENET: 'cosmoshub-4',
    NetworkType.TESTNET: 'theta-testnet-001',
}

TEST_EXPLORER_URL = 'https://explorer.theta-testnet.polypore.xyz/{path}'
BIG_DIPPER_EXPLORER_URL = 'https://bigdipper.live/cosmos/{path}'
MINT_SCAN_EXPLORER_URL = 'https://www.mintscan.io/cosmos/{path}'


def make_explorer(path, acc_subpath, tx_subpath):
    return ExplorerProvider(
        path.format(path=''),
        path.format(path=acc_subpath),
        path.format(path=tx_subpath),
    )


def make_explorer_std(path):
    return make_explorer(path, 'accounts/{address}', 'transactions/{tx_id}')


def make_explorer_mint_scan():
    return make_explorer(MINT_SCAN_EXPLORER_URL, 'account/{address}', 'txs/{tx_id}')


MINT_SCAN_EXPLORER_PROVIDER = {
    NetworkType.MAINNET: make_explorer_mint_scan(),
    NetworkType.STAGENET: make_explorer_mint_scan(),
    NetworkType.TESTNET: make_explorer_std(TEST_EXPLORER_URL),
}

BIG_DIPPER_EXPLORER_PROVIDER = {
    NetworkType.MAINNET: make_explorer_std(BIG_DIPPER_EXPLORER_URL),
    NetworkType.STAGENET: make_explorer_std(BIG_DIPPER_EXPLORER_URL),
    NetworkType.TESTNET: make_explorer_std(TEST_EXPLORER_URL),
}

DEFAULT_EXPLORER_PROVIDER = MINT_SCAN_EXPLORER_PROVIDER

TxFilterFunc = Optional[Callable[[object], bool]]

MAX_TX_COUNT_PER_PAGE = 100

MAX_TX_COUNT_PER_FUNCTION_CALL = 500

MAX_PAGES_PER_FUNCTION_CALL = 15

DEFAULT_REST_USER_AGENT = \
    'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'

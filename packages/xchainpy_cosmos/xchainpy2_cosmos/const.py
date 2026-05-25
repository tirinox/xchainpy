from typing import Optional, Callable

from xchainpy2_client import ExplorerProvider
from xchainpy2_utils import NetworkType, CryptoAmount, AssetATOM

COSMOS_DECIMAL = 6
"""
Cosmos Atom decimal places.
"""

DEFAULT_GAS_LIMIT = 200_000
"""
Default gas limit for Cosmos transactions.
It should be enough for most of the transfer transactions with MEMO.
"""

FEE_MINIMUM_GAS_PRICE = 0.005
"""
Minimum gas price for Cosmos transactions. 
On Cosmos Hub (chain ID cosmoshub-4), the default recommended value is 0.025 uatom per gas unit.
"""

DEFAULT_FEE = CryptoAmount.auto_base(int(DEFAULT_GAS_LIMIT * FEE_MINIMUM_GAS_PRICE), AssetATOM, COSMOS_DECIMAL)
"""
Default Max fee for Cosmos transactions.
Type: CryptoAmount
It is calculated as `DEFAULT_GAS_LIMIT * FEE_MINIMUM_GAS_PRICE`.
"""

COSMOS_DENOM = 'uatom'
"""
Cosmos Atom denomination.
"""

DEFAULT_DERIVATION_PATH = "44'/118'/0'/0/"
"""
Default derivation path for Cosmos accounts.
"""

COSMOS_ROOT_DERIVATION_PATHS = {
    NetworkType.MAINNET: DEFAULT_DERIVATION_PATH,
    NetworkType.TESTNET: DEFAULT_DERIVATION_PATH,
    NetworkType.STAGENET: DEFAULT_DERIVATION_PATH,
}
"""
Default root derivation paths for Cosmos accounts.
"""

COSMOS_ADDR_PREFIX = 'cosmos'
"""
Cosmos address prefix.
"""

CLIENT_URL_KEPLR = 'https://lcd-cosmoshub.keplr.app'
"""
Keplr client URL for Cosmos Hub.
"""

CLIENT_URL_COSMOSTATION = 'https://lcd-cosmos.cosmostation.io/'
"""
Cosmostation client URL for Cosmos Hub.
"""

CLIENT_URL_COSMOS_DIRECTORY = 'https://rest.cosmos.directory/cosmoshub'
"""
Cosmos Directory client URL for Cosmos Hub.
"""

DEFAULT_CLIENT_URLS = {
    NetworkType.MAINNET: CLIENT_URL_KEPLR,
    NetworkType.STAGENET: CLIENT_URL_KEPLR,
    # Note: In case anyone facing into CORS issue, try the following URLs
    #   // https://lcd-cosmos.cosmostation.io/
    #   // https://lcd-cosmoshub.keplr.app/
    #   // @see (Discord #xchainjs) https://discord.com/channels/838986635756044328/988096545926828082/988103739967688724
    NetworkType.TESTNET: 'https://rest.sentry-02.theta-testnet.polypore.xyz',
}
"""
Default client URLs for Cosmos networks.
Now it uses Keplr for Mainnet and Stagenet, and Theta Testnet for Testnet.
"""

COSMOS_CHAIN_IDS = {
    NetworkType.MAINNET: 'cosmoshub-4',
    NetworkType.STAGENET: 'cosmoshub-4',
    NetworkType.TESTNET: 'theta-testnet-001',
}
"""
Default chain IDs for Cosmos networks.
"""

TEST_EXPLORER_URL = 'https://explorer.theta-testnet.polypore.xyz/{path}'
"""
Testnet explorer URL for Cosmos.
"""

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
"""
Mint Scan explorer provider for Cosmos networks.
"""

BIG_DIPPER_EXPLORER_PROVIDER = {
    NetworkType.MAINNET: make_explorer_std(BIG_DIPPER_EXPLORER_URL),
    NetworkType.STAGENET: make_explorer_std(BIG_DIPPER_EXPLORER_URL),
    NetworkType.TESTNET: make_explorer_std(TEST_EXPLORER_URL),
}
"""
Big Dipper explorer provider for Cosmos networks.
"""

DEFAULT_EXPLORER_PROVIDER = MINT_SCAN_EXPLORER_PROVIDER
"""
Default explorer provider for Cosmos networks. Now it uses Mint Scan for Mainnet and Stagenet.
"""

TxFilterFunc = Optional[Callable[[object], bool]]

MAX_TX_COUNT_PER_PAGE = 100
"""
Maximum number of transactions to fetch per page.
"""

MAX_TX_COUNT_PER_FUNCTION_CALL = 500
"""
Maximum number of transactions to fetch per function call.
"""

MAX_PAGES_PER_FUNCTION_CALL = 15
"""
Maximum number of pages to fetch Txs per function call.
"""

DEFAULT_REST_USER_AGENT = \
    'Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36'
"""
Default user agent for REST requests.
"""

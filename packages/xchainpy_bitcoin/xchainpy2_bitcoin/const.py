from xchainpy2_client import ExplorerProvider, FeeBounds
from xchainpy2_utils import Asset
from xchainpy2_utils.consts import NetworkType

BTC_DECIMAL = 8

ROOT_DERIVATION_PATH_44 = "44'/0'/0'/0/"
ROOT_DERIVATION_PATH_49 = "49'/0'/0'/0/"

# Segwit modern derivation path
ROOT_DERIVATION_PATH_84 = "84'/0'/0'/0/"
ROOT_DERIVATION_PATH_TEST_NET_84 = "84'/1'/0'/0/"

ROOT_DERIVATION_PATHS = {
    NetworkType.MAINNET: ROOT_DERIVATION_PATH_84,
    NetworkType.STAGENET: ROOT_DERIVATION_PATH_84,
    NetworkType.TESTNET: ROOT_DERIVATION_PATH_TEST_NET_84,
    NetworkType.DEVNET: ROOT_DERIVATION_PATH_TEST_NET_84,
}

MIN_TX_FEE = 1000

BTC_DEFAULT_FEE_BOUNDS = FeeBounds(1, 1_000)  # in 1 sat/byte

BTC_SYMBOL = '₿'
BTC_SATOSHI_SYMBOL = '⚡'

TX_EMPTY_SIZE = 4 + 1 + 1 + 4
TX_INPUT_BASE = 32 + 4 + 1 + 4
TX_INPUT_PUBKEYHASH = 107
TX_OUTPUT_BASE = 8 + 1
TX_OUTPUT_PUBKEYHASH = 25

BTC_BLOCKSTREAM_MAINNET_EXPLORER = ExplorerProvider(
    'https://blockstream.info/',
    'https://blockstream.info/address/{address}',
    'https://blockstream.info/tx/{tx_id}',
)

BTC_BLOCKSTREAM_TESTNET_EXPLORER = ExplorerProvider(
    'https://blockstream.info/testnet/',
    'https://blockstream.info/testnet/address/{address}',
    'https://blockstream.info/testnet/tx/{tx_id}',
)

BTC_BLOCKCHAIR_MAINNET_EXPLORER = ExplorerProvider(
    'https://blockchair.com/',
    'https://blockchair.com/bitcoin/address/{address}',
    'https://blockchair.com/bitcoin/transaction/{tx_id}',
)

BTC_BLOCKCHAIR_TESTNET_EXPLORER = ExplorerProvider(
    'https://blockchair.com/',
    'https://blockchair.com/bitcoin/testnet/address/{address}',
    'https://blockchair.com/bitcoin/testnet/transaction/{tx_id}',
)

BLOCKSTREAM_EXPLORERS = {
    NetworkType.MAINNET: BTC_BLOCKSTREAM_MAINNET_EXPLORER,
    NetworkType.STAGENET: BTC_BLOCKSTREAM_MAINNET_EXPLORER,
    NetworkType.TESTNET: BTC_BLOCKSTREAM_TESTNET_EXPLORER,
}

MAX_MEMO_LENGTH = 80

DEFAULT_PROVIDER_NAMES = ['mempool', 'blockstream']

AssetTestBTC = Asset.from_string('BTC.TBTC')

from xchainpy2_client import ExplorerProvider, FeeBounds
from xchainpy2_utils import NetworkType, Asset

DOGE_DECIMAL = 8


ROOT_DERIVATION_PATHS = {
    NetworkType.MAINNET: "44'/3'/0'/0/",
    NetworkType.STAGENET: "44'/3'/0'/0/",
    NetworkType.TESTNET: "44'/1'/0'/0/",
    NetworkType.DEVNET: "44'/1'/0'/0/",
}

MIN_TX_FEE = 1000

DOGE_DEFAULT_FEE_BOUNDS = FeeBounds(10, 20_000_000)  # in 1 sat/byte

DOGE_BLOCKCHAIR_EXPLORER = ExplorerProvider(
    'https://blockchair.com/dogecoin/',
    'https://blockchair.com/dogecoin/address/{address}',
    'https://blockchair.com/dogecoin/transaction/{tx_id}',
)

DOGE_SOCHAIN_TESTNET_EXPLORER = ExplorerProvider(
    'https://sochain.com/tx/DOGETEST/',
    'https://sochain.com/address/DOGETEST/{address}',
    'https://sochain.com/tx/DOGETEST/{tx_id}',
)

DEFAULT_DOGE_EXPLORERS = {
    NetworkType.MAINNET: DOGE_BLOCKCHAIR_EXPLORER,
    NetworkType.STAGENET: DOGE_BLOCKCHAIR_EXPLORER,
    NetworkType.TESTNET: DOGE_SOCHAIN_TESTNET_EXPLORER,
}

MAX_MEMO_LENGTH = 80

DEFAULT_PROVIDER_NAMES = ['blockcypher', 'blockchair', 'blockbook']

AssetTestDOGE = Asset.from_string('DOGE.TDOGE')

from xchainpy2_client import ExplorerProvider, FeeBounds
from xchainpy2_utils import NetworkType, Asset

LTC_DECIMAL = 8

ROOT_DERIVATION_PATHS = {
    NetworkType.MAINNET: "84'/2'/0'/0/",
    NetworkType.STAGENET: "84'/2'/0'/0/",
    NetworkType.TESTNET: "84'/1'/0'/0/",
    NetworkType.DEVNET: "84'/1'/0'/0/",
}

MIN_TX_FEE = 1000

LTC_DEFAULT_FEE_BOUNDS = FeeBounds(0.5, 500)

LTC_BLOCKCHAIR_EXPLORER = ExplorerProvider(
    'https://blockchair.com/litecoin/',
    'https://blockchair.com/litecoin/address/{address}',
    'https://blockchair.com/litecoin/transaction/{tx_id}',
)

LTC_BLOCKCHIAR_TESTNET_EXPLORER = ExplorerProvider(
    'https://blockexplorer.one/litecoin/testnet/',
    'https://blockexplorer.one/litecoin/testnet/address/{address}',
    'https://blockexplorer.one/litecoin/testnet/transaction/{tx_id}',
)

BLOCKSTREAM_EXPLORERS = {
    NetworkType.MAINNET: LTC_BLOCKCHAIR_EXPLORER,
    NetworkType.STAGENET: LTC_BLOCKCHAIR_EXPLORER,
    NetworkType.TESTNET: LTC_BLOCKCHIAR_TESTNET_EXPLORER,
}

DEFAULT_LTC_EXPLORERS = BLOCKSTREAM_EXPLORERS

MAX_MEMO_LENGTH = 80

DEFAULT_PROVIDER_NAMES = ['blockcypher', 'blockchair', 'bitaps']

AssetTestLTC = Asset.from_string('LTC.TLTC')

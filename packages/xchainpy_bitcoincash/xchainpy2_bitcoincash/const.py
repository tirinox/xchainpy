from xchainpy2_client import ExplorerProvider, FeeBounds, Fees, FeeOption, FeeType
from xchainpy2_utils import NetworkType, Asset, Amount

BCH_DECIMAL = 8

ROOT_DERIVATION_PATHS = {
    NetworkType.MAINNET: "m/44'/145'/0'/0/",
    NetworkType.TESTNET: "m/44'/1'/0'/0/",
    NetworkType.STAGENET: "m/44'/145'/0'/0/",
}

BCH_DEFAULT_FEE_BOUNDS = FeeBounds(1, 500)  # in 1 sat/byte

BCH_BLOCKCHAIR_EXPLORER = ExplorerProvider(
    'https://blockchair.com/bch/',
    'https://blockchair.com/bch/address/{address}',
    'https://blockchair.com/bch/transaction/{tx_id}',
)

BCH_BLOCKCHAIR_TESTNET_EXPLORER = ExplorerProvider(
    'https://blockchair.com/bch-testnet/',
    'https://blockchair.com/bch-testnet/address/{address}',
    'https://blockchair.com/bch-testnet/transaction/{tx_id}',
)

DEFAULT_BCH_EXPLORERS = {
    NetworkType.MAINNET: BCH_BLOCKCHAIR_EXPLORER,
    NetworkType.STAGENET: BCH_BLOCKCHAIR_EXPLORER,
    NetworkType.TESTNET: BCH_BLOCKCHAIR_TESTNET_EXPLORER,
}

MAX_MEMO_LENGTH = 80

DEFAULT_PROVIDER_NAMES = []

AssetTestBCH = Asset.from_string('BCH.TBCH')

DEFAULT_BCH_FEES = Fees(
    FeeType.PER_BYTE,
    fees={
        FeeOption.AVERAGE: Amount.automatic(1, BCH_DECIMAL),
        FeeOption.FAST: Amount.automatic(3, BCH_DECIMAL),
        FeeOption.FASTEST: Amount.automatic(6, BCH_DECIMAL),
    }
)

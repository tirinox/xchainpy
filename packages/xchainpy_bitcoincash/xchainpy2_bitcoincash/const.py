from xchainpy2_client import ExplorerProvider, FeeBounds, Fees, FeeOption, FeeType
from xchainpy2_utils import NetworkType, Asset, Amount

BCH_DECIMAL = 8
"""Bitcoin Cash decimal places"""

ROOT_DERIVATION_PATHS = {
    NetworkType.MAINNET: "m/44'/145'/0'/0/",
    NetworkType.TESTNET: "m/44'/1'/0'/0/",
    NetworkType.STAGENET: "m/44'/145'/0'/0/",
}
"""Root derivation paths for Bitcoin Cash"""

BCH_DEFAULT_FEE_BOUNDS = FeeBounds(1, 500)  # in 1 sat/byte
"""Default fee bounds for Bitcoin Cash in sat/byte"""

BCH_BLOCKCHAIR_EXPLORER = ExplorerProvider(
    'https://blockchair.com/bch/',
    'https://blockchair.com/bch/address/{address}',
    'https://blockchair.com/bch/transaction/{tx_id}',
)
"""Blockchair explorer for Bitcoin Cash mainnet"""

BCH_BLOCKCHAIR_TESTNET_EXPLORER = ExplorerProvider(
    'https://blockchair.com/bch-testnet/',
    'https://blockchair.com/bch-testnet/address/{address}',
    'https://blockchair.com/bch-testnet/transaction/{tx_id}',
)
"""Blockchair explorer for Bitcoin Cash testnet"""

DEFAULT_BCH_EXPLORERS = {
    NetworkType.MAINNET: BCH_BLOCKCHAIR_EXPLORER,
    NetworkType.STAGENET: BCH_BLOCKCHAIR_EXPLORER,
    NetworkType.TESTNET: BCH_BLOCKCHAIR_TESTNET_EXPLORER,
}
"""Default explorers for Bitcoin Cash"""

MAX_MEMO_LENGTH = 80
"""Maximum memo length for Bitcoin Cash"""

DEFAULT_PROVIDER_NAMES = []
"""Default provider names for Bitcoin Cash. Not used at the moment"""

AssetTestBCH = Asset.from_string('BCH.TBCH')
"""Testnet BCH asset"""

DEFAULT_BCH_FEES = Fees(
    FeeType.PER_BYTE,
    fees={
        FeeOption.AVERAGE: Amount.automatic(1, BCH_DECIMAL),
        FeeOption.FAST: Amount.automatic(3, BCH_DECIMAL),
        FeeOption.FASTEST: Amount.automatic(6, BCH_DECIMAL),
    }
)
"""Typical fees for Bitcoin Cash"""

from xchainpy2_client import ExplorerProvider, FeeBounds
from xchainpy2_utils import NetworkType

BSC_MAINNET_EXPLORER = ExplorerProvider(
    'https://bscscan.com/',
    'https://bscscan.com/address/{address}',
    'https://bscscan.com/tx/{tx_id}',
)

BSC_TESTNET_EXPLORER = ExplorerProvider(
    'https://testnet.bscscan.com/',
    'https://testnet.bscscan.com/address/{address}',
    'https://testnet.bscscan.com/tx/{tx_id}',
)

DEFAULT_BSC_EXPLORER_PROVIDERS = {
    NetworkType.MAINNET: BSC_MAINNET_EXPLORER,
    NetworkType.TESTNET: BSC_TESTNET_EXPLORER,
    NetworkType.STAGENET: BSC_MAINNET_EXPLORER,
}

BSC_CHAIN_ID = {
    NetworkType.MAINNET: 56,
    NetworkType.TESTNET: 97,
    NetworkType.STAGENET: 56,
}

BSC_BNB_DECIMALS = 18

BSC_FEE_BOUNDS = FeeBounds(2_000_000_000, 1_000_000_000_000)

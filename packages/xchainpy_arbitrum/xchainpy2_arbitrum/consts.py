from xchainpy2_client import ExplorerProvider, FeeBounds
from xchainpy2_utils import NetworkType, Asset

ARB_MAINNET_EXPLORER = ExplorerProvider(
    'https://arbiscan.io/',
    'https://arbiscan.io/address/{address}',
    'https://arbiscan.io/tx/{tx_id}',
)

ARB_TESTNET_EXPLORER = ExplorerProvider(
    'https://sepolia.arbiscan.io/',
    'https://sepolia.arbiscan.io/address/{address}',
    'https://sepolia.arbiscan.io/tx/{tx_id}',
)

DEFAULT_ARB_EXPLORER_PROVIDERS = {
    NetworkType.MAINNET: ARB_MAINNET_EXPLORER,
    NetworkType.STAGENET: ARB_MAINNET_EXPLORER,
    NetworkType.TESTNET: ARB_TESTNET_EXPLORER,
}

ARB_CHAIN_ID = {
    # Arbitrum one
    NetworkType.MAINNET: 42161,
    NetworkType.STAGENET: 42161,
    NetworkType.TESTNET: 421614,  # Arbitrum Sepolia testnet
}

ARB_DECIMALS = 18

ARB_FEE_BOUNDS = FeeBounds(2_000_000_000, 1_000_000_000_000)

FREE_ARB_PROVIDERS = {
    # https://chainlist.org/chain/42161
    NetworkType.MAINNET: [
        "https://arb1.arbitrum.io/rpc",
        "https://rpc.ankr.com/arbitrum",
        "https://1rpc.io/arb",
    ],
    # https://chainlist.org/chain/421614
    NetworkType.TESTNET: [
        "https://sepolia-rollup.arbitrum.io/rpc",
    ],
}

FREE_ARB_PROVIDERS[NetworkType.STAGENET] = FREE_ARB_PROVIDERS[NetworkType.MAINNET]

ARB_NORMAL_FEE = 30  # nARB
ARB_SURE_FEE = 50  # nARB

AssetAETH = Asset.from_string("ARB.ETH")

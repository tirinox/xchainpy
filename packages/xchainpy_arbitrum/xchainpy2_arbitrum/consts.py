import os

from xchainpy2_client import ExplorerProvider, FeeBounds
from xchainpy2_utils import NetworkType, Asset

"""
    Explorer providers for the Arbitrum network.
"""
ARB_MAINNET_EXPLORER = ExplorerProvider(
    'https://arbiscan.io/',
    'https://arbiscan.io/address/{address}',
    'https://arbiscan.io/tx/{tx_id}',
)

"""
    Explorer providers for the Arbitrum testnet.
"""
ARB_TESTNET_EXPLORER = ExplorerProvider(
    'https://sepolia.arbiscan.io/',
    'https://sepolia.arbiscan.io/address/{address}',
    'https://sepolia.arbiscan.io/tx/{tx_id}',
)

"""
    Default explorer providers for the Arbitrum network.
"""
DEFAULT_ARB_EXPLORER_PROVIDERS = {
    NetworkType.MAINNET: ARB_MAINNET_EXPLORER,
    NetworkType.STAGENET: ARB_MAINNET_EXPLORER,
    NetworkType.TESTNET: ARB_TESTNET_EXPLORER,
}

"""
    Arbitrum chain IDs.
"""
ARB_CHAIN_ID = {
    # Arbitrum one
    NetworkType.MAINNET: 42161,
    NetworkType.STAGENET: 42161,
    NetworkType.TESTNET: 421614,  # Arbitrum Sepolia testnet
}

"""
    Arbitrum ETH decimals.
"""
ARB_DECIMALS = 18

"""
    Default Arbitrum fee bounds, protection against incorrectly set gas
"""
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

"""
    Default Arbitrum gas prices in gwei.
"""
ARB_NORMAL_FEE = 30

"""
    Default Arbitrum gas prices in gwei for sure transactions.
"""
ARB_SURE_FEE = 50

"""
    This is ETH asset on Arbitrum network. It is the gas asset.
"""
AssetAETH = Asset.from_string("ARB.ETH")

SELF_DIR = os.path.dirname(os.path.abspath(__file__))

ARB_TOKEN_LIST = f"{SELF_DIR}/data/arb_mainnet_latest.json"
"""
    Arbitrum ERC20 Token List
    Source: CoinGecko
"""

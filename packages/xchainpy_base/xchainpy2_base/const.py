import os

from xchainpy2_client import ExplorerProvider, FeeBounds
from xchainpy2_utils import NetworkType

""" 
    Base Mainnet Explorer URLS 
"""
BASE_MAINNET_EXPLORER = ExplorerProvider(
    'https://basescan.org/',
    'https://basescan.org/address/{address}',
    'https://basescan.org/tx/{tx_id}',
)

""" 
    Base Sepolia Testnet Explorer URLS 
"""
BASE_TESTNET_EXPLORER = ExplorerProvider(
    'https://sepolia.basescan.org/',
    'https://sepolia.basescan.org/address/{address}',
    'https://sepolia.basescan.org/tx/{tx_id}',
)

""" 
    Default Base Explorer Providers 
"""
DEFAULT_BASE_EXPLORER_PROVIDERS = {
    NetworkType.MAINNET: BASE_MAINNET_EXPLORER,
    NetworkType.STAGENET: BASE_MAINNET_EXPLORER,
    NetworkType.TESTNET: BASE_TESTNET_EXPLORER,
}

""" 
    Base Chain ID 
"""
BASE_CHAIN_ID = {
    NetworkType.MAINNET: 8453,
    NetworkType.STAGENET: 8453,
    NetworkType.TESTNET: 84532,
}

""" 
    Base Eth Decimals BASE 
"""
BASE_DECIMALS = 18

""" 
    Base Fee Bounds, protection against incorrectly set gas 
"""
BASE_FEE_BOUNDS = FeeBounds(1_000_000, 1_000_000_000)

""" 
    Free WEB3 Providers for Base Chain 
"""
FREE_BASE_PROVIDERS = {
    # https://chainlist.org/chain/8453
    NetworkType.MAINNET: [
        "https://base.llamarpc.com",
        "https://base-pokt.nodies.app",
        "https://mainnet.base.org",
    ],
    # https://chainlist.org/chain/84532
    NetworkType.TESTNET: [
        "https://base-sepolia.gateway.tenderly.co",
    ],
}

FREE_BASE_PROVIDERS[NetworkType.STAGENET] = FREE_BASE_PROVIDERS[NetworkType.MAINNET]

SELF_DIR = os.path.dirname(os.path.abspath(__file__))

BASE_TOKEN_LIST = f'{SELF_DIR}/data/base_mainnet_latest.json'
"""
    Base ERC20 token list (Popular and verified tokens)
    Source: ThorNode
    https://gitlab.com/thorchain/thornode/-/blob/develop/common/tokenlist/basetokens/base_mainnet_latest.json?ref_type=heads
"""

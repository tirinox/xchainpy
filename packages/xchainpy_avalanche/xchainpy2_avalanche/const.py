import os

from xchainpy2_client import ExplorerProvider, FeeBounds
from xchainpy2_utils import NetworkType

""" 
    Avalanche Mainnet Explorer URLS 
"""
AVAX_MAINNET_EXPLORER = ExplorerProvider(
    'https://snowtrace.io/',
    'https://snowtrace.io/address/{address}',
    'https://snowtrace.io/tx/{tx_id}',
)

""" 
    Avalanche Testnet Explorer URLS 
"""
AVAX_TESTNET_EXPLORER = ExplorerProvider(
    'https://testnet.snowtrace.io/',
    'https://testnet.snowtrace.io/address/{address}',
    'https://testnet.snowtrace.io/tx/{tx_id}',
)

""" 
    Default Avalanche Explorer Providers 
    """
DEFAULT_AVAX_EXPLORER_PROVIDERS = {
    NetworkType.MAINNET: AVAX_MAINNET_EXPLORER,
    NetworkType.STAGENET: AVAX_MAINNET_EXPLORER,
    NetworkType.TESTNET: AVAX_TESTNET_EXPLORER,
}

""" 
    Avalanche Chain ID 
"""
AVAX_CHAIN_ID = {
    NetworkType.MAINNET: 43114,
    NetworkType.STAGENET: 43114,
    NetworkType.TESTNET: 43113,
}

""" 
    Avalanche Decimals AVAX 
"""
AVAX_DECIMALS = 18

""" 
    Avalanche Fee Bounds, protection against incorrectly set gas 
"""
AVAX_FEE_BOUNDS = FeeBounds(100_000_000, 1_000_000_000)

""" 
    Free WEB3 Providers for Avalanche 
"""
FREE_AVAX_PROVIDERS = {
    # https://chainlist.org/chain/43114
    NetworkType.MAINNET: [
        "https://rpc.ankr.com/avalanche",
        "https://1rpc.io/avax/c",
    ],
    # https://chainlist.org/chain/43113
    NetworkType.TESTNET: [
        "https://rpc.ankr.com/avalanche_fuji",
    ],
}

FREE_AVAX_PROVIDERS[NetworkType.STAGENET] = FREE_AVAX_PROVIDERS[NetworkType.MAINNET]

""" 
    Avalanche Normal Fee in nAvax
"""
AVAX_NORMAL_FEE = 30  # nAvax

""" 
    Avalanche Sure Fee in nAvax
"""
AVAX_SURE_FEE = 50  # nAvax

SELF_DIR = os.path.dirname(os.path.abspath(__file__))

AVAX_TOKEN_LIST = f'{SELF_DIR}/data/avax_mainnet_latest.json'
"""
    Avalanche ERC20 token list (Popular and verified tokens)
    Source: Trader Joe Default
"""

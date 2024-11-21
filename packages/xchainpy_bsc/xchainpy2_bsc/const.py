import os

from xchainpy2_client import ExplorerProvider, FeeBounds
from xchainpy2_utils import NetworkType, Asset

"""
    Binance Smart Chain Mainnet explorer URLS
"""
BSC_MAINNET_EXPLORER = ExplorerProvider(
    'https://bscscan.com/',
    'https://bscscan.com/address/{address}',
    'https://bscscan.com/tx/{tx_id}',
)

"""
    Binance Smart Chain Testnet explorer URLS
"""
BSC_TESTNET_EXPLORER = ExplorerProvider(
    'https://testnet.bscscan.com/',
    'https://testnet.bscscan.com/address/{address}',
    'https://testnet.bscscan.com/tx/{tx_id}',
)

"""
    Binance Smart Chain Default Explorer URLS
"""
DEFAULT_BSC_EXPLORER_PROVIDERS = {
    NetworkType.MAINNET: BSC_MAINNET_EXPLORER,
    NetworkType.STAGENET: BSC_MAINNET_EXPLORER,
    NetworkType.TESTNET: BSC_TESTNET_EXPLORER,
}

"""
    Binance Smart Chain Chain IDs
"""
BSC_CHAIN_ID = {
    NetworkType.MAINNET: 56,
    NetworkType.STAGENET: 56,
    NetworkType.TESTNET: 97,
}

"""
    Binance Smart Chain BNB Decimals
"""
BSC_BNB_DECIMALS = 18

"""
    Default Binance Smart Chain Fee Bounds, protection against incorrectly set gas
"""
BSC_FEE_BOUNDS = FeeBounds(2_000_000_000, 1_000_000_000_000)

"""
    Free Binance Smart Chain WEB3 Providers
"""
FREE_BSC_PROVIDERS = {
    # https://chainlist.org/chain/56
    NetworkType.MAINNET: [
        "https://bsc-dataseed.bnbchain.org",
        "https://1rpc.io/bnb",
        "https://bsc-mainnet.public.blastapi.io",
    ],
    # https://chainlist.org/chain/97
    NetworkType.TESTNET: [
        "https://bsc-testnet-rpc.publicnode.com",
        "https://public.stackup.sh/api/v1/node/bsc-testnet",
        "https://bsc-testnet.public.blastapi.io",
    ],
}

FREE_BSC_PROVIDERS[NetworkType.STAGENET] = FREE_BSC_PROVIDERS[NetworkType.MAINNET]

"""
    Binance Smart Chain Normal Fee in gwei
"""
BSC_NORMAL_FEE = 1  # gwei

"""
    Binance Smart Chain Sure Fee in gwei
"""
BSC_SURE_FEE = 30  # gwei

SELF_DIR = os.path.dirname(os.path.abspath(__file__))

BSC_TOKEN_LIST = f'{SELF_DIR}/data/bsc_mainnet_latest.json'
"""
    Binance Smart Chain ERC20 Token List
    Source: PancakeSwap Extended
"""

AssetBSC_USDT = Asset.from_string('BSC.USDT-0X55D398326F99059FF775485246999027B3197955')
"""
    Binance Smart Chain USDT Asset (Tether)
"""

AssetBSC_USDC = Asset.from_string('BSC.USDC-0X8AC76A51CC950D9822D68B83FE1AD97B32CD580D')
"""
    Binance Smart Chain USDC Asset (Circle)
"""

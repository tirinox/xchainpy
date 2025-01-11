import os

from xchainpy2_client import ExplorerProvider, FeeBounds
from xchainpy2_utils import NetworkType, Asset, CryptoAmount, AssetBaseETH

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
        'https://1rpc.io/base',
        "https://base.llamarpc.com",
        "https://base-pokt.nodies.app",
        "https://mainnet.base.org",
    ],
    # https://chainlist.org/chain/84532
    NetworkType.TESTNET: [
        'https://base-sepolia-rpc.publicnode.com',
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

AssetBaseUSDC = Asset.from_string('BASE.USDC-0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913').upper()
"""
    Native USDC on Base Chain
"""

AssetBaseBridgedUSDC = Asset.from_string('BASE.USDC-0xd9aAEc86B65D86f6A7B5B1b0c42FFA531710b6CA').upper()
"""
    USD Base Coin (USDbC) is a bridged version of USDC which provides developers with a stablecoin solution for Base at 
    the time of mainnet launch. This bridged contract allows users to move USDC from Ethereum seamlessly to Base. 
    Separate and distinct naming helps make it clear to developers and users that this asset is bridged to Base.
    https://help.coinbase.com/en/coinbase/getting-started/crypto-education/usd-base-coin
"""

AssetBaseDAI = Asset.from_string('BASE.DAI-0x50c5725949A6F0c72E6C4a641F24049A917DB0Cb').upper()
"""
    DAI stable coin on Base Chain
"""

AssetBaseWETH = Asset.from_string('BASE.WETH-0x4200000000000000000000000000000000000006').upper()
"""
    Wrapped Ethereum on Base Chain
"""

AssetCbBTC = Asset.from_string('BASE.cbBTC-0xcbB7C0000aB88B473b1f5aFd9ef808440eed33Bf').upper()
"""
    Coinbase Wrapped BTC on Base Chain
"""

BASE_NORMAL_GAS_PRICE = CryptoAmount.from_base(0.03 * 10 ** 9, AssetBaseETH, BASE_DECIMALS)
"""
    Base Normal Gas Price. Please note that this is a rough estimate and can vary depending on the network congestion.
    Note: please use the estimation methods provided by the library to get the most accurate gas price.
"""

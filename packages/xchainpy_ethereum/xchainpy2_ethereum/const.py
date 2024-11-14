import os

from xchainpy2_client import ExplorerProvider
from xchainpy2_ethereum.gas import GasLimits
from xchainpy2_utils import NetworkType

SELF_DIR = os.path.dirname(os.path.abspath(__file__))

ETH_DECIMALS = 18
"""
    Ethereum Decimals
    The resolution of eth is 18 decimals, which means that 1 eth = "1 followed by 18 zeros" wei eth.
"""

MAIN_NET_ETHERSCAN_PROVIDER = ExplorerProvider(
    'https://etherscan.io',
    'https://etherscan.io/address/{address}',
    'https://etherscan.io/tx/{tx_id}',
)
"""
    Ethereum Mainnet explorer URLS (Etherscan.io)
"""

DEFAULT_ETH_EXPLORER_PROVIDERS = {
    NetworkType.MAINNET: MAIN_NET_ETHERSCAN_PROVIDER,
    NetworkType.TESTNET: ExplorerProvider(
        # sepolia
        'https://sepolia.etherscan.io/',
        'https://sepolia.etherscan.io/address/{address}',
        'https://sepolia.etherscan.io/tx/{tx_id}',
    ),
    NetworkType.STAGENET: MAIN_NET_ETHERSCAN_PROVIDER,
}
"""
    Ethereum Default Explorer URLS
"""

ETH_ROOT_DERIVATION_PATHS = {
    NetworkType.MAINNET: "m/44'/60'/0'/0/",
    NetworkType.TESTNET: "m/44'/60'/0'/0/",
    NetworkType.STAGENET: "m/44'/60'/0'/0/",
}
"""
    Ethereum Root Derivation Paths
"""

ETH_CHAIN_ID = {
    NetworkType.MAINNET: 1,
    NetworkType.TESTNET: 11155111,  # sepolia
    NetworkType.STAGENET: 1,
}
"""
    Ethereum Chain IDs.
    In the Ethereum Virtual Machine (EVM), the Chain ID is a unique identifier assigned to each blockchain to 
    prevent replay attacks, where a transaction on one chain could be copied and reused on another. 
    The Chain ID was introduced in EIP-155 to add an additional layer of security and to help distinguish between 
    different Ethereum-compatible networks, like Ethereum mainnet, testnets, and sidechains.
"""

FREE_ETH_PROVIDERS = {
    NetworkType.MAINNET: [
        "https://rpc.ankr.com/eth",
        "https://eth-mainnet.public.blastapi.io",
        "https://eth.llamarpc.com",
        "https://cloudflare-eth.com/",
        "https://rpc.flashbots.net/",
    ],
    NetworkType.TESTNET: [
        "https://rpc2.sepolia.org",
        "https://sepolia.drpc.org",
        "wss://sepolia.gateway.tenderly.co",
    ],
}
"""
    Free public Ethereum WEB3 Providers.
    These providers are used by default, and they may have some limitations.
    You better use your own provider for production.
"""

FREE_ETH_PROVIDERS[NetworkType.STAGENET] = FREE_ETH_PROVIDERS[NetworkType.MAINNET]

GAS_LIMITS = {
    NetworkType.MAINNET: GasLimits.default(),
    NetworkType.TESTNET: GasLimits.default(),
    NetworkType.STAGENET: GasLimits.default(),
}
"""
    Ethereum default gas limits
"""

EVM_NULL_ADDRESS = '0x0000000000000000000000000000000000000000'
"""
    Ethereum Null Address
"""

ETH_NORMAL_PRIORITY_FEE_WEI = 1500000000  # 1.5 Gwei
"""
    Ethereum Normal Fee in gwei
    This is a typical fee for a transaction but it can be increased or decreased based on your needs
"""

ETH_TOKEN_LIST = f"{SELF_DIR}/data/eth_mainnet_latest.json"
"""
    Ethereum ERC20 Token List
    Source: 1inch
"""

ERC20_ABI_FILE = f'{SELF_DIR}/data/abi/erc20.json'

ROUTER_ABI_FILE = f'{SELF_DIR}/data/abi/router.json'

MAX_APPROVAL = 2 ** 256 - 1
"""Maximum approval value for ERC20 tokens"""

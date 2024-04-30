from typing import NamedTuple

from xchainpy2_client import ExplorerProvider
from xchainpy2_ethereum.gas import GasLimits
from xchainpy2_utils import NetworkType

ETH_DECIMALS = 18

MAIN_NET_ETHERSCAN_PROVIDER = ExplorerProvider(
    'https://etherscan.io',
    'https://etherscan.io/address/{address}',
    'https://etherscan.io/tx/{tx_id}',
)

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

ETH_ROOT_DERIVATION_PATHS = {
    NetworkType.MAINNET: "m/44'/60'/0'/0/",
    NetworkType.TESTNET: "m/44'/60'/0'/0/",
    NetworkType.STAGENET: "m/44'/60'/0'/0/",
}

ETH_CHAIN_ID = {
    NetworkType.MAINNET: 1,
    NetworkType.TESTNET: 11155111,  # sepolia
    NetworkType.STAGENET: 1,
}

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

FREE_ETH_PROVIDERS[NetworkType.STAGENET] = FREE_ETH_PROVIDERS[NetworkType.MAINNET]


GAS_LIMITS = {
    NetworkType.MAINNET: GasLimits.default(),
    NetworkType.TESTNET: GasLimits.default(),
    NetworkType.STAGENET: GasLimits.default(),
}

EVM_NULL_ADDRESS = '0x0000000000000000000000000000000000000000'

ETH_NORMAL_PRIORITY_FEE_WEI = 1500000000  # 1.5 Gwei

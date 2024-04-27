from xchainpy2_client import ExplorerProvider, FeeBounds
from xchainpy2_utils import NetworkType

AVAX_MAINNET_EXPLORER = ExplorerProvider(
    'https://snowtrace.io/',
    'https://snowtrace.io/address/{address}',
    'https://snowtrace.io/tx/{tx_id}',
)

AVAX_TESTNET_EXPLORER = ExplorerProvider(
    'https://testnet.snowtrace.io/',
    'https://testnet.snowtrace.io/address/{address}',
    'https://testnet.snowtrace.io/tx/{tx_id}',
)

DEFAULT_AVAX_EXPLORER_PROVIDERS = {
    NetworkType.MAINNET: AVAX_MAINNET_EXPLORER,
    NetworkType.STAGENET: AVAX_MAINNET_EXPLORER,
    NetworkType.TESTNET: AVAX_TESTNET_EXPLORER,
}

AVAX_CHAIN_ID = {
    NetworkType.MAINNET: 43114,
    NetworkType.STAGENET: 43114,
    NetworkType.TESTNET: 43113,
}

AVAX_DECIMALS = 18

AVAX_FEE_BOUNDS = FeeBounds(2_000_000_000, 1_000_000_000_000)

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

AVAX_NORMAL_FEE = 30  # nAvax
AVAX_SURE_FEE = 50  # nAvax

from xchainpy2_client import ExplorerProvider
from xchainpy2_utils import NetworkType

ETH_DECIMAL = 18

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

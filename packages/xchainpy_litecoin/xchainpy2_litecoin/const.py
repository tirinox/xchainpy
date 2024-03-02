from xchainpy2_utils import NetworkType

LTC_DECIMAL = 8


ROOT_DERIVATION_PATHS = {
    NetworkType.MAINNET: "84'/2'/0'/0/",
    NetworkType.STAGENET: "84'/2'/0'/0/",
    NetworkType.TESTNET: "84'/1'/0'/0/",
    NetworkType.DEVNET: "84'/1'/0'/0/",
}

MIN_TX_FEE = 1000
LOWER_FEE_BOUND = 0.5
UPPER_FEE_BOUND = 500

LTC_EXPLORER = {
    NetworkType.MAINNET: {
    }
}
 
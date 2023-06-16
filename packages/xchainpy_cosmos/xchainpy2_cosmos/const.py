# The decimal for cosmos chain.
from xchainpy2_client import Fees, FeeType, FeeOption
from xchainpy2_utils import Amount, NetworkType

COSMOS_DECIMAL = 6

# Default gas limit
# As same as definition in Cosmosstation's web wallet
DEFAULT_GAS_LIMIT = '200000'

# Default fee
# As same as definition in Cosmosstation's web wallet
DEFAULT_FEE = Amount.from_base(5000, COSMOS_DECIMAL)

# Chain identifier for Cosmos chain
GAIA_CHAIN_KEY = 'GAIA'

# Default derivation path for Cosmos chain
DEFAULT_DERIVATION_PATH = "44'/118'/0'/0/"

COSMOS_ROOT_DERIVATION_PATHS = {
    NetworkType.MAINNET: DEFAULT_DERIVATION_PATH,
    NetworkType.TESTNET: DEFAULT_DERIVATION_PATH,
    NetworkType.STAGENET: DEFAULT_DERIVATION_PATH,
}

# Prefix
COSMOS_PREFIX = 'cosmos'


def get_default_fees() -> Fees:
    return Fees(
        type=FeeType.FLAT_FEE,
        fees={
            FeeOption.FAST: Amount.from_base(750, COSMOS_DECIMAL),
            FeeOption.FASTEST: Amount.from_base(2500, COSMOS_DECIMAL),
            FeeOption.AVERAGE: Amount.from_base(0, COSMOS_DECIMAL),
        }
    )


MAIN_CLIENT_URL = 'https://rest.cosmos.directory/cosmoshub'

DEFAULT_CLIENT_URLS = {
    NetworkType.MAINNET: MAIN_CLIENT_URL,
    NetworkType.STAGENET: MAIN_CLIENT_URL,
    # Note: In case anyone facing into CORS issue, try the following URLs
    #   // https://lcd-cosmos.cosmostation.io/
    #   // https://lcd-cosmoshub.keplr.app/
    #   // @see (Discord #xchainjs) https://discord.com/channels/838986635756044328/988096545926828082/988103739967688724
    NetworkType.TESTNET: 'https://rest.sentry-02.theta-testnet.polypore.xyz',
}

COSMOS_CHAIN_IDS = {
    NetworkType.MAINNET: 'cosmoshub-4',
    NetworkType.STAGENET: 'cosmoshub-4',
    NetworkType.TESTNET: 'theta-testnet-001',
}
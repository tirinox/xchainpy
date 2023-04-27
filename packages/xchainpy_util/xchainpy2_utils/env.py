# Pre-hard-fork endpoints (blocks 1 through 4786559):
from enum import Enum

THORNODE_9R_ARCHIVE_V0 = 'https://thornode-v0.ninerealms.com'

# Post-hard-fork endpoints (block 4786560 to present):
THORNODE_9R_CURRENT = 'https://thornode-v1.ninerealms.com'


class Environment(Enum):
    TESTNET = 'testnet'
    STAGENET = 'stagenet'
    MAINNET = 'mainnet'


class MidgardURL:
    THORCHAIN_9R_MAINNET = 'https://midgard.ninerealms.com'
    THORCHAIN_9R_STAGENET = 'https://stagenet-midgard.ninerealms.com'
    THORCHAIN_TESTNET = 'https://testnet.midgard.thorchain.info'
    THORCHAIN_THORSWAP_MAINNET = 'https://midgard.thorswap.net'
    MAYACHAIN_MAINNET = 'https://midgard.mayachain.info'

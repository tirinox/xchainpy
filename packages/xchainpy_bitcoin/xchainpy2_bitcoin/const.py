from xchainpy2_client import ExplorerProvider, FeeBounds
from xchainpy2_utils import Asset
from xchainpy2_utils.consts import NetworkType

"""
    Bitcoin Decimals places 
"""
BTC_DECIMAL = 8

"""
    BIP44 derivation path for Bitcoin mainnet wallets.
    
    This path is used for deriving keys according to BIP44 standard for
    compatibility with older Bitcoin wallets. These are non-segwit addresses. 
    These addresses always begin with a 1.
"""
ROOT_DERIVATION_PATH_44 = "44'/0'/0'/0/"

"""
    BIP49 derivation path for Bitcoin mainnet wallets.
    
    BIP49 refers to the accepted common standard of deriving segwit "compatibility" addresses. 
    These addresses begin with a 3.
"""
ROOT_DERIVATION_PATH_49 = "49'/0'/0'/0/"

"""
    BIP84 derivation path for Bitcoin mainnet wallets.
    
    BIP84 refers to the accepted common standard of deriving native segwit addresses. 
    These addresses always begin with bc1 - and are referred to bech32 addresses.    
"""
ROOT_DERIVATION_PATH_84 = "84'/0'/0'/0/"

"""
    BIP44 derivation path for Bitcoin testnet wallets.
"""
ROOT_DERIVATION_PATH_TEST_NET_84 = "84'/1'/0'/0/"

"""
    Dictionary of derivation paths for different networks.
    BIP84 is used for all networks.
"""
ROOT_DERIVATION_PATHS = {
    NetworkType.MAINNET: ROOT_DERIVATION_PATH_84,
    NetworkType.STAGENET: ROOT_DERIVATION_PATH_84,
    NetworkType.TESTNET: ROOT_DERIVATION_PATH_TEST_NET_84,
    NetworkType.DEVNET: ROOT_DERIVATION_PATH_TEST_NET_84,
}


"""
    Default fee bounds for Bitcoin transactions.
    The minimum fee is set to 1 sat/byte and the maximum fee is set to 1000 sat/byte.
    Fees which are higher than this are considered to be too high and are rejected.
"""
BTC_DEFAULT_FEE_BOUNDS = FeeBounds(1, 1_000)  # in 1 sat/byte

"""
    Unicode symbols for Bitcoin.
"""
BTC_SYMBOL = '₿'

"""
    Unicode symbol for Satoshi.
"""
BTC_SATOSHI_SYMBOL = '⚡'


"""
    Explorer providers for Bitcoin (Blockstream mainnet).
"""
BTC_BLOCKSTREAM_MAINNET_EXPLORER = ExplorerProvider(
    'https://blockstream.info/',
    'https://blockstream.info/address/{address}',
    'https://blockstream.info/tx/{tx_id}',
)

"""
    Explorer providers for Bitcoin (Blockstream testnet).
"""
BTC_BLOCKSTREAM_TESTNET_EXPLORER = ExplorerProvider(
    'https://blockstream.info/testnet/',
    'https://blockstream.info/testnet/address/{address}',
    'https://blockstream.info/testnet/tx/{tx_id}',
)

"""
    Explorer providers for Bitcoin (Blockchair mainnet).
"""
BTC_BLOCKCHAIR_MAINNET_EXPLORER = ExplorerProvider(
    'https://blockchair.com/',
    'https://blockchair.com/bitcoin/address/{address}',
    'https://blockchair.com/bitcoin/transaction/{tx_id}',
)

"""
    Explorer providers for Bitcoin (Blockchair testnet).
"""
BTC_BLOCKCHAIR_TESTNET_EXPLORER = ExplorerProvider(
    'https://blockchair.com/',
    'https://blockchair.com/bitcoin/testnet/address/{address}',
    'https://blockchair.com/bitcoin/testnet/transaction/{tx_id}',
)

"""
    Explorer providers for Bitcoin (Blockcypher mainnet).
"""
BLOCKSTREAM_EXPLORERS = {
    NetworkType.MAINNET: BTC_BLOCKSTREAM_MAINNET_EXPLORER,
    NetworkType.STAGENET: BTC_BLOCKSTREAM_MAINNET_EXPLORER,
    NetworkType.TESTNET: BTC_BLOCKSTREAM_TESTNET_EXPLORER,
}

"""
    Maximum memo length for Bitcoin. 
    Please refer to the following link for more information about memo length reduction:
    https://dev.thorchain.org/concepts/memo-length-reduction.html
"""
MAX_MEMO_LENGTH = 80

"""
    Default Bitcoin provider that are used to broadcast transactions and get transaction data.
"""
DEFAULT_PROVIDER_NAMES = ['mempool', 'blockstream']

AssetTestBTC = Asset.from_string('BTC.TBTC')
"""
    Asset for Bitcoin.
"""

FOO = AssetTestBTC
"""
    FOO
"""

from xchainpy2_client import NoClient

# You don't have to install absolutely all clients. You can install only the ones you need.
# We will try to import all clients and if they are not found, we will use NoClient instead.
try:
    from xchainpy2_binance import BinanceChainClient
except ImportError:
    BinanceChainClient = NoClient

try:
    from xchainpy2_bitcoin import BitcoinClient
except ImportError:
    BitcoinClient = NoClient

try:
    from xchainpy2_cosmos import CosmosGaiaClient
except ImportError:
    CosmosGaiaClient = NoClient

try:
    from xchainpy2_mayachain import MayaChainClient
except ImportError:
    MayaChainClient = NoClient

try:
    from xchainpy2_thorchain import THORChainClient
except ImportError:
    THORChainClient = NoClient

try:
    from xchainpy2_ethereum import EthereumClient
except ImportError:
    EthereumClient = NoClient

try:
    from xchainpy2_bsc import BinanceSmartChainClient
except ImportError:
    BinanceSmartChainClient = NoClient


try:
    from xchainpy2_avalanche import AvalancheClient
except:
    AvalancheChainClient = NoClient

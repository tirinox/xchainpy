from xchainpy2_client import NoClient
from xchainpy2_utils import Chain

# You don't have to install absolutely all clients. You can install only the ones you need.
# We will try to import all clients and if they are not found, we will use NoClient instead.

try:
    from xchainpy2_bitcoin import BitcoinClient
except ImportError:
    BitcoinClient = NoClient

try:
    from xchainpy2_litecoin import LitecoinClient
except ImportError:
    LitecoinClient = NoClient

try:
    from xchainpy2_dogecoin import DogecoinClient
except ImportError:
    DogecoinClient = NoClient

try:
    from xchainpy2_bitcoincash import BitcoinCashClient
except ImportError:
    BitcoinCashClient = NoClient

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
    AvalancheClient = NoClient

try:
    from xchainpy2_arbitrum import ArbitrumClient
except ImportError:
    ArbitrumClient = NoClient

# You add more clients here...

CLIENT_CLASSES = {
    Chain.THORChain: THORChainClient,
    Chain.Cosmos: CosmosGaiaClient,
    Chain.Maya: MayaChainClient,
    Chain.Bitcoin: BitcoinClient,
    Chain.BitcoinCash: BitcoinCashClient,
    Chain.Litecoin: LitecoinClient,
    Chain.Doge: DogecoinClient,
    Chain.Ethereum: EthereumClient,
    Chain.BinanceSmartChain: BinanceSmartChainClient,
    Chain.Avalanche: AvalancheClient,
    Chain.Arbitrum: ArbitrumClient,
    # to be continued
}
"""
A dictionary that maps Chain to its client class.
"""

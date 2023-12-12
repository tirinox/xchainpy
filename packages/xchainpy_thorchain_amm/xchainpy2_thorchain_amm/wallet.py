from xchainpy2_client import NoClient

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

from xchainpy2_thorchain_query import THORChainQuery
from xchainpy2_utils import Chain
from xchainpy2_thorchain_amm import WalletSettings


class Wallet:
    def __init__(self, config: WalletSettings):
        if not config.query_api:
            self.query_api = THORChainQuery()
        else:
            self.query_api = config.query_api

        self.network = self.query_api.cache.network

        self.clients = {}
        self._create_clients(config)

    def _create_clients(self, config: WalletSettings):
        c = config.enabled_chains
        client_classes = {
            Chain.THORChain: THORChainClient,
            Chain.Cosmos: CosmosGaiaClient,
            Chain.Binance: BinanceChainClient,
            Chain.Maya: MayaChainClient,
            Chain.Bitcoin: BitcoinClient,
            # to be continued
        }
        for chain, chain_class in client_classes.items():
            if config.is_enabled(chain):
                if issubclass(chain_class, NoClient):
                    raise ImportError(f"{chain} client is not found. Try to install it by running"
                                      f" 'pip install xchainpy2_{chain}' or remove it from the enabled chains set in "
                                      f"config(WalletSettings).")
                self.clients[chain] = chain_class(phrase=config.phrase)

from xchainpy2_cosmos import CosmosGaiaClient
from xchainpy2_thorchain import THORChainClient
from xchainpy2_thorchain_query import THORChainQuery
from xchainpy2_utils import Chain


class Wallet:
    def __init__(self, phrase: str, query: THORChainQuery):
        self.network = query.cache.network
        self.clients = {
            Chain.THORChain: THORChainClient(network=self.network, phrase=phrase),
            Chain.Cosmos: CosmosGaiaClient(network=self.network, phrase=phrase),
            # todo: add more clients
        }

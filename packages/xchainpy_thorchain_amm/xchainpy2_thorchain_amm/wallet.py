from xchainpy2_cosmos import CosmosGaiaClient
from xchainpy2_thorchain import THORChainClient
from xchainpy2_thorchain_amm import WalletSettings
from xchainpy2_thorchain_query import THORChainQuery
from xchainpy2_utils import Chain


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
            # to be continued
        }
        for chain, chain_class in client_classes.items():
            if config.is_enabled(chain):
                self.clients[chain] = chain_class(phrase=config.phrase)

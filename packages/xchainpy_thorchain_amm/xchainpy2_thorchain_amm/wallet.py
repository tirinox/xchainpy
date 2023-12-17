import asyncio
import datetime
from typing import Optional, Set

from xchainpy2_client import NoClient, XChainClient
from xchainpy2_thorchain_query.models import InboundDetail

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
from xchainpy2_utils import Chain, EVM_CHAINS
from .models import AllBalances, ChainBalances, ALL
from .evm_helper import EVMHelper


class Wallet:
    CLIENT_CLASSES = {
        Chain.THORChain: THORChainClient,
        Chain.Cosmos: CosmosGaiaClient,
        Chain.Binance: BinanceChainClient,
        Chain.Maya: MayaChainClient,
        Chain.Bitcoin: BitcoinClient,
        # to be continued
    }

    def __init__(self, phrase: str,
                 query_api: Optional[THORChainQuery] = None,
                 enabled_chains: Set[Chain] = ALL,
                 concurrency: int = 5):
        self._semaphore = asyncio.Semaphore(concurrency)

        if not query_api:
            self.query_api = THORChainQuery()
        else:
            self.query_api = query_api

        self.enabled_chains = enabled_chains

        self.network = self.cache.network

        self.clients = {}
        self._create_clients(phrase)

        self._evm_helpers = {}
        self._init_evm_helpers()

    @property
    def cache(self):
        return self.query_api.cache

    def get_client(self, chain: Chain) -> Optional[XChainClient]:
        return self.clients.get(chain)

    def is_chain_enabled(self, chain: Chain):
        if not self.enabled_chains:
            return True
        return chain in self.enabled_chains

    def _init_evm_helpers(self):
        for chain in EVM_CHAINS:
            if self.is_chain_enabled(chain):
                self._evm_helpers[chain] = EVMHelper(self.get_client(chain), self.cache)

    def _create_clients(self, phrase):
        for chain, chain_class in self.CLIENT_CLASSES.items():
            if self.is_chain_enabled(chain):
                if issubclass(chain_class, NoClient):
                    raise ImportError(f"{chain} client is not found. Try to install it by running"
                                      f" 'pip install xchainpy2_{chain}' or remove it from the enabled chains set in "
                                      f"config(WalletSettings).")
                self.clients[chain] = chain_class(phrase=phrase)

    async def get_all_balances(self) -> AllBalances:
        result = AllBalances(
            datetime.datetime.now(),
            {}
        )
        for client in self.clients.values():
            async with self._semaphore:
                client: XChainClient
                balances = await client.get_balance()
                result.balances[client.chain] = ChainBalances(
                    client.chain, client.get_address(),
                    balances
                )
        return result

    async def get_inbound_for_chain(self, chain: Chain) -> Optional[InboundDetail]:
        details = await self.cache.get_inbound_details()
        return details.get(str(chain))

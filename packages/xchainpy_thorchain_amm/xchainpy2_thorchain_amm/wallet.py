import asyncio
import datetime
from typing import Optional

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
from xchainpy2_thorchain_amm import WalletSettings, AllBalances, ChainBalances
from .evm_helper import EVMHelper


class Wallet:
    def __init__(self, config: WalletSettings):
        self._semaphore = asyncio.Semaphore(config.concurrency)

        if not config.query_api:
            self.query_api = THORChainQuery()
        else:
            self.query_api = config.query_api

        self.network = self.cache.network

        self.clients = {}
        self._create_clients(config)

        self._evm_helpers = {}
        self._init_evm_helpers(config)

    @property
    def cache(self):
        return self.query_api.cache

    def get_client(self, chain: Chain) -> Optional[XChainClient]:
        return self.clients.get(chain)

    def _init_evm_helpers(self, config: WalletSettings):
        for chain in EVM_CHAINS:
            if config.is_enabled(chain):
                self._evm_helpers[chain] = EVMHelper(self.get_client(chain), self.cache)

    def _create_clients(self, config: WalletSettings):
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
import asyncio
import datetime
from contextlib import suppress
from typing import Optional, Set, Union, List, Tuple

from xchainpy2_client import NoClient, XChainClient
from xchainpy2_thorchain_query import THORChainQuery, THORChainCache, InboundDetail
from xchainpy2_utils import Chain, Asset
from .detect_clients import THORChainClient, CLIENT_CLASSES
# from .evm_helper import EVMHelper
from .models import AllBalances, ChainBalances, ALL

ChainCollection = Union[Set[Chain], List[Chain], Tuple[Chain]]


class Wallet:
    """
    Wallet class is a high-level interface to your multi-chain wallet.
    It allows you to get balances, transaction data, send transactions.
    You can enable or disable chains according to your needs.
    """

    def __init__(self, phrase: str,
                 query_api: Optional[THORChainQuery] = None,
                 enabled_chains: ChainCollection = ALL,
                 concurrency: int = 5,
                 default_chain: Chain = Chain.THORChain):
        """
        Initialize the Wallet with a mnemonic phrase.

        :param phrase: Seed phrase of the wallet
        :param query_api: THORChainQuery instance, if not provided, a new instance will be created
        :param enabled_chains: A set of chains that are enabled for the wallet, if not provided, all chains are enabled
        :param concurrency: Concurrency level for some async operations
        :param default_chain: Default chain for the wallet, by default it is THORChain. Used in some methods,
        like explorer URLs.
        """

        self.default_chain = default_chain

        self._semaphore = asyncio.Semaphore(concurrency)

        self.query_api = query_api or THORChainQuery()

        self._enabled_chains = set(CLIENT_CLASSES.keys()) if enabled_chains is ALL else set(enabled_chains)

        self.network = self.cache.network

        self.clients = {}
        self._create_clients(phrase)

        self._evm_helpers = {}
        self._init_evm_helpers()

    @property
    def cache(self) -> THORChainCache:
        """
        Get the cache instance of the query API.

        :return: THORChainCache
        """
        return self.query_api.cache

    def get_client(self, chain: Union[Chain, Asset]) -> Optional[XChainClient]:
        """
        Get the client class instance for the given chain.

        :param chain: Chain or Asset
        :return: XChainClient or None if not found
        """
        if isinstance(chain, Asset):
            chain = Chain(chain.chain)
        return self.clients.get(chain)

    def get_thorchain_client(self) -> Optional[THORChainClient]:
        """
        Get the THORChain client instance.

        :return: THORChainClient or None if not found
        """
        return self.get_client(Chain.THORChain)

    def is_chain_enabled(self, chain: Chain):
        """
        Check if the given chain is enabled for the wallet.

        :param chain: Chain
        :return: True if enabled, False otherwise
        """
        if not self._enabled_chains:
            return True
        return chain in self._enabled_chains

    def _init_evm_helpers(self):
        pass  # todo
        # for chain in EVM_CHAINS:
        #     if self.is_chain_enabled(chain):
        #         # noinspection PyTypeChecker
        #         self._evm_helpers[chain] = EVMHelper(self.get_client(chain), self.cache)

    def _create_clients(self, phrase):
        for chain in self._enabled_chains:
            chain_class = CLIENT_CLASSES.get(chain)
            if not chain_class or issubclass(chain_class, NoClient):
                raise ImportError(f"{chain} client is not found. Try to install it by running"
                                  f" 'pip install xchainpy2_{chain.value.lower()}' "
                                  f"or remove it from the enabled chains set in "
                                  f"config(WalletSettings).")
            # todo add kwargs!
            self.clients[chain] = chain_class(phrase=phrase)

    async def get_all_balances(self) -> AllBalances:
        """
        Get all balances for all enabled chains. Runs concurrently, see the concurrency parameter in the constructor.

        :return: AllBalances
        """
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
        """
        Get inbound details for the given chain from the THORChain.
        The result is cached.
        :param chain: Chain
        :return: InboundDetail or None if not found
        """
        details = await self.cache.get_inbound_details()
        return details.get(str(chain))

    async def close(self):
        """
        Close all clients
        """
        for client in self.clients.values():
            if hasattr(client, 'close'):
                with suppress(Exception):
                    await client.close()
            client.purge_client()

    def purge_client(self, chain: Chain):
        """
        Purge keys from the client for the given chain.
        :param chain: Chain
        """
        client = self.get_client(chain)
        if client:
            client.purge_client()

    def explorer_url_tx(self, tx_id: str):
        """
        Get the explorer URL for the given transaction ID.
        It calls the get_explorer_tx_url method of the default chain client.

        :param tx_id: Transaction ID or hash
        :return: URs string
        """
        cli = self.clients.get(self.default_chain)
        if not cli:
            raise ValueError(f"Client for {self.default_chain} is not found.")
        return cli.get_explorer_tx_url(tx_id)

    def explorer_url_address(self, address: str):
        """
        Get the explorer URL for the given address.
        It calls the get_explorer_address_url method of the default chain client.

        :param address: Address
        :return: URL string
        """
        cli = self.clients.get(self.default_chain)
        if not cli:
            raise ValueError(f"Client for {self.default_chain} is not found.")
        return cli.get_explorer_address_url(address)

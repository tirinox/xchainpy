from typing import List

from aioetherscan import Client
from aiohttp_retry import ExponentialRetry
from asyncio_throttle import Throttler

from xchainpy2_client import XcTx
from xchainpy2_utils import CryptoAmount, Chain, NetworkType
from .base import EVMDataProvider


class EtherscanDataProvider(EVMDataProvider):
    def __init__(self, chain: Chain, network: NetworkType,
                 etherscan_api_key: str, **kwargs):
        super().__init__(chain, network, **kwargs)
        self.etherscan_api_key = etherscan_api_key
        self._make_underlying_client(etherscan_api_key)

    def _chain_to_api_kind(self):
        if self.chain == Chain.Ethereum:
            return "eth"
        elif self.chain == Chain.BinanceSmartChain:
            return "bsc"
        elif self.chain == Chain.Avalanche:
            return "avax"
        elif self.chain == Chain.Arbitrum:
            return "arbitrum"
        # elif self.chain == Chain.Polygon:
        #     return "polygon"
        # elif self.chain == Chain.Optimism:
        #     return "optimism"
        # elif self.chain == Chain.Fantom:
        #     return "fantom"
        else:
            raise ValueError(f"Chain {self.chain} is not supported")

    def _get_etherscan_network(self):
        if self.network == NetworkType.MAINNET or self.network == NetworkType.STAGENET:
            return "main"
        elif self.network == NetworkType.TESTNET:
            if self.chain == Chain.Ethereum:
                return "sepolia"
            else:
                return "testnet"

    def _make_underlying_client(self, etherscan_api_key: str):
        throttler = Throttler(rate_limit=1, period=6.0)
        retry_options = ExponentialRetry(attempts=2)
        api_kind = self._chain_to_api_kind()
        network = self._get_etherscan_network()
        self.client = Client(etherscan_api_key, api_kind=api_kind, network=network, throttler=throttler,
                             retry_options=retry_options)

    def _check_access(self):
        if not self.etherscan_api_key:
            raise ValueError("Etherscan API key is required")

    async def get_erc20_token_balances(self, address: str, **kwargs) -> List[CryptoAmount]:
        self._check_access()
        holdings = await self.client.token.token_holding_erc20(address=address, **kwargs)
        return holdings

    async def get_address_transactions(self, address: str) -> List[XcTx]:
        self._check_access()
        txs = await self.client.account.get_transactions(address=address)
        return txs

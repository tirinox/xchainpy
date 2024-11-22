from typing import List

from xchainpy2_client import XcTx
from .base import EVMDataProvider
from xchainpy2_utils import Chain, NetworkType, CryptoAmount, Asset, async_wrap

try:
    from moralis import evm_api
except ImportError:
    evm_api = None


class MoralisDataProvider(EVMDataProvider):
    @async_wrap
    def get_erc20_token_balances(self, address: str) -> List[CryptoAmount]:
        results = evm_api.token.get_wallet_token_balances(self.api_key, {
            "chain": self._chain_id_for_moralis,
            "address": address
        })
        return [
            CryptoAmount.automatic(
                int(entry['balance']), Asset(self.chain.value, symbol=entry['symbol'], contract=entry['token_address']),
                entry['decimals']
            ) for entry in results
        ]

    @async_wrap
    def get_address_transactions(self, address: str, offset=0, limit=10) -> List[XcTx]:
        result = evm_api.transaction.get_wallet_transactions(
            self.api_key,
            params={
                "address": address,
                "chain": self._chain_id_for_moralis,
                "limit": limit,
            },
        )

        # todo: convert to XcTx objects
        return result

    def __init__(self, chain: Chain, network: NetworkType,
                 api_key: str, **kwargs):
        super().__init__(chain, network, **kwargs)

        if not evm_api:
            raise ValueError("Moralis SDK is not installed. Run `pip install moralis`")

        self.api_key = api_key
        self._make_underlying_client()

    def _make_underlying_client(self):
        if not evm_api:
            raise ValueError("Moralis SDK is not installed. Run `pip install moralis`")

    # noinspection PyTypeChecker
    @property
    def _chain_id_for_moralis(self) -> 'ChainList':
        if self.chain == Chain.Ethereum:
            return 'eth'
        elif self.chain == Chain.BinanceSmartChain:
            return 'bsc'
        elif self.chain == Chain.Avalanche:
            return 'avalanche'
        elif self.chain == Chain.Arbitrum:
            return 'arbitrum'
        else:
            raise ValueError(f"Chain {self.chain} is not supported by this method. Please submit a PR.")

from datetime import datetime
from typing import NamedTuple, Optional, List, Set, Dict

from xchainpy2_client import FeeOption
from xchainpy2_thorchain_query import THORChainQuery
from xchainpy2_utils import Chain, CryptoAmount, Asset

ALL = None


class WalletSettings(NamedTuple):
    phrase: str
    enabled_chains: Set[Chain]
    query_api: Optional[THORChainQuery] = None
    concurrency: int = 5

    @classmethod
    def default(cls, phrase, enabled_chains=ALL):
        return cls(
            phrase=phrase,
            enabled_chains={
                Chain.THORChain,
                Chain.Maya,
                Chain.Cosmos,
                Chain.Binance,
                Chain.Cosmos,
            } if enabled_chains is ALL else enabled_chains
        )

    def is_enabled(self, chain: Chain):
        return chain in self.enabled_chains


class ChainBalances(NamedTuple):
    chain: Chain
    address: str
    balances: List[CryptoAmount]


class AllBalances(NamedTuple):
    date: datetime
    balances: Dict[Chain, ChainBalances]

    @property
    def flat(self) -> List[CryptoAmount]:
        return [
            balance
            for chain_balances in self.balances.values()
            for balance in chain_balances.balances
        ]


class ExecuteSwap(NamedTuple):
    input: CryptoAmount
    destination_asset: Asset
    destination_address: Optional[str]
    memo: str
    fee_option: FeeOption

from typing import NamedTuple, Dict, Optional, List

from xchainpy2_client import FeeOption
from xchainpy2_midgard import Balance
from xchainpy2_thorchain_query import THORChainQuery
from xchainpy2_utils import Chain, CryptoAmount, Asset


class WalletSettings(NamedTuple):
    phrase: str
    enabled_chains: Dict[Chain, bool]
    query_api: Optional[THORChainQuery] = None

    @classmethod
    def default(cls, phrase):
        return cls(
            phrase=phrase,
            enabled_chains={
                Chain.THORChain: True,
                Chain.Cosmos: True
            }
        )

    def is_enabled(self, chain: Chain):
        return bool(self.enabled_chains.get(chain, True))


class AllBalances(NamedTuple):
    chain: Chain
    address: str
    balances: List[Balance]


class ExecuteSwap(NamedTuple):
    input: CryptoAmount
    destination_asset: Asset
    destination_address: Optional[str]
    memo: str
    fee_option: FeeOption

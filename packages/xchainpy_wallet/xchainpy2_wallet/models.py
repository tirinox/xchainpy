from datetime import datetime
from typing import NamedTuple, List, Dict

from xchainpy2_utils import Chain, CryptoAmount

ALL = None


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

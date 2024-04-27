from datetime import datetime
from typing import NamedTuple, Optional, List, Dict

from xchainpy2_client import FeeOption
from xchainpy2_utils import Chain, CryptoAmount, Asset

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


class ExecuteSwap(NamedTuple):
    input: CryptoAmount
    destination_asset: Asset
    destination_address: Optional[str]
    memo: str
    fee_option: FeeOption


class AMMException(Exception):
    def __init__(self, message, errors: list = None):
        super().__init__(message)
        self.errors = errors


class THORNameException(AMMException):
    ...

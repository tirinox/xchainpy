from typing import NamedTuple, Optional

from xchainpy2_client import FeeOption
from xchainpy2_utils import CryptoAmount, Asset


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

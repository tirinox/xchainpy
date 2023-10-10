from enum import Enum
from typing import List, Optional

from pydantic import BaseModel


class BlockcypherNetwork(Enum):
    BTC = 'btc/main'
    BTC_TEST = 'btc/test3'
    LTC = 'ltc/main'
    DOGE = 'doge/main'
    DASH = 'dash/main'


class AddressTxDTO(BaseModel, extra='allow'):
    tx_hash: str
    block_height: int
    confirmed: str


class TxInput(BaseModel, extra='allow'):
    output_value: str
    addresses: List[str]
    script_type: Optional[str]


class TxOutput(BaseModel, extra='allow'):
    value: str
    addresses: List[str]
    script_type: Optional[str]
    script: str


class Transaction(BaseModel, extra='allow'):
    hash: str
    block_hash: str
    confirmed: str

    hex: str
    inputs: List[TxInput]
    outputs: List[TxOutput]


class GetBalanceDTO(BaseModel, extra='allow'):
    balance: int
    unconfirmed_balance: int
    final_balance: int
    n_tx: int
    unconfirmed_n_tx: int
    final_n_tx: int


from enum import Enum
from typing import List, Optional

from pydantic import BaseModel


class SochainNetwork(Enum):
    BTC = 'BTC'
    BTC_TEST = 'BTCTEST'
    LTC = 'LTC'
    LTC_TEST = 'LTCTEST'
    DOGE = 'DOGE'
    DOGE_TEST = 'DOGETEST'


class TxIO(BaseModel, extra='allow'):
    index: int
    value: str
    address: str
    type: Optional[str]
    script: str


class Transaction(BaseModel, extra='allow'):
    hash: str
    block_hash: str
    confirmations: int
    time: int
    tx_hex: str
    inputs: List[TxIO]
    outputs: List[TxIO]


class AddressUTXO(BaseModel, extra='allow'):
    hash: str
    index: int
    script: str
    address: str
    tx_hex: str
    value: str
    block: int


class AddressTxDTO(BaseModel, extra='allow'):
    hash: str
    block: int
    time: int


class AddressDTO(BaseModel, extra='allow'):
    network: str
    address: str
    balance: str
    received_value: str
    pending_value: str
    total_txs: int


class GetTxsDTO(BaseModel, extra='allow'):
    transactions: List[AddressTxDTO]


class GetBalanceDTO(BaseModel, extra='allow'):
    confirmed: str
    unconfirmed: str


class BroadcastDTO(BaseModel, extra='allow'):
    tx_hex: str


class UnspentTxsDTO(BaseModel, extra='allow'):
    outputs: List[AddressUTXO]


class BroadcastTransfer(BaseModel, extra='allow'):
    network: str
    txid: str


class TxConfirmedStatus(BaseModel, extra='allow'):
    network: str
    txid: str
    confirmations: int
    is_confirmed: bool

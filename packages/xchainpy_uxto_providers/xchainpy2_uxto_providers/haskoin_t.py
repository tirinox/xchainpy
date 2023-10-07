from dataclasses import Field
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel


class HaskoinNetwork(Enum):
    BTC = 'btc'
    BTC_TEST = 'btctest'
    BCH = 'bch'
    BCH_TEST = 'bchtest'


class AddressParams(BaseModel, extra='allow'):
    haskoin_url: str = Field(..., alias='haskoinUrl')
    network: HaskoinNetwork
    address: str


class ErrorResponse(BaseModel, extra='allow'):
    error: object


class BalanceData(BaseModel, extra='allow'):
    address: str
    confirmed: int
    unconfirmed: int
    utxo: int
    txs: int
    received: int


class RawTransaction(BaseModel, extra='allow'):
    result: str


class AddressDTO(BaseModel, extra='allow'):
    network: str
    address: str
    balance: str
    received_value: str
    pending_value: str
    total_txs: int
    received: int
    utxo: int
    address: str
    txs: int
    unconfirmed: int
    confirmed: int


class TxHashParams(BaseModel, extra='allow'):
    haskoin_url: str = Field(..., alias='haskoinUrl')
    network: HaskoinNetwork
    tx_id: str


class TxIO(BaseModel, extra='allow'):
    txid: int
    output: int
    script: str
    address: str
    value: int
    type: Optional[str]


class Block(BaseModel, extra='allow'):
    height: int
    position: int


class Transaction(BaseModel, extra='allow'):
    txid: str
    block: Block
    confirmations: int
    time: int

    tx_hex: str
    inputs: List[TxIO]
    outputs: List[TxIO]


class AddressTxDTO(BaseModel, extra='allow'):
    txid: str
    block: Block
    time: int


class GetTxsDTO(BaseModel, extra='allow'):
    transactions: List[AddressTxDTO]


class TxConfirmedStatus(BaseModel, extra='allow'):
    network: str
    txid: str
    confirmations: int
    is_confirmed: bool


class AddressUTXO(BaseModel, extra='allow'):
    address: str
    block: Block
    txid: str
    index: int
    pkscript: str
    value: str
    tx_hex: str


class TxUnspent(BaseModel, extra='allow'):
    pkscript: str
    value: int
    address: str
    block: Block
    index: int
    txid: str

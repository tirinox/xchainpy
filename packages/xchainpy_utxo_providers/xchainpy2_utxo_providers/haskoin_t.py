from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field


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
    txid: str = ''
    sig_script: str = Field('', alias='sigscript')
    pk_script: str = Field('', alias='pk_script')
    address: Optional[str] = ''
    value: int
    type: str = ''


class Block(BaseModel, extra='allow'):
    height: int = 0
    position: int = 0
    mempool: int = 0


class Transaction(BaseModel, extra='allow'):
    txid: str
    block: Block
    confirmations: int = 0
    time: int
    size: int
    fee: int

    tx_hex: str = ''
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

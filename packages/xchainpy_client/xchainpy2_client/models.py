import abc
from datetime import datetime
from enum import Enum
from typing import Optional, List, NamedTuple, Dict

from xchainpy2_utils import Asset, Amount, NetworkType, CryptoAmount
from .fees import FeeBounds


class TxType(Enum):
    TRANSFER = 'transfer'
    UNKNOWN = 'unknown'


class TokenTransfer(NamedTuple):
    from_address: str
    to_address: str
    amount: Amount
    asset: Optional[Asset] = None
    tx_hash: Optional[str] = None
    outbound: bool = True  # if true, it is a transfer out of the wallet, otherwise it is a transfer into the wallet

    # outbound = true corresponds TxTo of XChainJS
    # outbound = false corresponds TxFrom of XChainJS

    @classmethod
    def to_tx(cls, from_address: str, to_address: str, amount: Amount, asset: Optional[Asset] = None, tx_hash=None):
        return cls(from_address, to_address, amount, asset, tx_hash)

    @classmethod
    def from_tx(cls, from_address: str, to_address: str, amount: Amount, asset: Optional[Asset] = None, tx_hash=None):
        return cls(from_address, to_address, amount, asset, tx_hash, outbound=False)


class XcTx(NamedTuple):
    asset: Asset
    transfers: List[TokenTransfer]
    date: Optional[datetime]
    type: TxType
    hash: str
    height: int
    memo: str = ''
    is_success: bool = True
    original: Optional[object] = None  # transaction object / dict from underlying service

    @property
    def inbound_txs(self):
        return [t for t in self.transfers if not t.outbound]

    @property
    def outbound_txs(self):
        return [t for t in self.transfers if t.outbound]


class TxPage(NamedTuple):
    total: int
    txs: List[XcTx]


class TxHistoryPage(NamedTuple):
    address: str
    offset: int = 0
    limit: int = 0
    start_time: Optional[datetime] = None
    asset: Optional[Asset] = None


RootDerivationPaths = Dict[NetworkType, str]


class XChainClientParams(NamedTuple):
    network: Optional[NetworkType] = None
    phrase: Optional[str] = None
    fee_bound: Optional[FeeBounds] = None
    root_derivation_paths: Optional[RootDerivationPaths] = None


class OnlineDataProvider(abc.ABC):
    @abc.abstractmethod
    async def get_balance(self, address: str) -> List[CryptoAmount]:
        pass

    @abc.abstractmethod
    async def get_transactions(self, address: str = '',
                               offset: int = 0,
                               limit: int = 0,
                               start_time: Optional[datetime] = None,
                               end_time: Optional[datetime] = None,
                               asset: Optional[Asset] = None) -> TxPage:
        pass

    @abc.abstractmethod
    async def get_transaction_data(self, tx_id: str) -> Optional[XcTx]:
        pass


class Witness(NamedTuple):
    value: int
    script: bytes


class UTXO(NamedTuple):
    hash: str
    index: int
    value: int
    witness_utxo: Witness
    tx_hex: str = ""
    confirmations: int = 0
    script_pub_key: bytes = b''


class SecretsException(Exception):
    """
    Exception raised for errors related to secret management: private keys, or phrases.
    """
    ...

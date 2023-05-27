import abc
from datetime import datetime
from enum import Enum
from typing import Optional, List, NamedTuple, Dict

from xchainpy2_utils import Asset, Amount, NetworkType, CryptoAmount, Address


class TxType(Enum):
    TRANSFER = 'transfer'
    UNKNOWN = 'unknown'


class TxTo(NamedTuple):
    address: str
    amount: Amount
    asset: Optional[Asset] = None


class TxFrom(NamedTuple):
    from_address: str
    from_tx_hash: str
    amount: Amount
    asset: Optional[Asset] = None


class XcTx(NamedTuple):
    asset: Asset
    # list of "from" txs. BNC will have one `TxFrom` only, `BTC` might have many transactions going "in" (based on UTXO)
    from_txs: List[TxFrom]
    # list of "to" transactions. BNC will have one `TxTo` only,
    #   `BTC` might have many transactions going "out" (based on UTXO)
    to_txs: List[TxTo]
    date: datetime
    type: TxType
    hash: str


class TxPage(NamedTuple):
    total: int
    txs: List[XcTx]


class TxHistoryPage(NamedTuple):
    address: str
    offset: int = 0
    limit: int = 0
    start_time: Optional[datetime] = None
    asset: Optional[Asset] = None


class TxHistoryParams(NamedTuple):
    address: str
    offset: int = 0
    limit: int = 0
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    asset: Optional[Asset] = None


class TxParams(NamedTuple):
    asset: Asset
    amount: Amount
    recipient: str
    memo: Optional[str] = None
    fee_rate: Optional[int] = None


class FeeOption(Enum):
    AVERAGE = 'average'
    FAST = 'fast'
    FASTEST = 'fastest'


FeeRates = Dict[FeeOption, float]


class FeeType(Enum):
    FLAT_FEE = 'base'
    PER_BYTE = 'byte'


Fee = Amount
FeeRate = float


class Fees(NamedTuple):
    type: FeeType
    fees: Dict[FeeOption, Fee]


class FeesWithRates(NamedTuple):
    fees: Fees
    rates: FeeRates


class FeeBounds(NamedTuple):
    lower: Fee
    upper: Fee


RootDerivationPaths = Dict[NetworkType, str]


class XChainClientParams(NamedTuple):
    network: Optional[NetworkType] = None
    phrase: Optional[str] = None
    fee_bound: Optional[FeeBounds] = None
    root_derivation_paths: Optional[RootDerivationPaths] = None


# export type UtxoOnlineDataProviders = Record<Network, UtxoOnlineDataProvider | undefined>

class OnlineDataProvider(abc.ABC):
    @abc.abstractmethod
    async def get_balance(self, address: str) -> List[CryptoAmount]:
        pass

    @abc.abstractmethod
    async def get_transactions(self, params: TxHistoryParams) -> TxPage:
        pass

    @abc.abstractmethod
    async def get_transaction_data(self, tx_id: str, asset_address: Optional[Address]) -> XcTx:
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


class UtxoOnlineDataProvider(OnlineDataProvider):
    @abc.abstractmethod
    async def get_confirmed_unspent_txs(self, address: str) -> List[UTXO]:
        ...

    @abc.abstractmethod
    async def get_unspent_txs(self, address: str) -> List[UTXO]:
        ...

    @abc.abstractmethod
    async def broadcast_tx(self, tx_hex: str) -> str:
        ...


UTXOOnlineDataProviders = Dict[NetworkType, UtxoOnlineDataProvider]

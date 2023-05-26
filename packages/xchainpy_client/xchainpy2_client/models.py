from datetime import datetime
from enum import Enum
from typing import Optional, List, NamedTuple, Dict

from xchainpy2_utils import Asset, Amount, NetworkType


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


class FeeWithRates(NamedTuple):
    fee: Fee
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

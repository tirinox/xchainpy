import abc
from datetime import datetime
from enum import Enum
from typing import Optional, List, NamedTuple, Dict

from xchainpy2_utils import Asset, Amount, NetworkType, CryptoAmount, DEFAULT_ASSET_DECIMAL


class TxType(Enum):
    TRANSFER = 'transfer'
    UNKNOWN = 'unknown'


class AssetInfo(NamedTuple):
    asset: Asset
    decimals: int = DEFAULT_ASSET_DECIMAL


class TokenTransfer(NamedTuple):
    from_address: str
    to_address: str
    amount: Amount
    asset: Optional[Asset] = None
    tx_hash: Optional[str] = None
    outbound: bool = True  # if true, it is a transfer out of the wallet, otherwise it is a transfer into the wallet
    # outbound = true corresponds TxTo of XChainJS
    # outbound = false corresponds TxFrom of XChainJS


class XcTx(NamedTuple):
    asset: Asset
    transfers: List[TokenTransfer]
    date: datetime
    type: TxType
    hash: str
    height: int
    memo: str = ''

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
    async def get_transactions(self, address: str,
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

import abc
from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import Optional, List, NamedTuple, Dict, Union

from xchainpy2_utils import Asset, Amount, NetworkType, CryptoAmount, DEFAULT_ASSET_DECIMAL


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


class FeeOption(Enum):
    AVERAGE = 'average'
    FAST = 'fast'
    FASTEST = 'fastest'

    _ETH_PRIORITY_FEE = 'max'
    _ETH_BASE_FEE = 'base'


FeeRates = Dict[FeeOption, float]


class FeeType(Enum):
    FLAT_FEE = 'base'
    PER_BYTE = 'byte'


Fee = Union[Amount, int, float, Decimal]
FeeRate = float  # satoshi per kilobyte in Bitcoin and other UTXO chains

INF_FEE = 1_000_000_000_000_000_000


class Fees(NamedTuple):
    type: FeeType
    fees: Dict[FeeOption, Fee]  # for EVM chains, the fee is in gwei

    @property
    def average(self):
        return self.fees[FeeOption.AVERAGE]

    @property
    def fast(self):
        return self.fees[FeeOption.FAST]

    @property
    def fastest(self):
        return self.fees[FeeOption.FASTEST]


class FeesWithRates(NamedTuple):
    fees: Fees
    rates: FeeRates


class FeeBounds(NamedTuple):
    lower: FeeRate  # satoshi per byte
    upper: FeeRate  # satoshi per byte

    def check_fee_bounds(self, fee_rate: FeeRate, per_kb: bool = False):
        """
        Check if the given fee rate is within the bounds
        :param fee_rate: fee rate to check, in satoshi per byte
        :param per_kb: if True, the fee rate is in satoshi per kilobyte. Otherwise, it is in satoshi per byte
        """
        if per_kb:
            fee_rate /= 1000

        if fee_rate < self.lower or fee_rate > self.upper:
            raise ValueError(f"Fee outside of predetermined bounds: {fee_rate}")

    @classmethod
    def infinite(cls):
        return FeeBounds(lower=0, upper=INF_FEE)


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

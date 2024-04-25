import time
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import NamedTuple, List, Dict, Optional, Set

from xchainpy2_midgard import PoolDetail, THORNameDetails
from xchainpy2_thorchain import THOR_BLOCK_TIME_SEC
from xchainpy2_thornode import Pool, LiquidityProviderSummary, Saver, QuoteFees, LastBlock, QuoteSwapResponse
from xchainpy2_utils import CryptoAmount, Amount, Asset, Chain, Address, DC


class QueryError(LookupError):
    pass


class Block(NamedTuple):
    current: int
    last_added: Optional[int]
    full_protection: int


class TotalFees(NamedTuple):
    asset: Asset
    outbound_fee: CryptoAmount
    affiliate_fee: CryptoAmount


class SwapEstimate(NamedTuple):
    total_fees: TotalFees
    slip_bps: int
    net_output: CryptoAmount
    inbound_confirmation_seconds: float
    outbound_delay_seconds: float
    can_swap: bool
    errors: List[str]
    recommended_min_amount_in: int
    streaming_swap_interval: int
    details: QuoteSwapResponse

    @property
    def memo(self):
        return self.details.memo

    @property
    def notes(self):
        return self.details.notes

    @property
    def is_less_than_price_limit(self):
        if self.errors:
            return any(
                'less than price limit' in e for e in self.errors
            )
        else:
            return False

    @property
    def streaming_swap_quantity(self) -> int:
        return self.details.max_streaming_quantity


def get_rune_balance_of_node_pool(pool: Pool) -> Amount:
    balance = getattr(pool, 'balance_rune', None)
    if balance is None:
        balance = getattr(pool, 'balance_cacao', None)
    return Amount.from_base(balance)


class LiquidityPool(NamedTuple):
    pool: Optional[PoolDetail]
    thornode_details: Optional[Pool]
    asset_balance: Amount
    rune_balance: Amount
    asset: Asset
    asset_string: str
    rune_to_asset_ratio: Decimal
    asset_to_rune_ratio: Decimal

    AVAILABLE = 'available'

    @classmethod
    def from_pool_details(cls, pool: PoolDetail, thornode_details: Pool):
        ab = Amount.from_base(pool.asset_depth)
        rb = Amount.from_base(pool.rune_depth)

        ab_dec = Decimal(pool.asset_depth, DC)
        rb_dec = Decimal(pool.rune_depth, DC)

        return cls(
            pool, thornode_details,
            asset_balance=ab,
            rune_balance=rb,
            asset=Asset.from_string(pool.asset),
            asset_string=pool.asset,
            rune_to_asset_ratio=rb_dec / ab_dec,
            asset_to_rune_ratio=ab_dec / rb_dec,
        )

    @classmethod
    def from_node_pool(cls, thornode_pool: Pool):
        rune_balance = get_rune_balance_of_node_pool(thornode_pool)
        asset_balance = Amount.from_base(thornode_pool.balance_asset)

        ab_dec = asset_balance.as_decimal
        rb_dec = rune_balance.as_decimal

        return cls(
            None, thornode_pool,
            asset_balance=asset_balance,
            rune_balance=rune_balance,
            asset=Asset.from_string(thornode_pool.asset),
            asset_string=thornode_pool.asset,
            rune_to_asset_ratio=rb_dec / ab_dec,
            asset_to_rune_ratio=ab_dec / rb_dec,
        )

    def is_available(self) -> bool:
        return self.pool.status.lower() == self.AVAILABLE


@dataclass
class PoolCache:
    last_refreshed: float
    pools: Dict[str, LiquidityPool]


@dataclass
class NameCache:
    address_to_name: Dict[str, Set[str]]
    name_details: Dict[str, THORNameDetails]
    name_last_refreshed: Dict[str, float]

    def put(self, name: str, n: Optional[THORNameDetails]):
        if n is None and name:
            self.name_details.pop(name, None)
            self.name_last_refreshed[name] = time.monotonic()
            return

        for entry in n.entries:
            self.address_to_name.setdefault(entry.address, set()).add(name)
        if name:
            self.name_details[name] = n
            self.name_last_refreshed[name] = time.monotonic()

    @staticmethod
    def is_expired(n: THORNameDetails, last_block_height: int):
        return int(n.expire) < last_block_height

    def invalidate(self, block_height: int):
        expired_names = [
            name for name, n in self.name_details.items() if self.is_expired(n, block_height)
        ]
        for name in expired_names:
            del self.name_details[name]
            del self.name_last_refreshed[name]

        for address, names in self.address_to_name.items():
            names.difference_update(expired_names)


@dataclass
class LastBlockCache:
    last_blocks: List[LastBlock]
    last_refreshed: float


class InboundDetail(NamedTuple):
    chain: Chain
    address: Address
    router: Optional[Address]
    gas_rate: int
    gas_rate_units: str
    outbound_tx_size: int
    outbound_fee: int
    halted_chain: bool
    halted_trading: bool
    halted_lp: bool
    dust_threshold: int


InboundDetails = Dict[str, InboundDetail]


@dataclass
class InboundDetailCache:
    last_refreshed: float
    inbound_details: InboundDetails


@dataclass
class NetworkValuesCache:
    last_refreshed: float
    network_values: Dict[str, int]


class UnitData(NamedTuple):
    liquidity_units: int
    total_units: int


class LPAmount(NamedTuple):
    rune: CryptoAmount
    asset: CryptoAmount

    @classmethod
    def zero(cls, asset: Asset = None) -> 'LPAmount':
        asset = asset or Asset.from_string('')
        return cls(CryptoAmount.zero(asset), CryptoAmount.zero(asset))


class PositionDepositValue(NamedTuple):
    rune: Amount
    asset: Amount


class LPAmountTotal(NamedTuple):
    rune: CryptoAmount
    asset: CryptoAmount
    total: CryptoAmount

    @classmethod
    def zero(cls, asset: Asset = None) -> 'LPAmountTotal':
        asset = asset or Asset.from_string('')
        return cls(CryptoAmount.zero(asset), CryptoAmount.zero(asset), CryptoAmount.zero(asset))


class ILProtectionData(NamedTuple):
    il_protection: Decimal
    total_days: float


class EstimateAddLP(NamedTuple):
    asset_pool: str
    slip_percent: float
    pool_share: LPAmount
    lp_units: int
    inbound_fees: LPAmountTotal
    rune_to_asset_ratio: int
    estimated_wait_seconds: int
    errors: List[str]
    can_add: bool
    recommended_min_amount_in: int


class WithdrawMode(Enum):
    RuneOnly = 'RuneOnly'
    AssetOnly = 'AssetOnly'
    Symmetric = 'Symmetric'


class EstimateWithdrawLP(NamedTuple):
    can_withdraw: bool
    deposit_amount: CryptoAmount
    asset_address: Optional[str]
    rune_address: Optional[str]
    slip_percent: float
    inbound_fee: LPAmountTotal
    inbound_min_to_send: LPAmountTotal
    outbound_fee: LPAmountTotal
    asset_amount: CryptoAmount
    rune_amount: CryptoAmount
    lp_growth: str
    impermanent_loss_protection: ILProtectionData
    estimated_wait_seconds: int
    asset_pool: str
    errors: List[str]
    memo: str
    inbound_address: str
    mode: WithdrawMode

    @classmethod
    def make_error(cls, error, mode):
        zero = CryptoAmount.zero(Asset.from_string(''))
        return cls(
            False, zero, None, None, 0,
            LPAmountTotal.zero(), LPAmountTotal.zero(), LPAmountTotal.zero(),
            zero, zero,
            '', ILProtectionData(Decimal(0), 0), 0, '', [error],
            '', '', mode
        )


class SaverFees(NamedTuple):
    affiliate: CryptoAmount
    asset: Asset
    outbound: CryptoAmount


class EstimateWithdrawSaver(NamedTuple):
    expected_asset_amount: CryptoAmount
    fee: SaverFees
    expiry: datetime
    to_address: Address
    memo: str
    estimated_wait_time: float
    slip_basis_points: float
    dust_amount: CryptoAmount
    errors: List[str]

    @property
    def can_withdraw(self):
        return not self.errors

    @classmethod
    def make_error(cls, errors, asset: Asset):
        return cls(
            CryptoAmount.zero(asset),
            SaverFees(CryptoAmount.zero(asset), asset, CryptoAmount.zero(asset)),
            datetime.now(), '', '', 0, 0,
            CryptoAmount.zero(asset),
            errors
        )


class WithdrawLiquidityPosition(NamedTuple):
    asset: Asset
    percentage: Decimal
    asset_address: Optional[str] = None
    rune_address: Optional[str] = None


class LiquidityPosition(NamedTuple):
    pool_share: LPAmount
    position: LiquidityProviderSummary
    lp_growth: str
    impermanent_loss_protection: ILProtectionData


class PoolRatios(NamedTuple):
    asset_to_rune: Decimal
    rune_to_asset: Decimal


class EstimateAddSaver(NamedTuple):
    can_add_saver: bool
    asset_amount: CryptoAmount
    estimated_deposit_value: CryptoAmount
    slip_basis_points: int
    fee: SaverFees
    expiry: datetime
    to_address: str
    memo: str
    saver_cap_filled_percent: float
    estimated_wait_time: int
    errors: List[str]
    recommended_min_amount_in: int

    @classmethod
    def make_error(cls, errors, asset: Asset):
        return cls(
            False,
            CryptoAmount.zero(asset), CryptoAmount.zero(asset), 0,
            SaverFees(CryptoAmount.zero(asset), asset, CryptoAmount.zero(asset)),
            datetime.now(), '', '', 0, 0, errors, 0
        )


class SaversPosition(NamedTuple):
    deposit_value: CryptoAmount
    redeemable_value: CryptoAmount
    last_add_height: int
    percentage_growth: float
    age_in_years: float
    age_in_days: float
    errors: List[str]
    outbound_fee: CryptoAmount


class SwapOutput(NamedTuple):
    output: CryptoAmount
    swap_fee: CryptoAmount
    slip: Decimal


class InboundStatus(Enum):
    Observed_Consensus = 'Observed_Consensus'
    Observed_Incomplete = 'Observed_Incomplete'
    Unknown = 'Unknown'


class SwapStatus(Enum):
    Complete = 'Complete'
    Complete_Refunded = 'Complete_Refunded'
    Complete_Below_Dust = 'Complete_Below_Dust'
    Incomplete = 'Incomplete'


class AddLpStatus(Enum):
    Complete = 'Complete'
    Complete_Refunded = 'Complete_Refunded'
    Complete_Below_Dust = 'Complete_Below_Dust'
    Incomplete = 'Incomplete'


class WithdrawStatus(Enum):
    Complete = 'Complete'
    Incomplete = 'Incomplete'
    Complete_Refunded = 'Complete_Refunded'


class RefundStatus(Enum):
    Complete = 'Complete'
    Incomplete = 'Incomplete'
    Complete_Refunded = 'Complete_Refunded'


class AddSaverStatus(Enum):
    Complete = 'Complete'
    Complete_Refunded = 'Complete_Refunded'
    Complete_Below_Dust = 'Complete_Below_Dust'
    Incomplete = 'Incomplete'


class SwapInfo(NamedTuple):
    status: SwapStatus
    to_address: str
    minimum_amount_out: CryptoAmount
    affliate_fee: CryptoAmount
    expected_out_block: int
    expected_out_date: datetime
    confirmations: int
    expected_amount_out: CryptoAmount
    actual_amount_out: Optional[CryptoAmount] = None


class InboundTx(NamedTuple):
    status: InboundStatus
    date: datetime
    block: int
    expected_confirmation_block: int
    expected_confirmation_date: datetime
    amount: CryptoAmount
    from_address: str
    memo: str


class AddLpInfo(NamedTuple):
    status: AddLpStatus
    is_symmetric: bool
    asset_tx: Optional[InboundTx] = None
    rune_tx: Optional[InboundTx] = None
    asset_confirmation_date: Optional[datetime] = None
    pool: Asset = None


class WithdrawInfo(NamedTuple):
    status: WithdrawStatus
    withdrawal_amount: CryptoAmount
    expected_confirmation_date: datetime
    thorchain_height: int
    outbound_height: int
    estimated_wait_time: int


class WithdrawSaverInfo(NamedTuple):
    status: WithdrawStatus
    withdrawal_amount: CryptoAmount
    expected_confirmation_date: datetime
    thorchain_height: int
    finalised_height: int
    outbound_block: int
    estimated_wait_time: float


class RefundInfo(NamedTuple):
    status: RefundStatus
    refund_amount: CryptoAmount
    to_address: str
    expected_confirmation_date: datetime
    finalised_height: int
    thorchain_height: int
    outbound_block: int
    estimated_wait_time: int


class AddSaverInfo(NamedTuple):
    status: AddSaverStatus
    asset_tx: Optional[InboundTx] = None
    saver_pos: Optional[Saver] = None


class BlockInformation(NamedTuple):
    inbound_confirmation_blocks: int = 0
    inbound_confirmation_seconds: float = 0.0
    outbound_delay_blocks: int = 0
    outbound_delay_seconds: float = 0.0


class LoanOpenQuote(NamedTuple):
    inbound_address: str
    expected_wait_time: BlockInformation
    fees: QuoteFees
    slippage_bps: int
    router: str
    expiry: int
    warning: str
    notes: str
    dust_threshold: int
    memo: str
    expected_amount_out: int
    expected_collateralization_ratio: float
    expected_collateral_up: int
    expected_debt_up: int
    errors: List[str]
    recommended_min_amount_in: int


class LoanCloseQuote(NamedTuple):
    inbound_address: str
    expected_wait_time: BlockInformation
    fees: QuoteFees
    slippage_bps: int
    router: str
    expiry: int
    warning: str
    notes: str
    dust_threshold: int
    memo: str
    expected_amount_out: int
    expected_collateral_down: int
    expected_debt_down: int
    errors: List[str]
    recommended_min_amount_in: int


class THORNameEstimate(NamedTuple):
    can_register: bool
    reason: str
    cost: CryptoAmount
    details: Optional[THORNameDetails] = None
    last_block_number: int = 0

    def expiry_block_from_date(self, expiry: datetime) -> int:
        return (expiry - datetime.now()).total_seconds() / THOR_BLOCK_TIME_SEC + self.last_block_number

    @classmethod
    def error(cls, reason: str, last_block_number: int) -> 'THORNameEstimate':
        return cls(False, reason, CryptoAmount.zero(Asset.from_string('')), None, last_block_number)

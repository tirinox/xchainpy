from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import NamedTuple, List, Dict, Optional

from xchainpy2_client import FeeOption
from xchainpy2_midgard import PoolDetail
from xchainpy2_thornode import Pool, LiquidityProviderSummary, Saver, QuoteFees
from xchainpy2_utils import CryptoAmount, Amount, Asset, Chain, Address, DC


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


InboundDetails = Dict[str, InboundDetail]


@dataclass
class InboundDetailCache:
    last_refreshed: float
    inbound_details: InboundDetails


@dataclass
class NetworkValuesCache:
    last_refreshed: float
    network_values: Dict[str, int]


class MidgardConfig(NamedTuple):
    api_retries: int
    midgard_base_urls: List[str]


class EstimateSwapParams(NamedTuple):
    input: CryptoAmount
    destination_asset: Asset
    destination_address: Address
    slip_limit: Optional[Decimal] = None
    affiliate_address: Optional[Address] = None
    affiliate_fee_basis_points: Optional[int] = None
    interface_id: Optional[str] = None
    fee_option: Optional[FeeOption] = None


class UnitData(NamedTuple):
    liquidity_units: int
    total_units: int


class LPAmount(NamedTuple):
    rune: CryptoAmount
    asset: CryptoAmount


class PostionDepositValue(NamedTuple):
    rune: Amount
    asset: Amount


class LPAmountTotal(NamedTuple):
    rune: CryptoAmount
    asset: CryptoAmount
    total: CryptoAmount


class Block(NamedTuple):
    current: int
    last_added: Optional[int]
    full_protection: int


class ILProtectionData(NamedTuple):
    il_protection: Decimal
    total_days: float


class ConstructMemo(NamedTuple):
    input_amount: CryptoAmount
    destination_asset: Asset
    limit: Amount
    destination_address: Address
    affiliate_address: Address
    affiliate_fee_basis_points: int
    fee_option: Optional[FeeOption] = None
    interface_id: str = ''


class TxDetails(NamedTuple):
    memo: str
    to_address: str
    expiry: datetime
    tx_estimate: SwapEstimate


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


class EstimateWithdrawLP(NamedTuple):
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


class GetSaver(NamedTuple):
    asset: Asset
    address: Address
    height: Optional[int] = None


class EstimateAddSaver(NamedTuple):
    asset_amount: CryptoAmount
    estimated_deposit_value: CryptoAmount
    slip_basis_points: int
    fee: SaverFees
    expiry: datetime
    to_address: str
    memo: str
    saver_cap_filled_percent: float
    estimated_wait_time: int
    can_add_saver: bool
    errors: List[str]
    recommended_min_amount_in: int


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


class TxType(Enum):
    Swap = 'Swap'
    AddLP = 'AddLP'
    WithdrawLP = 'WithdrawLP'
    AddSaver = 'AddSaver'
    WithdrawSaver = 'WithdrawSaver'
    Refund = 'Refund'
    Other = 'Other'
    Unknown = 'Unknown'


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


class TxProgress(NamedTuple):
    tx_type: TxType
    inbound_observed: Optional[InboundTx] = None
    swap_info: Optional[SwapInfo] = None
    add_lp_info: Optional[AddLpInfo] = None
    add_saver_info: Optional[AddSaverInfo] = None
    withdraw_lp_info: Optional[WithdrawInfo] = None
    withdraw_saver_info: Optional[WithdrawInfo] = None
    refund_info: Optional[RefundInfo] = None


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

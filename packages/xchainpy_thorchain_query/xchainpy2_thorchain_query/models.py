from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import NamedTuple, List, Dict, Optional

from xchainpy2_midgard import PoolDetail
from xchainpy2_thornode import Pool, LiquidityProviderSummary
from xchainpy2_utils import CryptoAmount, Amount, Asset, Chain, Address


class FeeOption(Enum):  # todo: move to it client package
    Average = 'average'
    Fast = 'fast'
    Fastest = 'fastest'


class TotalFees(NamedTuple):
    inbound_fee: CryptoAmount
    swap_fee: CryptoAmount
    outbound_fee: CryptoAmount
    affiliate_fee: CryptoAmount


class SwapEstimate(NamedTuple):
    total_fees: TotalFees
    slip_percentage: float
    net_output: CryptoAmount
    wait_time_seconds: int
    can_swap: bool
    errors: List[str]


class LiquidityPool(NamedTuple):
    pool: PoolDetail
    thornode_details: Pool
    asset_balance: Amount
    rune_balance: Amount
    asset: Asset
    asset_string: str
    rune_to_asset_ratio: float
    asset_to_rune_ratio: float

    AVAILABLE = 'available'

    @classmethod
    def from_pool_details(cls, pool: PoolDetail, thornode_details: Pool):
        ab = Amount.from_base(pool.asset_depth)
        rb = Amount.from_base(pool.asset_depth)
        return cls(
            pool, thornode_details,
            asset_balance=ab,
            rune_balance=rb,
            asset=Asset.from_string(pool.asset),
            asset_string=pool.asset,
            rune_to_asset_ratio=int(rb) / int(ab),
            asset_to_rune_ratio=int(ab) / int(rb)
        )

    def is_available(self) -> bool:
        return self.pool.status.lower() == self.AVAILABLE


@dataclass
class PoolCache:
    last_refreshed: int
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


@dataclass
class InboundDetailCache:
    last_refreshed: int
    inbound_details: Dict[str, InboundDetail]


@dataclass
class NetworkValuesCache:
    last_refreshed: int
    network_values: Dict[str, float]


class MidgardConfig(NamedTuple):
    api_retries: int
    midgard_base_urls: List[str]


class EstimateSwapParams(NamedTuple):
    input: CryptoAmount
    destination_asset: Asset
    destination_address: Address
    slip_limit: Optional[float] = None
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


class LPAmountTotal(NamedTuple):
    rune: CryptoAmount
    asset: CryptoAmount
    total: CryptoAmount


class Block(NamedTuple):
    current: int
    last_added: Optional[int]
    full_protection: int


class ILProtectionData(NamedTuple):
    il_protection: float
    total_days: int


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
    slip_percent: int
    pool_share: LPAmount
    lp_units: int
    inbound_fees: LPAmount
    rune_to_asset_ratio: int
    estimated_wait_seconds: int
    errors: List[str]
    can_add: bool


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


class WithdrawLiquidityPosition(NamedTuple):
    asset: Asset
    percentage: float
    asset_address: Optional[str] = None
    rune_address: Optional[str] = None


class LiquidityPosition(NamedTuple):
    pool_share: LPAmount
    position: LiquidityProviderSummary
    lp_growth: str
    impermanent_loss_protection: ILProtectionData


class PoolRatios(NamedTuple):
    asset_to_rune: float
    rune_to_asset: float


class GetSaver(NamedTuple):
    asset: Asset
    address: Address
    height: Optional[int] = None


class SaverFees(NamedTuple):
    affiliate: CryptoAmount
    asset: Asset
    outbound: CryptoAmount


class EstimateAddSaver(NamedTuple):
    asset_amount: CryptoAmount
    estimated_deposit_value: CryptoAmount
    slip_basis_points: int
    fee: SaverFees
    expiry: datetime
    to_address: str
    memo: str
    saver_cap_filled_percent: int
    estimated_wait_time: int
    can_add_saver: bool
    errors: List[str]


class SaversPosition(NamedTuple):
    deposit_value: CryptoAmount
    redeemable_value: CryptoAmount
    last_add_height: int
    percentage_growth: float
    age_in_years: float
    age_in_days: float


class SaversWithdraw(NamedTuple):
    height: int
    asset: str
    address: str
    withdraw_bps: int
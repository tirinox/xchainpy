import time
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import NamedTuple, List, Dict, Optional, Set

from xchainpy2_midgard import PoolDetail, THORNameDetails
from xchainpy2_thorchain import THOR_BLOCK_TIME_SEC
from xchainpy2_thornode import Pool, LiquidityProviderSummary, QuoteFees, LastBlock, QuoteSwapResponse, \
    QuoteSaverWithdrawResponse
from xchainpy2_utils import CryptoAmount, Amount, Asset, Chain, Address, DC


class QueryError(LookupError):
    """
    Query error is raised when the module fails to query the data from THORChain.
    """
    pass


class TotalFees(NamedTuple):
    """
    A named tuple representing the total fees for a swap transaction including outbound and affiliate fees.
    """

    asset: Asset
    """Destination asset"""

    total_bps: int
    """Total basis points for the fees"""

    total_fee: int
    """Total fee in the destination asset"""

    slippage_bps: int
    """Slippage in basis points (0-10000)"""

    affiliate_fee: int
    """Affiliate fee in the destination asset"""

    liquidity_fee: int
    """Liquidity fee in the destination asset"""

    outbound_fee: int
    """Outbound fee in the destination asset"""

    @property
    def total_fee_amount(self) -> CryptoAmount:
        return CryptoAmount(Amount.from_base(self.total_fee), self.asset)

    @property
    def affiliate_fee_amount(self) -> CryptoAmount:
        return CryptoAmount(Amount.from_base(self.affiliate_fee), self.asset)

    @property
    def liquidity_fee_amount(self) -> CryptoAmount:
        return CryptoAmount(Amount.from_base(self.liquidity_fee), self.asset)

    @property
    def outbound_fee_amount(self) -> CryptoAmount:
        return CryptoAmount(Amount.from_base(self.outbound_fee), self.asset)

    @classmethod
    def zero(cls, asset: Asset) -> 'TotalFees':
        """
        Create a zero TotalFees instance.

        :param asset: Destination asset
        :return: TotalFees instance
        """
        return cls(asset, 0, 0, 0, 0, 0, 0)


class SwapEstimate(NamedTuple):
    """
    A named tuple representing an estimate for a swap transaction.
    """

    total_fees: TotalFees
    """Total fees that will be charged for the swap"""
    slip_bps: int
    """Slippage in basis points (0-10000)"""
    net_output: CryptoAmount
    """Net output amount after fees and slippage"""
    inbound_confirmation_seconds: float
    """Estimated time in seconds for the inbound transaction to be confirmed"""
    outbound_delay_seconds: float
    """Estimated time in seconds for the outbound transaction to be delayed"""
    can_swap: bool
    """Whether the swap can be executed"""
    errors: List[str]
    """List of errors, if any (in case the swap cannot be executed)"""
    recommended_min_amount_in: int
    """Recommended minimum amount to send in the swap"""
    streaming_swap_interval: int
    """Recommended interval for streaming swaps in blocks"""
    details: QuoteSwapResponse
    """Original details of the swap estimate that was returned by THORChain API"""

    @property
    def memo(self):
        return self.details.memo

    memo.__doc__ = QuoteSwapResponse.memo.__doc__

    @property
    def notes(self):
        return self.details.notes

    notes.__doc__ = QuoteSwapResponse.notes.__doc__

    @property
    def is_less_than_price_limit(self):
        """
        Check if the swap is less than the price limit. Does search for the error message in the errors list.
        :return: True if the swap is less than the price limit, False otherwise
        :rtype: bool
        """
        if self.errors:
            return any(
                'less than price limit' in e for e in self.errors
            )
        else:
            return False

    @property
    def streaming_swap_max_quantity(self) -> int:
        """
        Get the maximum amount of trades a streaming swap can do for a trade
        """
        return self.details.max_streaming_quantity


def get_rune_balance_of_node_pool(pool: Pool) -> Amount:
    """
    Helper function to get the rune/cacao balance of a pool. Just unification of the rune/cacao balance attribute.

    :param pool: Pool object
    :return: Amount of rune/cacao in the pool
    """
    balance = getattr(pool, 'balance_rune', None)
    if balance is None:
        balance = getattr(pool, 'balance_cacao', None)
    return Amount.from_base(balance)


class LiquidityPool(NamedTuple):
    """
    Compound Names Tuple class representing a liquidity pool in THORChain.
    It includes the pool details taken from the Midgard API and THORNode API
    """

    # todo: get rid of duplicate fields, make them properties

    pool: Optional[PoolDetail]
    """Pool details from Midgard API"""
    thornode_details: Optional[Pool]
    """Pool details from THORNode API"""
    asset_balance: Amount
    """Amount of asset in the pool"""
    rune_balance: Amount
    """Amount of Rune/Cacao in the pool"""
    asset: Asset
    """Collateral asset of the pool"""
    asset_string: str
    """Collateral asset as a string"""
    rune_to_asset_ratio: Decimal
    """Rune to asset ratio; asset price in Runes"""
    asset_to_rune_ratio: Decimal
    """Asset to rune ratio; Rune price in asset units"""

    AVAILABLE = 'available'
    """Pool status: available"""

    @classmethod
    def from_pool_details(cls, pool: PoolDetail, thornode_details: Pool):
        """
        Create a LiquidityPool instance from pool details from Midgard API and THORNode API.

        :param pool: Midgard pool details
        :param thornode_details: THORNode pool details
        :return: a new LiquidityPool instance
        :rtype: LiquidityPool
        """

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
        """
        Create a LiquidityPool instance from THORNode pool details only.

        :param thornode_pool: THORNode pool details
        :type thornode_pool: Pool
        :return: a new LiquidityPool instance
        :rtype: LiquidityPool
        """
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
        """
        Check if the pool is in available status.

        :return: True if the pool is available, False otherwise
        :rtype: bool
        """
        return self.pool.status.lower() == self.AVAILABLE


@dataclass
class PoolCache:
    """
    A dataclass representing a cache of liquidity pools.
    """

    last_refreshed: float
    """Timestamp of the last refresh"""
    pools: Dict[str, LiquidityPool]
    """Mapping of liquidity pools by pool asset string"""


@dataclass
class NameCache:
    """
    A dataclass representing a cache of THORNames.
    """

    address_to_name: Dict[str, Set[str]]
    """Mapping of addresses to names"""
    name_details: Dict[str, THORNameDetails]
    """Mapping of names to name details"""
    name_last_refreshed: Dict[str, float]
    """Timestamp of the last refresh for each name"""

    def put(self, name: str, n: Optional[THORNameDetails]):
        """
        Put a THORNameDetails object into the cache.

        :param name: Name of the THORName
        :type name: str
        :param n: THORNameDetails object, None if the name is to be removed from the cache
        :type n: Optional[THORNameDetails]
        :return: None
        """
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
        """
        Check if a THORNameDetails object is expired.

        :param n: THORName details
        :type n: THORNameDetails
        :param last_block_height: Last block height to compare the expiry with
        :type last_block_height: int
        :return: True if the THORNameDetails object is expired, False otherwise
        :rtype: bool
        """
        return int(n.expire) < last_block_height

    def invalidate(self, block_height: int):
        """
        Invalidate expired THORNameDetails at the given block height.

        :param block_height: Block height to compare the expiry with
        :return: None
        """
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
    """
    A dataclass representing a cache of last blocks of THORChain and connected chains.
    """

    last_blocks: List[LastBlock]
    """List of last blocks"""
    last_refreshed: float
    """Timestamp of the last refresh"""


class InboundDetail(NamedTuple):
    """
    A named tuple representing the inbound details for a chain. It includes the chain, Asgard address,
    router, gas rate and other helpful information.
    See: https://thornode.ninerealms.com/thorchain/inbound_addresses
    """

    chain: Chain
    """Chain"""
    address: Address
    """Address of the vault"""
    router: Optional[Address]
    """Router address for EVM chains"""
    gas_rate: int
    """Gas rate"""
    gas_rate_units: str
    """Gas rate units: gwei, satsperbyte, etc."""
    outbound_tx_size: int
    """Outbound transaction size"""
    outbound_fee: int
    """Outbound fee"""
    halted_chain: bool
    """Whether the chain is halted"""
    halted_trading: bool
    """Whether trading is halted"""
    halted_lp: bool
    """Whether liquidity operations is halted"""
    dust_threshold: int
    """Dust threshold, do not send amounts below this value"""


InboundDetails = Dict[str, InboundDetail]
"""Mapping of chain names to inbound details"""


@dataclass
class InboundDetailCache:
    """
    A dataclass representing a cache of inbound details for chains.
    """

    last_refreshed: float
    """Timestamp of the last refresh"""
    inbound_details: InboundDetails
    """Mapping of chain names to inbound details"""


@dataclass
class NetworkValuesCache:
    """
    A dataclass representing a cache of network values (constants, Mimir) for THORChain.
    """

    last_refreshed: float
    """Timestamp of the last refresh"""
    network_values: Dict[str, int]
    """Mapping of network values"""


class UnitData(NamedTuple):
    """
    A named tuple representing the data of a unit of liquidity.
    """
    liquidity_units: int
    """Liquidity units"""
    total_units: int
    """Total units of pool"""


class LPAmount(NamedTuple):
    """
    A named tuple representing the amount of liquidity in a pool.
    """

    # todo: merge with LPAmountTotal
    rune: CryptoAmount
    """Rune amount"""
    asset: CryptoAmount
    """Asset amount"""

    @classmethod
    def zero(cls, asset: Asset = None) -> 'LPAmount':
        """
        Create a zero LPAmount instance.

        :param asset: Asset
        :return: LPAmount instance
        :rtype: LPAmount
        """
        asset = asset or Asset.from_string('')
        return cls(CryptoAmount.zero(asset), CryptoAmount.zero(asset))


class LPAmountTotal(NamedTuple):
    """
    A named tuple representing the total amount of liquidity in a pool.
    """

    rune: CryptoAmount
    """Rune amount"""
    asset: CryptoAmount
    """Asset amount"""
    total: CryptoAmount
    """Total amount in Rune"""

    @classmethod
    def zero(cls, asset: Asset = None) -> 'LPAmountTotal':
        """
        Create a zero LPAmountTotal instance.

        :param asset: Asset
        :return:
        :rtype: LPAmountTotal
        """
        asset = asset or Asset.from_string('')
        return cls(CryptoAmount.zero(asset), CryptoAmount.zero(asset), CryptoAmount.zero(asset))


class EstimateAddLP(NamedTuple):
    """
    A named tuple representing an estimate for adding liquidity to a pool.
    """

    asset_pool: str
    """Pool name"""
    slip_percent: float
    """Slippage percentage"""
    pool_share: LPAmount
    """Pool share"""
    lp_units: int
    """Liquidity units"""
    inbound_fees: LPAmountTotal
    """Inbound fees"""
    rune_to_asset_ratio: int
    """Rune to asset ratio"""
    estimated_wait_seconds: int
    """Estimated wait time in seconds"""
    errors: List[str]
    """List of errors, if any"""
    can_add: bool
    """Whether the liquidity can be added"""
    recommended_min_amount_in: int
    """Recommended minimum amount to send in the transaction"""


class WithdrawMode(Enum):
    """
    An enumeration representing the mode of withdrawal.
    """

    RuneOnly = 'RuneOnly'
    """Withdraw only Rune"""
    AssetOnly = 'AssetOnly'
    """Withdraw only Asset"""
    Symmetric = 'Symmetric'
    """Both Rune and Asset"""


class EstimateWithdrawLP(NamedTuple):
    """
    A named tuple representing an estimate for withdrawing liquidity from a pool.
    """
    can_withdraw: bool
    """Whether the liquidity can be withdrawn"""
    deposit_amount: CryptoAmount
    """Deposit amount"""
    asset_address: Optional[str]
    """Asset address"""
    rune_address: Optional[str]
    """Rune address"""
    slip_percent: float
    """Slippage percentage"""
    inbound_fee: LPAmountTotal
    """Inbound fee"""
    inbound_min_to_send: LPAmountTotal
    """Minimum amount to send"""
    outbound_fee: LPAmountTotal
    """Outbound fee"""
    asset_amount: CryptoAmount
    """Asset amount"""
    rune_amount: CryptoAmount
    """Rune amount"""
    lp_growth: str
    """LP growth"""
    estimated_wait_seconds: int
    """Estimated wait time in seconds"""
    asset_pool: str
    """Pool name"""
    errors: List[str]
    """List of errors, if any"""
    memo: str
    """Memo"""
    inbound_address: str
    """Inbound address"""
    mode: WithdrawMode

    @classmethod
    def make_error(cls, error, mode):
        zero = CryptoAmount.zero(Asset.from_string(''))
        return cls(
            False, zero, None, None, 0,
            LPAmountTotal.zero(), LPAmountTotal.zero(), LPAmountTotal.zero(),
            zero, zero,
            '', 0, '', [error],
            '', '', mode
        )


class SaverFees(NamedTuple):
    affiliate: CryptoAmount
    asset: Asset
    outbound: CryptoAmount


class EstimateWithdrawSaver(NamedTuple):
    """
    A named tuple representing an estimate for withdrawing liquidity from the savers vault.
    """

    expected_asset_amount: CryptoAmount
    """Expected asset amount that will be withdrawn to the user after applying fees and slippage"""

    fee: SaverFees
    """Fees for the withdrawal"""

    expiry: datetime
    """Expiry date of the withdrawal request"""

    to_address: Address
    """Address to send the withdraw request to"""

    memo: str
    """Memo string that is supposed to be sent along with the transaction to perform the withdrawal"""
    estimated_wait_time: float
    """Estimated wait time in seconds"""

    slip_basis_points: float
    """Slippage in basis points 0..10000 paid for internal swaps"""

    dust_amount: CryptoAmount
    """Dust amount, any amount below this value will be considered dust and ignored"""

    errors: List[str]
    """List of errors, if any"""

    details: Optional[QuoteSaverWithdrawResponse] = None
    """QuoteSaverWithdrawResponse received from THORChain API, may contain additional details"""

    @property
    def can_withdraw(self):
        """
        If there are no errors, the withdrawal can be made.
        :return: bool
        """
        return not self.errors

    @classmethod
    def make_error(cls, errors, asset: Asset, details=None):
        """
        Create an EstimateWithdrawSaver instance with errors list.

        :param errors: List of errors
        :param asset: Asset to withdraw
        :return: EstimateWithdrawSaver
        """
        return cls(
            CryptoAmount.zero(asset),
            SaverFees(CryptoAmount.zero(asset), asset, CryptoAmount.zero(asset)),
            datetime.now(), '', '', 0, 0,
            CryptoAmount.zero(asset),
            errors,
            details=details,
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
    """
    A named tuple representing the position of a saver in the savers vault.
    """

    deposit_value: CryptoAmount
    """Deposit value"""

    redeemable_value: CryptoAmount
    """Current redeemable value"""

    last_add_height: int
    """Last add height (THORChain blocks)"""

    saver_growth: float
    """Saver growth (percentage)"""

    errors: List[str]
    """List of errors, if any"""


class SwapOutput(NamedTuple):
    """
    A named tuple representing the output of a swap transaction.
    """
    output: CryptoAmount
    """Output amount and asset"""
    swap_fee: CryptoAmount
    """Swap fee amount"""
    slip: Decimal
    """Slippage 0..1"""


class BlockInformation(NamedTuple):
    """
    A named tuple representing inbound/outbound TX delay in blocks and seconds.
    """

    inbound_confirmation_blocks: int = 0
    """Inbound confirmation blocks"""
    inbound_confirmation_seconds: float = 0.0
    """Inbound confirmation seconds"""
    outbound_delay_blocks: int = 0
    """Outbound delay blocks"""
    outbound_delay_seconds: float = 0.0
    """Outbound delay seconds"""


class LoanOpenQuote(NamedTuple):
    """
    A named tuple representing a quote for opening a loan.
    """

    inbound_address: str
    """Vault's address to send your collateral to"""
    expected_wait_time: BlockInformation
    """Expected wait time for the transaction to be confirmed"""
    fees: QuoteFees
    """Fees for the transaction"""
    slippage_bps: int
    """Slippage in basis points"""
    router: str
    """Router address (for EVM chains)"""
    expiry: int
    """Expiry block number"""
    warning: str
    """Warning message"""
    notes: str
    """Notes and instructions"""
    dust_threshold: int
    """Dust threshold"""
    memo: str
    """Prepared memo for the transaction"""
    expected_amount_out: int
    """Expected amount out"""
    expected_collateralization_ratio: float
    """Expected collateralization ratio"""
    expected_collateral_up: int
    """Expected collateral up"""
    expected_debt_up: int
    """Expected debt up"""
    errors: List[str]
    """List of errors, if any"""
    recommended_min_amount_in: int
    """Recommended minimum amount to send in the transaction"""

    @classmethod
    def empty_with_errors(cls, errors):
        """
        Create an empty LoanOpenQuote instance with errors list.

        :param errors: List of errors
        :return: LoanOpenQuote
        """
        return cls(
            inbound_address='',
            expected_wait_time=BlockInformation(),
            fees=QuoteFees(),
            slippage_bps=-1,
            router='',
            expiry=-1,
            warning='',
            notes='',
            dust_threshold=0,
            memo='',
            expected_amount_out=0,
            expected_debt_up=0,
            expected_collateral_up=0,
            expected_collateralization_ratio=0,
            errors=errors,
            recommended_min_amount_in=0,
        )


class LoanCloseQuote(NamedTuple):
    """
    A named tuple representing a quote for closing a loan.
    """

    inbound_address: str
    """Inbound address to repay the loan"""
    expected_wait_time: BlockInformation
    """Expected wait time for the transaction to be confirmed"""
    fees: QuoteFees
    """Fees for the transaction"""
    slippage_bps: int
    """Slippage in basis points"""
    router: str
    """Router address (for EVM chains)"""
    expiry: int
    """Expiry block number"""
    warning: str
    """Warning message"""
    notes: str
    """Notes and instructions"""
    dust_threshold: int
    """Dust threshold"""
    memo: str
    """Prepared memo for the transaction"""
    expected_amount_out: int
    """Expected amount out"""
    expected_collateral_down: int
    """Expected collateral down"""
    expected_debt_down: int
    """Expected debt down"""
    errors: List[str]
    """List of errors, if any"""
    recommended_min_amount_in: int
    """Recommended minimum amount to send in the transaction"""

    @classmethod
    def empty_with_errors(cls, errors):
        """
        Create an empty LoanCloseQuote instance with errors list.

        :param errors: List of errors
        :return: LoanCloseQuote
        """
        return cls(
            inbound_address='',
            expected_wait_time=BlockInformation(),
            fees=QuoteFees(),
            slippage_bps=-1,
            router='',
            expiry=-1,
            warning='',
            notes='',
            dust_threshold=0,
            memo='',
            expected_amount_out=0,
            expected_collateral_down=0,
            expected_debt_down=0,
            errors=errors,
            recommended_min_amount_in=0,
        )


class THORNameEstimate(NamedTuple):
    """
    A named tuple representing a result of simulating a THORName registration. If successful, the `can_register` field
    will be `True` and the `cost` field will contain the estimated cost of the registration. If the registration is not
    possible, the `can_register` field will be `False` and the `reason` field will contain the reason why the
    registration is not possible.
    """
    can_register: bool
    """Whether the registration is possible"""
    reason: str
    """The reason why the registration is not possible"""
    cost: CryptoAmount
    """The estimated cost of the registration"""
    details: Optional[THORNameDetails] = None
    """The details of the registration, if successful"""
    last_block_number: int = 0
    """The last block number when the estimate was made"""

    def expiry_block_from_date(self, expiry: datetime) -> int:
        """
        Calculate the block number at which the registration will expire.

        :param expiry: The expiry date of the registration
        :type expiry: datetime
        :return: block number at which the registration will expire
        :rtype: int
        """
        return (expiry - datetime.now()).total_seconds() / THOR_BLOCK_TIME_SEC + self.last_block_number

    @classmethod
    def error(cls, reason: str, last_block_number: int) -> 'THORNameEstimate':
        """
        Create a THORNameEstimate instance representing an error.

        :param reason: Reason for the error
        :param last_block_number: Block number when the estimate was made
        :return: THORNameEstimate
        """
        return cls(False, reason, CryptoAmount.zero(Asset.from_string('')), None, last_block_number)

import asyncio
import json
import math
from datetime import datetime
from typing import Union, Optional, Tuple

from xchainpy2_client import XChainClient
from xchainpy2_thorchain import THORMemo, THOR_BASIS_POINT_MAX
from xchainpy2_thornode import QuoteSwapResponse, QueueResponse, QuoteFees, \
    TxStatusResponse, TxSignersResponse
from xchainpy2_utils import DEFAULT_CHAIN_ATTRS, CryptoAmount, Asset, RUNE_DECIMAL, Amount, Chain, AssetRUNE, \
    get_chain_gas_asset, NetworkType
from .cache import THORChainCache
from .const import DEFAULT_INTERFACE_ID, Mimir, THORNAME_BLOCKS_ONE_YEAR
from .fee import calc_network_fee, calc_outbound_fee
from .liquidity import get_liquidity_units, get_pool_share, get_slip_on_liquidity
from .midgard import MidgardAPIClient, ConfigurationEx
from .models import SwapEstimate, TotalFees, LPAmount, EstimateAddLP, UnitData, LPAmountTotal, \
    LiquidityPosition, PoolRatios, EstimateWithdrawLP, \
    THORNameEstimate, WithdrawMode, InboundDetail
from .swap import get_base_amount_with_diff_decimals
from .thornode import THORNodeAPIClient
from .track.tracker import TransactionTracker


class THORChainQuery:
    """
    THORChain Query Class is designed to query THORChain data and provide estimates for transactions.
    It also supports caching of data through THORChainCache to reduce the number of API calls.
    """

    def __init__(self,
                 cache: THORChainCache = None,
                 chain_attributes=None,
                 interface_id=DEFAULT_INTERFACE_ID,
                 native_decimal=RUNE_DECIMAL):
        """
        Initialize THORChain Query.

        :param cache: THORChainCache instance. If not provided, a new instance will be created.
        :param chain_attributes: Dictionary of chain attributes. Default is DEFAULT_CHAIN_ATTRS.
        :param interface_id: You need this field to mark your identifier for public APIs, and avoid blocking requests
        from unknown sources. Default is DEFAULT_INTERFACE_ID.
        :param native_decimal: Decimal places for the native asset, e.g. RUNE. Default is RUNE_DECIMAL.
        """

        if not cache:
            cache = THORChainCache()

        self.cache = cache
        self.chain_attributes = chain_attributes or DEFAULT_CHAIN_ATTRS
        self.interface_id = interface_id
        self.native_decimal = native_decimal

        # todo: write some tests
        self.cache.thornode_client.patch_client(self.interface_id, self.interface_id)
        self.cache.midgard_client.patch_client(self.interface_id, self.interface_id)

    @classmethod
    def from_thornode_and_midgard(
            cls,
            thornode_url='', midgard_url='',
            chain_attributes=None,
            interface_id=DEFAULT_INTERFACE_ID,
            native_decimal=RUNE_DECIMAL,
            network: NetworkType = NetworkType.MAINNET
    ):
        """
        Create a THORChainQuery instance using custom Thornode and Midgard URLs.

        :param thornode_url: URL for Thornode API (with port and protocol)
        :param midgard_url: URL for Midgard API (with port and protocol)
        :param native_decimal: Native asset decimal places (e.g. RUNE has 8 decimals)
        :param interface_id: Interface ID for the API client. This is used to identify your requests and avoid blocking.
        :param chain_attributes: Dict of chain attributes for the query. Default is DEFAULT_CHAIN_ATTRS.
        :param network: Network type (Mainnet, Stagenet, Testnet). Default is MAINNET.

        :return: THORChainQuery instance
        """
        if not isinstance(network, NetworkType):
            network = NetworkType(network)

        midgard = MidgardAPIClient(ConfigurationEx.new(host=midgard_url)) if midgard_url else MidgardAPIClient()
        thornode = THORNodeAPIClient(ConfigurationEx.new(host=thornode_url)) if thornode_url else THORNodeAPIClient()
        cache = THORChainCache(midgard, thornode, network=network)
        return cls(
            cache=cache,
            interface_id=interface_id,
            chain_attributes=chain_attributes or DEFAULT_CHAIN_ATTRS,
            native_decimal=native_decimal
        )

    @property
    def native_chain_attributes(self):
        """
        Returns the chain attributes for the native chain (e.g. THORChain)

        :return: ChainAttributes
        """
        return self.chain_attributes[self.native_asset.chain]

    @property
    def native_asset(self):
        """
        Returns the native asset (e.g. AssetRUNE or AssetCACAO).

        :return: Asset
        """
        return self.cache.native_asset

    @property
    def native_block_time(self) -> float:
        """
        Returns the average block time for the native chain.

        :return: block time in seconds
        :rtype: float
        """
        return self.chain_attributes[Chain(self.native_asset.chain)].avg_block_time

    @staticmethod
    def abbreviate_asset_string(asset: Asset, max_length=5) -> str:
        """
        Helper method to abbreviate an asset string if it is too long.

        :param asset: Asset to abbreviate
        :param max_length: Maximum length of the asset string, default is 5
        :return: Abbreviated asset string
        :rtype: str
        """

        if asset.contract and len(asset.contract) > max_length:
            abbrev = asset.contract[:max_length]
            asset = asset._replace(contract=abbrev)
        return str(asset)

    async def close(self):
        """
        Close the THORChain Query instance and the cache.
        """
        await self.cache.close()

    async def get_tx_details(self, tx_id: str) -> TxSignersResponse:
        """
        Get transaction details and status from the protocol API. See TxSignersResponse for more details.

        :param tx_id: Transaction hash (inbound)
        :return: TxSignersResponse
        """
        return await self.cache.tx_api.tx_signers(tx_id)

    async def get_tx_status(self, tx_id: str) -> TxStatusResponse:
        """
        Get transaction status and stages from the protocol API. See TxStatusResponse for more details.

        :param tx_id: Transaction hash (inbound)
        :return: TxStatusResponse
        """
        return await self.cache.tx_api.tx_status(tx_id)

    @staticmethod
    def _prepare_args_of_quote_call(**kwargs):
        # filter out empty values from kwargs
        kwargs = {key: value for key, value in kwargs.items() if value}

        affiliate_address = kwargs.get('affiliate')
        affiliate_bps = kwargs.get('affiliate_bps')

        if not affiliate_address and affiliate_bps:
            raise ValueError('Affiliate address is required if affiliate basis points are set')

        if affiliate_address and not affiliate_bps:
            kwargs['affiliate_bps'] = 0  # explicitly set to keep track of affiliate address

        return kwargs

    async def quote_swap(self,
                         input_amount: CryptoAmount,
                         destination_address: str,
                         destination_asset: Union[Asset, str],
                         tolerance_bps: int = 0,
                         affiliate_bps=0,
                         affiliate_address='',
                         streaming_interval=0,
                         streaming_quantity=0,
                         height=0,
                         ) -> SwapEstimate:
        """
        Quote a swap transaction. This is a read-only method and does not send any transactions.

        :param input_amount: CryptoAmount - amount to swap
        :param destination_address: Destination address to receive the swapped asset
        :param destination_asset: Destination asset to swap to
        :param tolerance_bps: Basis points of slippage tolerance (0..10000)
        :param affiliate_bps: Affiliate basis points (0..10000)
        :param affiliate_address: Affiliate address
        :param streaming_interval: Streaming swap interval in blocks
        :param streaming_quantity: Streaming swap quantity
        :param height: Height to query (optional), 0 for latest
        :return: Swap estimate
        :rtype: SwapEstimate
        """
        errors = []
        from_asset = str(input_amount.asset) if isinstance(input_amount.asset, Asset) else input_amount.asset
        destination_asset = str(destination_asset) if isinstance(destination_asset, Asset) else destination_asset
        input_amount_int = get_base_amount_with_diff_decimals(input_amount.amount, self.native_decimal)
        input_amount_int = int(input_amount_int)

        try:
            kwargs = self._prepare_args_of_quote_call(
                height=height,
                from_asset=from_asset,
                to_asset=destination_asset,
                amount=input_amount_int,
                destination=destination_address,
                tolerance_bps=tolerance_bps,
                affiliate_bps=affiliate_bps,
                affiliate=affiliate_address,
                streaming_interval=streaming_interval,
                streaming_quantity=streaming_quantity,
            )

            swap_quote: QuoteSwapResponse
            swap_quote = await self.cache.quote_api.quoteswap(**kwargs)

        except ValueError:
            error, response = self._get_error_and_response_from_last_thor_response()
            if error:
                errors.append(error)

            zero = CryptoAmount(Amount.zero(), AssetRUNE)
            # noinspection PyTypeChecker
            return SwapEstimate(
                TotalFees.zero(destination_asset),
                0,
                zero,
                0, 0,
                can_swap=False,
                errors=errors,
                recommended_min_amount_in=0,
                streaming_swap_interval=0,
                details=response,
            )

        if (int(swap_quote.recommended_min_amount_in) and
                int(input_amount_int) < int(swap_quote.recommended_min_amount_in)):
            recommended_in = CryptoAmount.automatic(int(swap_quote.recommended_min_amount_in), input_amount.asset,
                                                    decimals=self.native_decimal)
            errors.append(f'Input amount {input_amount} is less than recommended min amount in '
                          f'{recommended_in}')

        fee_asset = Asset.from_string_exc(swap_quote.fees.asset)

        fees: QuoteFees = swap_quote.fees
        return SwapEstimate(
            TotalFees(
                fee_asset,
                fees.total_bps, int(fees.total), fees.slippage_bps, int(fees.affiliate), int(fees.liquidity),
                int(fees.outbound),
            ),
            slip_bps=int(swap_quote.fees.slippage_bps),
            net_output=CryptoAmount(Amount(int(swap_quote.expected_amount_out)), destination_asset),
            outbound_delay_seconds=swap_quote.outbound_delay_seconds,
            inbound_confirmation_seconds=swap_quote.inbound_confirmation_seconds,
            can_swap=not bool(errors),
            errors=errors,
            recommended_min_amount_in=int(swap_quote.recommended_min_amount_in),
            streaming_swap_interval=streaming_interval,
            details=swap_quote,
        )

    # alias for quote_swap
    estimate_swap = quote_swap
    estimate_swap.__doc__ = quote_swap.__doc__

    async def outbound_delay(self, outbound_amount: CryptoAmount) -> float:
        """
        Works out how long an outbound Tx will be held by THORChain before sending.
        See https://gitlab.com/thorchain/thornode/-/blob/develop/x/thorchain/manager_txout_current.go#L548
        This function does not guarantee the exact delay.
        Please use quote_swap for a more accurate estimate.

        :param outbound_amount: CryptoAmount  being sent.
        :return: required delay in seconds
        """
        values = await self.cache.get_network_values()

        min_tx_volume_threshold = CryptoAmount(
            Amount.automatic_base(values.get(Mimir.MIN_TX_OUT_VOLUME_THRESHOLD, 1), self.native_decimal),
            self.cache.native_asset
        )
        max_tx_out_offset = values.get(Mimir.MAX_TX_OUT_OFFSET, 0)
        tx_out_delay_rate = float(
            Amount.automatic_base(values.get(Mimir.TX_OUT_DELAY_RATE, 0), self.native_decimal)
        )

        queue: QueueResponse = await self.cache.queue_api.get_queue()
        outbound_value = CryptoAmount(
            Amount.automatic_base(queue.scheduled_outbound_value, self.native_decimal),
            self.cache.native_asset
        )

        # blocks required to confirm tx
        avg_block_time = self.chain_attributes[self.cache.chain].avg_block_time

        # If asset is equal to Rune set runeValue as outbound amount else set it to the asset's value in rune
        rune_value = await self.cache.convert(outbound_value, self.cache.native_asset)

        # Check rune value amount
        if rune_value.amount < min_tx_volume_threshold.amount:
            return avg_block_time

        # Add OutboundAmount in rune to the outbound queue
        outbound_amount_total = outbound_amount + rune_value

        # calculate if outboundAmountTotal is over the volume threshold
        volume_threshold = outbound_amount_total / min_tx_volume_threshold

        # check delay rate
        if tx_out_delay_rate - float(volume_threshold.amount) <= 1:
            tx_out_delay_rate = 1

        # calculate the minimum number of blocks in the future the txn has to be
        min_blocks = math.ceil(float(rune_value.amount) / tx_out_delay_rate)

        min_blocks = min(max_tx_out_offset, min_blocks)
        return avg_block_time * min_blocks

    async def _get_fees_in(self, fees: TotalFees, asset: Asset) -> TotalFees:
        """
        Convenience method to convert TotalFees to a different CryptoAmount

        TotalFees are always calculated and returned in RUNE, this method can
        be used to show the equivalent fees in another Asset Type
        :param fees: TotalFees - the fees you want to convert
        :param asset: Asset - the asset you want the fees converted to
        :return: TotalFees in asset
        """
        outbound_fee, affiliate_fee, total_fee, liq_fee = await asyncio.gather(
            self.cache.convert(fees.outbound_fee_amount, asset),
            self.cache.convert(fees.affiliate_fee_amount, asset),
            self.cache.convert(fees.total_fee_amount, asset),
            self.cache.convert(fees.liquidity_fee_amount, asset),
        )
        return TotalFees(
            asset,
            total_bps=fees.total_bps,
            total_fee=int(total_fee),
            slippage_bps=fees.slippage_bps,
            affiliate_fee=int(affiliate_fee),
            liquidity_fee=int(liq_fee),
            outbound_fee=int(outbound_fee)
        )

    async def _get_confirmation_counting(self, input_coin: CryptoAmount):
        """
        Finds the required confCount required for an inbound or outbound Tx to THORChain.
        Estimate based on Midgard data only.
        Finds the gas asset of the given asset (e.g. BUSD is on BNB),
        finds the value of asset in Gas Asset then finds the required confirmation count.
        ConfCount is then times by 6 seconds.
        See https://docs.thorchain.org/chain-clients/overview
        :param input_coin: amount/asset of the outbound amount.
        :return: time in seconds before a Tx is confirmed by THORChain
        """

        # RUNE, BNB and Synths have near instant finality, so no conf counting required. - need to make a BFT only case.
        if (input_coin.asset == self.native_asset or
                input_coin.asset.chain in (Chain.Cosmos, Chain.THORChain, Chain.Maya) or
                input_coin.asset.chain):
            return self.chain_attributes[Chain.THORChain].avg_block_time
        else:
            # Get the gas asset for the inbound.asset.chain
            gas_asset = get_chain_gas_asset(input_coin.asset.chain)

            # check for chain asset, else need to convert asset value to chain asset.
            amount_in_gas_asset = await self.cache.convert(input_coin, gas_asset)

            # find the required confs
            conf_config = self.chain_attributes[input_coin.asset.chain]
            required_confs = math.ceil(amount_in_gas_asset.amount / conf_config.block_reward)
            return required_confs * conf_config.avg_block_time

    async def estimate_add_lp(self, param: LPAmount) -> EstimateAddLP:
        """
        Estimates a liquidity position for given crypto amount value, both asymmetrical and symmetrical
        :param param: LPAmount - parameters needed for a estimated liquidity position
        :return: EstimateAddLP
        """
        errors = []

        if param.asset.asset.synth or param.rune.asset.synth:
            errors.append('you cannot add liquidity with a synth')
        if param.rune.asset != self.native_asset:
            errors.append('param.rune must be THOR.RUNE/MAYA.CACAO')

        asset_pool = await self.cache.get_pool_for_asset(param.asset.asset)

        lp_units = get_liquidity_units(param, asset_pool)
        inbound_details = await self.cache.get_inbound_details()
        unit_data = UnitData(
            liquidity_units=lp_units,
            total_units=int(asset_pool.thornode_details.pool_units),
        )

        pool_share = get_pool_share(unit_data, asset_pool)

        asset_wait_time_sec = await self._get_confirmation_counting(param.asset)
        rune_wait_time_sec = await self._get_confirmation_counting(param.rune)

        wait_time_sec = max(asset_wait_time_sec, rune_wait_time_sec)

        asset_inbound_fee = CryptoAmount(Amount.zero(), param.asset.asset)
        rune_inbound_fee = CryptoAmount(Amount.zero(), self.native_asset)

        if param.asset.amount > 0:
            asset_inbound_fee = calc_network_fee(param.asset.asset, inbound_details[param.asset.asset.chain])
            if asset_inbound_fee.amount * 3 > param.asset.amount:
                errors.append('Asset amount is less than fees (3x inbound fee)')

        if param.rune.amount > 0:
            rune_inbound_fee = calc_network_fee(self.native_asset, inbound_details[self.native_asset.chain])
            if rune_inbound_fee.amount * 3 > param.rune.amount:
                errors.append('Rune amount is less than fees (3x inbound fee)')

        asset_inbound_fee_rune = await self.cache.convert(asset_inbound_fee, self.native_asset)
        total_fees_amount = asset_inbound_fee_rune + rune_inbound_fee

        slip = get_slip_on_liquidity(LPAmount(param.asset, param.rune), asset_pool)

        return EstimateAddLP(
            asset_pool=asset_pool.pool.asset,
            slip_percent=float(slip) * 100.0,
            pool_share=pool_share,
            lp_units=Amount.automatic_base(lp_units),
            rune_to_asset_ratio=int(asset_pool.rune_to_asset_ratio),
            inbound_fees=LPAmountTotal(
                asset=asset_inbound_fee,
                rune=rune_inbound_fee,
                total=total_fees_amount,
            ),
            estimated_wait_seconds=wait_time_sec,
            errors=errors,
            can_add=(not errors),
            recommended_min_amount_in=0,
        )

    async def check_liquidity_position(self, asset: Asset, asset_or_rune_address: str) -> LiquidityPosition:
        """
        Checks the liquidity position of a given asset and address.

        :param asset: Asset to check
        :param asset_or_rune_address: address to check
        :return: LiquidityPosition
        """
        pool_asset = await self.cache.get_pool_for_asset(asset)
        if not pool_asset:
            raise ValueError(f"Could not find pool for asset {asset}")

        liquidity_provider = await self.cache.get_liquidity_provider(
            pool_asset.asset_string,
            asset_or_rune_address,
        )

        if not liquidity_provider:
            raise ValueError(f"Could not find liquidity provider for {asset_or_rune_address}")

        # Current block number for that chain
        last_block_obj = await self.cache.get_last_block()
        block = next((b for b in last_block_obj if b.chain == asset.chain), None)
        if not block:
            raise ValueError(f"Could not find block for chain {asset.chain}")

        # Pools total units & Lp's total units
        unit_data = UnitData(
            liquidity_units=int(liquidity_provider.units),
            total_units=int(pool_asset.thornode_details.pool_units),
        )

        current_lp = LPAmount(
            asset=Amount.automatic_base(liquidity_provider.asset_deposit_value),
            rune=Amount.automatic_base(liquidity_provider.rune_deposit_value),
        )

        pool_share = get_pool_share(unit_data, pool_asset)

        # Liquidity Unit Value Index = sprt(assetDepth * runeDepth) / Pool_Units
        # Using this formula we can work out an individual position to find LUVI and then the growth rate

        deposit_luvi = math.sqrt(
            current_lp.asset.amount * current_lp.rune.amount / unit_data.liquidity_units
        )

        redeem_luvi = math.sqrt(
            float(pool_share.asset.amount) * float(pool_share.rune.amount) / unit_data.liquidity_units
        )

        lp_growth = redeem_luvi - deposit_luvi
        current_lp_growth = (lp_growth / deposit_luvi if lp_growth > 0 else 0.0) * 100.0

        return LiquidityPosition(
            pool_share,
            liquidity_provider,
            f'{current_lp_growth:.2f} %',
        )

    async def get_pool_ratio(self, asset: Asset) -> PoolRatios:
        """
        Gets the pool ratio for a given asset
        Do not send assetNativeRune, There is no pool for it.
        :param asset: asset required to find the pool
        :return: object type ratios
        """
        asset_pool = await self.cache.get_pool_for_asset(asset)
        return PoolRatios(
            asset_to_rune=asset_pool.asset_to_rune_ratio,
            rune_to_asset=asset_pool.rune_to_asset_ratio,
        )

    async def estimate_withdraw_lp(self, asset: Asset,
                                   mode: WithdrawMode,
                                   withdraw_bps: int = THOR_BASIS_POINT_MAX,
                                   asset_address: Optional[str] = None,
                                   rune_address: Optional[str] = None,
                                   ) -> EstimateWithdrawLP:
        """
        Estimate the withdrawal of liquidity
        :param asset: Pool to withdraw from
        :param mode: withdrawal mode (asset, rune, symmetric)
        :param withdraw_bps: basis points to withdraw 0..10k (0..100%)
        :param asset_address: asset address (optional)
        :param rune_address: rune address (optional)
        :return:
        """
        asset = Asset.automatic(asset)
        if not asset.chain or not asset.symbol:
            return EstimateWithdrawLP.make_error(f"Invalid asset {asset}", mode)

        if withdraw_bps <= 0 or withdraw_bps > THOR_BASIS_POINT_MAX:
            return EstimateWithdrawLP.make_error(f"Invalid withdraw basis points {withdraw_bps}; "
                                                 f"must be 0..{THOR_BASIS_POINT_MAX}", mode)

        # Caution Dust Limits: BTC, BCH, LTC chains 10k sats; DOGE 1m Sats; ETH 0 wei; THOR 0 RUNE.
        member_address = rune_address if rune_address else asset_address

        member_detail = await self.check_liquidity_position(asset, member_address)
        if not member_detail or not member_detail.position.units:
            return EstimateWithdrawLP.make_error(f"Address {member_address} has no liquidity position for {asset}",
                                                 mode)

        dust_values = DEFAULT_CHAIN_ATTRS[asset.chain].dust
        asset_pool = await self.cache.get_pool_for_asset(asset)
        if not asset_pool:
            return EstimateWithdrawLP.make_error(f"Could not find pool for asset {asset}", mode)

        inbound_address = ''
        if not rune_address and asset_address:
            inbound_details = await self.cache.get_inbound_details()
            inbound_address = inbound_details.get(asset.chain, {}).get('address', '')
            if not inbound_address:
                return EstimateWithdrawLP.make_error(f"Could not find inbound address for {asset}", mode)

        # get pool share from unit data
        pool_share = get_pool_share(
            UnitData(
                liquidity_units=int(member_detail.position.units),
                total_units=int(asset_pool.pool.liquidity_units),
            ),
            asset_pool,
        )

        # get slip on liquidity removal
        slip = get_slip_on_liquidity(pool_share, asset_pool)

        # TODO make sure we compare wait times for withdrawing both rune and asset OR just rune OR just asset
        withdraw_part = withdraw_bps / THOR_BASIS_POINT_MAX
        wait_time_sec_for_asset, wait_time_sec_for_rune = await asyncio.gather(
            self._get_confirmation_counting(pool_share.asset / withdraw_part),
            self._get_confirmation_counting(pool_share.rune / withdraw_part)
        )

        # todo: is it cacao for maya?
        if member_detail.position.rune_address and member_detail.position.asset_address:
            wait_time_in_sec = max(wait_time_sec_for_asset, wait_time_sec_for_rune)
        elif member_detail.position.rune_address:
            wait_time_in_sec = wait_time_sec_for_rune
        else:
            wait_time_in_sec = wait_time_sec_for_asset

        all_inbound_details = await self.cache.get_inbound_details()
        inbound_details = all_inbound_details.get(asset.chain, None)

        rune_inbound = calc_network_fee(self.cache.native_asset, inbound_details)
        asset_inbound = calc_network_fee(asset, inbound_details)
        rune_outbound = calc_outbound_fee(self.cache.native_asset, inbound_details)
        asset_outbound = calc_outbound_fee(asset, inbound_details)

        # todo cacao?
        total_dust_in_rune, in_asset_fee_in_rune, out_asset_fee_in_rune = await asyncio.gather(
            self.cache.convert(dust_values.asset, self.cache.native_asset),
            self.cache.convert(asset_inbound, self.cache.native_asset),
            self.cache.convert(asset_outbound, self.cache.native_asset),
        )

        memo = THORMemo.withdraw('').build()  # todo

        deposit_amount = CryptoAmount.zero(asset)  # todo!

        return EstimateWithdrawLP(
            can_withdraw=True,
            mode=mode,
            deposit_amount=deposit_amount,
            asset_address=member_detail.position.asset_address,
            rune_address=member_detail.position.rune_address,
            slip_percent=float(slip) * 100.0,
            inbound_fee=LPAmountTotal(
                rune_inbound,
                asset_inbound,
                in_asset_fee_in_rune + rune_inbound
            ),
            inbound_min_to_send=LPAmountTotal(
                dust_values.rune,
                dust_values.asset,
                total_dust_in_rune + dust_values.rune
            ),
            outbound_fee=LPAmountTotal(
                rune_outbound,
                asset_outbound,
                out_asset_fee_in_rune + rune_outbound
            ),
            asset_amount=pool_share.asset,
            rune_amount=pool_share.rune,
            lp_growth=member_detail.lp_growth,
            estimated_wait_seconds=wait_time_in_sec,
            asset_pool=asset_pool.pool.asset,
            errors=[],
            memo=memo,
            inbound_address=inbound_address,
        )

    def _get_error_and_response_from_last_thor_response(self) -> Tuple[str, object]:
        try:
            response = self.cache.thornode_client.last_response
            data = response.data
            if isinstance(data, str):
                data = json.loads(data)
            error = data.get('error')
            if not error:
                # if no error message, this means the error has not occurred in the API, but in our code
                raise

            return str(error), response
        except Exception as e:
            return f'Could not pass error info. {e!r}', None

    async def estimate_thor_name(self, is_update: bool, thorname: str, expiry: datetime = None) -> THORNameEstimate:
        """
        Estimate the cost of registering or updating a THORName. Calculations are worked out locally based on the
        current network values and the current state of the THORName.

        :param is_update: bool - True if updating an existing THORName
        :param thorname: str - the THORName to register or update
        :param expiry: datetime - the desired expiry date of the THORName
        :return: THORNameEstimate
        """
        thor_name_details = await self.cache.get_name_details(thorname)
        if thor_name_details and thor_name_details.owner != '' and not is_update:
            return THORNameEstimate.error("THORName already registered; cannot register again", 0)

        if not thor_name_details and is_update:
            return THORNameEstimate.error("THORName not found; cannot update", 0)

        current_thorchain_height = await self.cache.get_native_block_height()

        current_expire = int(thor_name_details.expire) if thor_name_details else 0

        current_height_for_expiry = current_expire if is_update else current_thorchain_height

        blocks_to_add_to_expiry = 0 if is_update else THORNAME_BLOCKS_ONE_YEAR

        if expiry:
            current_timestamp = datetime.now().timestamp()
            expiry_timestamp = expiry.timestamp()
            interval_to_expire = expiry_timestamp - current_timestamp
            blocks_to_expire = int(interval_to_expire / self.native_block_time)
            new_height_for_expiry = current_thorchain_height + blocks_to_expire
            if current_expire:
                blocks_to_add_to_expiry = new_height_for_expiry - current_height_for_expiry
            else:
                blocks_to_add_to_expiry = blocks_to_expire

        # compute value
        constants = await self.cache.get_network_values()
        one_time_fee = Amount.zero(self.native_decimal) if is_update else Amount.automatic_base(
            constants.get(Mimir.TNS_REGISTER_FEE, 0), self.native_decimal)
        fee_per_block = constants.get(Mimir.TNS_FEE_PER_BLOCK, 0)
        total_fee_per_block = Amount.automatic_base(
            fee_per_block * max(blocks_to_add_to_expiry, 0),
            self.native_decimal
        )
        total_cost_amount = one_time_fee.as_asset + total_fee_per_block.as_asset
        total_cost = CryptoAmount(total_cost_amount, self.native_asset)

        return THORNameEstimate(
            can_register=True,
            reason='',
            cost=total_cost,
            details=thor_name_details,
            last_block_number=current_thorchain_height
        )

    async def get_inbound_details(self, chain: Union[str, Chain]) -> InboundDetail:
        """
        Get the inbound details for a given chain. It contains the recommended fee, fee units,
        router and vault addresses and the status of the chain.

        :param chain: str or Chain enum value
        :return: InboundDetail
        """
        return await self.cache.get_details_for_chain(chain)

    def tracker(self,
                wallet=None, inbound_chain: Optional[Chain] = None, outbound_chain: Optional[Chain] = None,
                inbound_client: Optional[XChainClient] = None,
                outbound_client: Optional[XChainClient] = None) -> TransactionTracker:
        """
        Create a transaction tracker for a given wallet or chain/client combination.
        Provide either a wallet with inbound/outbound chain idents or clients combination, not both.

        :param wallet: Optional[Wallet] - the wallet to get the client from
        :param inbound_chain: Optional[Chain] - the inbound Chain enum item
        :param outbound_chain: Optional[Chain] - the outbound Chain enum item
        :param inbound_client: Optional[XChainClient] - directly provide the inbound client
        :param outbound_client: Optional[XChainClient] - directly provide the outbound client
        :return: TransactionTracker object
        """

        if (inbound_client or outbound_client) and (wallet and (inbound_chain or outbound_chain)):
            raise ValueError("Cannot provide both wallet and chain/client")

        if not inbound_client and wallet:
            inbound_client = wallet.get_client(inbound_chain)
            if not inbound_client:
                raise ValueError(
                    f"You provided a wallet but no client for inbound chain {inbound_chain} could be found")

        if not outbound_chain and wallet:
            outbound_client = wallet.get_client(outbound_chain)
            if not outbound_client:
                raise ValueError(
                    f"You provided a wallet but no client for outbound chain {outbound_chain} could be found")

        return TransactionTracker(self.cache, self.chain_attributes,
                                  inbound_chain_client=inbound_client,
                                  outbound_chain_client=outbound_client)

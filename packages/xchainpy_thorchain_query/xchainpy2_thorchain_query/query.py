import asyncio
import json
import math
from datetime import datetime, timedelta
from typing import Union, List, Optional, Tuple


from xchainpy2_client import XChainClient
from xchainpy2_thorchain import THORMemo, THOR_BASIS_POINT_MAX
from xchainpy2_thornode import QuoteSwapResponse, QueueResponse, QuoteSaverDepositResponse, QuoteFees, \
    TxStatusResponse, TxSignersResponse
from xchainpy2_utils import DEFAULT_CHAIN_ATTRS, CryptoAmount, Asset, RUNE_DECIMAL, Amount, Chain, AssetRUNE, \
    get_chain_gas_asset
from .fee import calc_network_fee, calc_outbound_fee
from .midgard import MidgardAPIClient, ConfigurationEx
from .cache import THORChainCache
from .const import DEFAULT_INTERFACE_ID, Mimir, DEFAULT_EXTRA_ADD_MINUTES, THORNAME_BLOCKS_ONE_YEAR
from .liquidity import get_liquidity_units, get_pool_share, get_slip_on_liquidity
from .models import SwapEstimate, TotalFees, LPAmount, EstimateAddLP, UnitData, LPAmountTotal, \
    LiquidityPosition, PoolRatios, EstimateWithdrawLP, \
    EstimateAddSaver, SaverFees, EstimateWithdrawSaver, SaversPosition, LoanOpenQuote, \
    BlockInformation, LoanCloseQuote, THORNameEstimate, WithdrawMode, InboundDetail
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
    def from_thornode_and_midgard(cls, thornode_url='', midgard_url='',
                                  chain_attributes=None,
                                  interface_id=DEFAULT_INTERFACE_ID,
                                  native_decimal=RUNE_DECIMAL):
        """
        Create a THORChainQuery instance using custom Thornode and Midgard URLs.

        :param thornode_url: URL for Thornode API (with port and protocol)
        :param midgard_url: URL for Midgard API (with port and protocol)
        :param native_decimal: Native asset decimal places (e.g. RUNE has 8 decimals)
        :param interface_id: Interface ID for the API client. This is used to identify your requests and avoid blocking.
        :param chain_attributes: Dict of chain attributes for the query. Default is DEFAULT_CHAIN_ATTRS.

        :return: THORChainQuery instance
        """
        midgard = MidgardAPIClient(ConfigurationEx.new(host=midgard_url)) if midgard_url else MidgardAPIClient()
        thornode = THORNodeAPIClient(ConfigurationEx.new(host=thornode_url)) if thornode_url else THORNodeAPIClient()
        cache = THORChainCache(midgard, thornode)
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
            Amount.from_base(values.get(Mimir.MIN_TX_OUT_VOLUME_THRESHOLD, 1), self.native_decimal),
            self.cache.native_asset
        )
        max_tx_out_offset = values.get(Mimir.MAX_TX_OUT_OFFSET, 0)
        tx_out_delay_rate = float(
            Amount.from_base(values.get(Mimir.TX_OUT_DELAY_RATE, 0), self.native_decimal)
        )

        queue: QueueResponse = await self.cache.queue_api.get_queue()
        outbound_value = CryptoAmount(
            Amount.from_base(queue.scheduled_outbound_value, self.native_decimal),
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
        if tx_out_delay_rate - volume_threshold.amount.amount <= 1:
            tx_out_delay_rate = 1

        # calculate the minimum number of blocks in the future the txn has to be
        min_blocks = math.ceil(rune_value.amount.amount / tx_out_delay_rate)

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
                input_coin.asset.chain in (Chain.Binance, Chain.Cosmos, Chain.THORChain, Chain.Maya) or
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
            lp_units=Amount.from_base(lp_units),
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
            asset=Amount.from_base(liquidity_provider.asset_deposit_value),
            rune=Amount.from_base(liquidity_provider.rune_deposit_value),
        )

        pool_share = get_pool_share(unit_data, pool_asset)

        # Liquidity Unit Value Index = sprt(assetDepth * runeDepth) / Pool_Units
        # Using this formula we can work out an individual position to find LUVI and then the growth rate

        deposit_luvi = math.sqrt(
            current_lp.asset.amount * current_lp.rune.amount / unit_data.liquidity_units
        )

        redeem_luvi = math.sqrt(
            pool_share.asset.amount.amount * pool_share.rune.amount.amount / unit_data.liquidity_units
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

    async def estimate_add_saver(self, add_amount: CryptoAmount) -> EstimateAddSaver:
        """
        Estimate the add liquidity with saver.
        Derived from https://dev.thorchain.org/thorchain-dev/connection-guide/savers-guide

        :param add_amount: CryptoAmount
        :return: EstimateAddSaver
        """
        # check for errors before sending quote
        errors = await self.get_add_savers_estimate_errors(add_amount)

        if errors:
            return EstimateAddSaver.make_error(errors, add_amount.asset)

        # request param amount should always be in 1e8 which is why we pass in adjusted decimals if chain decimals != 8
        if add_amount.amount.decimals != self.native_decimal:
            new_add_amount = get_base_amount_with_diff_decimals(add_amount, self.native_decimal)
        else:
            new_add_amount = add_amount.amount.as_base

        new_add_amount_raw = int(new_add_amount)
        deposit_quote: QuoteSaverDepositResponse = await self.cache.quote_api.quotesaverdeposit(
            asset=str(add_amount.asset),
            amount=new_add_amount_raw,
        )

        if not deposit_quote:
            errors.append(f"Thornode request quote failed")
        if hasattr(deposit_quote, 'error'):
            errors.append(f"Thornode request quote failed: {deposit_quote.error}")

        # The recommended minimum inbound amount for this transaction type & inbound asset.
        # Sending less than this amount could result in failed refunds
        recommended_min_amount_in = int(deposit_quote.recommended_min_amount_in or 0)
        if recommended_min_amount_in and new_add_amount_raw < int(recommended_min_amount_in):
            recommended_in = CryptoAmount.automatic(int(deposit_quote.recommended_min_amount_in), new_add_amount.asset,
                                                    decimals=self.native_decimal)

            errors.append(f"Amount {new_add_amount.amount} is less than recommended min amount {recommended_in}")

        # Error handling
        if errors:
            return EstimateAddSaver.make_error(errors, add_amount.asset)

        # Calculate transaction expiry time of the vault address
        current_date_time = datetime.now()
        minutes_to_add = DEFAULT_EXTRA_ADD_MINUTES
        expiry_date_time = current_date_time + timedelta(minutes=minutes_to_add)

        # Calculate seconds
        if deposit_quote.inbound_confirmation_seconds:
            estimated_wait = deposit_quote.inbound_confirmation_seconds
        else:
            estimated_wait = await self._get_confirmation_counting(add_amount)

        pool_details = await self.cache.get_pool_for_asset(add_amount.asset)
        pool = pool_details.pool

        # Organise fees
        saver_fees = SaverFees(
            affiliate=CryptoAmount.from_base(deposit_quote.fees.affiliate, add_amount.asset),
            asset=add_amount.asset,
            outbound=CryptoAmount.from_base(deposit_quote.fees.outbound, add_amount.asset)
        )

        # Define savers filled capacity
        saver_cap_filled_percent = int(pool.synth_supply) / int(pool.asset_depth) * 100

        # Return object
        return EstimateAddSaver(
            asset_amount=CryptoAmount.from_base(deposit_quote.expected_amount_out, add_amount.asset),
            estimated_deposit_value=CryptoAmount.from_base(deposit_quote.expected_amount_out, add_amount.asset),
            fee=saver_fees,
            expiry=expiry_date_time,
            to_address=deposit_quote.inbound_address,
            memo=deposit_quote.memo,
            estimated_wait_time=estimated_wait,
            can_add_saver=(not errors),
            slip_basis_points=int(deposit_quote.fees.slippage_bps),
            saver_cap_filled_percent=saver_cap_filled_percent,
            errors=errors,
            recommended_min_amount_in=recommended_min_amount_in,
        )

    async def get_add_savers_estimate_errors(self, add_amount: CryptoAmount) -> List[str]:
        errors = []

        if add_amount.amount.internal_amount <= 0:
            errors.append(f'Invalid input amount: {add_amount.amount}; must be greater than 0')

        if add_amount.asset.synth:
            errors.append(f'Cannot add savers for synthetic assets: {add_amount.asset}')

        if add_amount.asset.chain == Chain.THORChain.value:
            errors.append(f'Cannot add RUNE to savers vault')

        pools = await self.cache.get_pools()
        saver_pools = [pool for pool in pools.values() if pool.thornode_details.savers_depth != "0"]
        saver_pool = next((pool for pool in saver_pools if pool.asset == add_amount.asset), None)
        if not saver_pool:
            errors.append(f"{add_amount.asset} does not have a saver's pool")

        inbound_details = await self.cache.get_inbound_details()
        inbound = inbound_details.get(add_amount.asset.chain)
        if inbound is None:
            errors.append(f"no inbound details for chain {add_amount.asset.chain}")
        if inbound.halted_chain:
            errors.append(f"{add_amount.asset.chain} is halted, cannot add")

        pool = pools.get(str(add_amount.asset))
        if pool.pool.status.lower() != pool.AVAILABLE:
            errors.append(f"Pool is not available for this asset {add_amount.asset}")

        # "Quote"-call will check it!
        # inbound_fee = calc_network_fee(add_amount.asset, inbound)
        # if add_amount < inbound_fee:
        #     errors.append(f"Add amount does not cover fees")
        return errors

    async def estimate_withdraw_saver(self,
                                      asset: Asset,
                                      address: str,
                                      withdraw_bps: int,
                                      height: int = 0) -> EstimateWithdrawSaver:
        """
        Estimate the withdrawal liquidity with saver (query THORChain node)
        :param asset: asset to withdraw
        :param address: address to withdraw to
        :param withdraw_bps: basis points to withdraw 0..10k (0..100%)
        :param height: block height to query (optional)
        :return: EstimateWithdrawSaver
        """
        errors = []

        if not asset.chain or not asset.symbol:
            errors.append(f'Invalid asset: {asset}')

        if withdraw_bps < 0 or withdraw_bps > THOR_BASIS_POINT_MAX:
            errors.append(f'Invalid withdraw basis points: {withdraw_bps}; '
                          f'must be between 0 and {THOR_BASIS_POINT_MAX}')

        if asset == self.native_asset or asset.synth:
            errors.append(f"Native Rune and synth assets are not supported only L1's")

        if errors:
            return EstimateWithdrawSaver.make_error(errors, asset)

        try:
            # Request withdraw quote
            withdraw_quote = await self.cache.quote_api.quotesaverwithdraw(
                height=height,
                asset=str(asset),
                address=address,
                withdraw_bps=withdraw_bps
            )
        except ValueError:
            error, withdraw_quote = self._get_error_and_response_from_last_thor_response()
            if error:
                errors.append(error)

            zero = CryptoAmount(Amount.zero(), asset)
            # noinspection PyTypeChecker
            return EstimateWithdrawSaver(
                expected_asset_amount=zero,
                fee=SaverFees(zero, asset, zero),
                expiry=datetime.now(),
                to_address='',
                memo='',
                estimated_wait_time=0,
                slip_basis_points=0,
                dust_amount=zero,
                errors=errors,
                details=withdraw_quote,
            )

        if not withdraw_quote:
            errors.append(f"Thornode request quote failed")
        elif hasattr(withdraw_quote, 'error'):
            errors.append(f"Thornode request quote failed: {withdraw_quote.error}")

        if not withdraw_quote.fees.asset or withdraw_quote.expected_amount_out == '':
            errors.append(f"This address is not found in the savers list of {asset}")

        if errors:
            return EstimateWithdrawSaver.make_error(errors, asset, withdraw_quote)

        # Calculate transaction expiry time of the vault address
        current_date_time = datetime.now()
        minutes_to_add = DEFAULT_EXTRA_ADD_MINUTES
        expiry_date_time = current_date_time + timedelta(minutes=minutes_to_add)
        estimated_wait = int(withdraw_quote.outbound_delay_seconds)
        withdraw_asset = Asset.from_string_exc(withdraw_quote.fees.asset)

        return EstimateWithdrawSaver(
            expected_asset_amount=CryptoAmount.from_base(withdraw_quote.expected_amount_out, asset),
            fee=SaverFees(
                CryptoAmount.from_base(withdraw_quote.fees.affiliate, withdraw_asset),
                withdraw_asset,
                CryptoAmount.from_base(withdraw_quote.fees.outbound, withdraw_asset)
            ),
            expiry=expiry_date_time,
            to_address=withdraw_quote.inbound_address,
            memo=withdraw_quote.memo,
            estimated_wait_time=estimated_wait,
            slip_basis_points=int(withdraw_quote.fees.slippage_bps),
            dust_amount=CryptoAmount.from_base(withdraw_quote.dust_amount, withdraw_asset),
            errors=errors,
            details=withdraw_quote,
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

    async def get_saver_position(self, asset: Union[str, Asset], address: str) -> Optional[SaversPosition]:
        """
        Get the position of a saver
        :param asset: asset (pool) to check
        :type asset: Union[str, Asset]
        :param address: saver's address
        :type address: str
        :return: SaversPosition or None if not found
        :rtype: Optional[SaversPosition]
        """
        errors = []

        pool_details = await self.cache.get_pool_for_asset(asset)

        saver = await self.cache.saver_api.saver(str(asset), address)

        if not pool_details or not pool_details.pool:
            errors.append(f"Could not get pool details for {asset}")

        if not saver or not saver.last_add_height:
            errors.append(f"Could not find position for {address}")

        owner_units = int(saver.units)
        last_added = int(saver.last_add_height)
        saver_units = int(pool_details.thornode_details.savers_units)
        asset_depth = int(pool_details.thornode_details.savers_depth)
        redeemable_value = (owner_units / saver_units) * asset_depth
        deposit_amount = CryptoAmount.from_base(saver.asset_deposit_value, asset)
        redeemable_asset_amount = CryptoAmount.from_base(redeemable_value, asset)

        if saver.asset_deposit_value:
            saver_growth = (redeemable_value - saver.asset_deposit_value) / saver.asset_deposit_value * 100.0
        else:
            saver_growth = 0.0

        return SaversPosition(
            deposit_amount,
            redeemable_asset_amount,
            last_added,
            saver_growth,
            errors,
        )

    async def get_loan_quote_open(self, amount: CryptoAmount, target_asset: Asset,
                                  destination: str, min_out: Amount, affiliate_bps: int = 0,
                                  affiliate: str = '', height: int = 0) -> LoanOpenQuote:
        """
        Get a quote for opening a loan
        :param int amount: the asset amount in 1e8 decimals and the asset used to repay the loan
        :param Asset target_asset: the target asset to receive (loan denominated in TOR regardless)
        :param str destination: the destination address, required to generate memo
        :param Amount min_out: the minimum amount of the target asset to accept
        :param str affiliate_bps: the affiliate fee in basis points
        :param int affiliate: the affiliate (address or thorname)
        :param height: optional height (default is the last block)
        :return: LoanOpenQuote
        """
        errors = []

        try:
            resp = await self.cache.quote_api.quoteloanopen(
                asset=str(amount.asset),
                amount=amount.amount.as_base.amount,
                target_asset=str(target_asset),
                destination=destination,
                min_out=min_out.as_base.amount,
                affiliate_bps=int(affiliate_bps),
                affiliate=affiliate,
                height=height
            )
        except ValueError:
            error, _ = self._get_error_and_response_from_last_thor_response()
            if error:
                errors.append(error)
            return LoanOpenQuote.empty_with_errors(errors)

        if resp.recommended_min_amount_in and amount.amount.as_base.amount < resp.recommended_min_amount_in:
            errors.append(f"Amount is less than recommended minimum amount in: {resp.recommended_min_amount_in}")

        if errors:
            return LoanOpenQuote.empty_with_errors(errors)

        return LoanOpenQuote(
            inbound_address=resp.inbound_address,
            expected_wait_time=BlockInformation(
                outbound_delay_blocks=int(resp.expected_delay_blocks),
                outbound_delay_seconds=float(resp.outbound_delay_seconds),
            ),
            fees=QuoteFees(
                asset=Asset.from_string(resp.fees.asset),
                affiliate=int(resp.fees.affiliate),
                outbound=int(resp.fees.outbound),
                total_bps=int(resp.fees.total_bps),
            ),
            slippage_bps=int(resp.slippage_bps),
            router=resp.router,
            expiry=int(resp.expiry),
            warning=resp.warning,
            notes=resp.notes,
            dust_threshold=int(resp.dust_threshold),
            memo=resp.memo,
            expected_amount_out=int(resp.expected_amount_out),
            expected_debt_up=int(resp.expected_debt_up),
            expected_collateral_up=int(resp.expected_collateral_up),
            expected_collateralization_ratio=float(resp.expected_collateralization_ratio),
            errors=errors,
            recommended_min_amount_in=int(resp.recommended_min_amount_in),
        )

    async def get_loan_quote_close(self, amount: CryptoAmount, from_address: str,
                                   loan_asset: Asset, loan_owner: str,
                                   min_out: Amount, height: int = 0) -> LoanCloseQuote:
        """
        Get a quote for closing a loan.

        :param amount:
            CryptoAmount object representing the asset amount in 1e8 decimals and the asset used to repay the loan.
        :param from_address:
            The address that is paying off the loan.
        :param loan_asset:
            Asset object representing the collateral asset of the loan.
        :param loan_owner:
            The owner of the loan collateral.
        :param min_out:
            Amount object representing the minimal threshold for output amount.
        :param height:
            Optional block height, defaults to the current tip if not provided.
        :type height: int, optional
        :return:
            LoanCloseQuote object representing the quote for closing the loan.
        :rtype: LoanCloseQuote
        """
        errors = []

        try:
            resp = await self.cache.quote_api.quoteloanclose(
                height=height,
                asset=str(amount.asset),
                amount=amount.amount.as_base.amount,
                from_address=from_address,
                loan_asset=str(loan_asset),
                loan_owner=loan_owner,
                min_out=min_out.as_base.amount
            )
        except ValueError:
            error, _ = self._get_error_and_response_from_last_thor_response()
            if error:
                errors.append(error)
            return LoanCloseQuote.empty_with_errors(errors)

        if errors:
            return LoanCloseQuote.empty_with_errors(errors)

        return LoanCloseQuote(
            inbound_address=resp.inbound_address,
            expected_wait_time=BlockInformation(
                outbound_delay_blocks=int(resp.outbound_delay_blocks),
                outbound_delay_seconds=float(resp.outbound_delay_seconds),
            ),
            fees=QuoteFees(
                asset=Asset.from_string(resp.fees.asset),
                liquidity=int(resp.fees.liquidity),
                outbound=int(resp.fees.outbound),
                total_bps=int(resp.fees.total_bps),
            ),
            slippage_bps=int(resp.slippage_bps),
            router=resp.router,
            expiry=int(resp.expiry),
            warning=resp.warning,
            notes=resp.notes,
            dust_threshold=int(resp.dust_threshold),
            memo=resp.memo,
            expected_amount_out=int(resp.expected_amount_out),
            expected_collateral_down=int(resp.expected_collateral_down),
            expected_debt_down=int(resp.expected_debt_down),
            errors=errors,
            recommended_min_amount_in=int(resp.recommended_min_amount_in),
        )

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
        one_time_fee = Amount.zero(self.native_decimal) if is_update else Amount.from_base(
            constants.get(Mimir.TNS_REGISTER_FEE, 0), self.native_decimal)
        fee_per_block = constants.get(Mimir.TNS_FEE_PER_BLOCK, 0)
        total_fee_per_block = Amount.from_base(
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

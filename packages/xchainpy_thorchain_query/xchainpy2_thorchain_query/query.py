import asyncio
import json
import math
from datetime import datetime, timedelta
from typing import Union, List, Optional

from xchainpy2_thorchain import THORMemo, THOR_BASIS_POINT_MAX
from xchainpy2_thornode import QuoteSwapResponse, QueueResponse, QuoteSaverDepositResponse, Saver, QuoteFees, \
    TxStatusResponse, TxSignersResponse
from xchainpy2_utils import DEFAULT_CHAIN_ATTRS, CryptoAmount, Asset, RUNE_DECIMAL, Amount, Chain, AssetRUNE, \
    DEFAULT_ASSET_DECIMAL, YEAR
from .cache import THORChainCache
from .const import DEFAULT_INTERFACE_ID, Mimir, DEFAULT_EXTRA_ADD_MINUTES, THORNAME_BLOCKS_ONE_YEAR
from .liquidity import get_liquidity_units, get_pool_share, get_slip_on_liquidity, get_liquidity_protection_data
from .models import SwapEstimate, TotalFees, LPAmount, EstimateAddLP, UnitData, LPAmountTotal, \
    LiquidityPosition, Block, PositionDepositValue, PoolRatios, EstimateWithdrawLP, \
    EstimateAddSaver, SaverFees, EstimateWithdrawSaver, SaversPosition, InboundDetails, LoanOpenQuote, \
    BlockInformation, LoanCloseQuote, THORNameEstimate, WithdrawMode
from .swap import get_base_amount_with_diff_decimals, calc_network_fee, calc_outbound_fee, \
    get_chain_gas_asset


class THORChainQuery:
    def __init__(self,
                 cache: THORChainCache = None,
                 chain_attributes=DEFAULT_CHAIN_ATTRS,
                 interface_id=DEFAULT_INTERFACE_ID,
                 native_decimal=RUNE_DECIMAL):

        if not cache:
            cache = THORChainCache()

        self.cache = cache
        self.chain_attributes = chain_attributes
        self.interface_id = interface_id
        self.native_decimal = native_decimal

    @property
    def native_chain_attributes(self):
        return self.chain_attributes[self.native_asset.chain]

    @property
    def native_asset(self):
        return self.cache.native_asset

    @property
    def native_block_time(self):
        return self.chain_attributes[Chain(self.native_asset.chain)].avg_block_time

    @staticmethod
    def abbreviate_asset_string(asset: Asset, max_length=5):
        if asset.contract and len(asset.contract) > max_length:
            abbrev = asset.contract[:max_length]
            asset = asset._replace(contract=abbrev)
        return str(asset)

    async def close(self):
        await self.cache.close()

    async def get_tx_details(self, txid: str) -> TxSignersResponse:
        """
        Get Tx Details
        :param txid: Transaction hash (inbound)
        :return: TxSignersResponse
        """
        return await self.cache.tx_api.tx_signers(txid)

    async def get_tx_status(self, txid: str) -> TxStatusResponse:
        """
        Get Tx status and stages
        :param txid:
        :return: TxStatusResponse
        """
        return await self.cache.tx_api.tx_status(txid)

    # ------ old stuff ----

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
        :return:
        """
        errors = []
        from_asset = str(input_amount.asset) if isinstance(input_amount.asset, Asset) else input_amount.asset
        destination_asset = str(destination_asset) if isinstance(destination_asset, Asset) else destination_asset
        input_amount_int = get_base_amount_with_diff_decimals(input_amount.amount, DEFAULT_ASSET_DECIMAL)
        input_amount_int = int(input_amount_int)

        try:
            swap_quote: QuoteSwapResponse
            swap_quote = await self.cache.quote_api.quoteswap(
                height=height, from_asset=from_asset, to_asset=destination_asset, amount=input_amount_int,
                destination=destination_address,
                tolerance_bps=tolerance_bps,
                affiliate_bps=affiliate_bps, affiliate=affiliate_address,
                streaming_interval=streaming_interval,
                streaming_quantity=streaming_quantity,
            )
        except ValueError:
            try:
                response = self.cache._thornode_client.last_response
                data = response.data
                if isinstance(data, str):
                    data = json.loads(data)
                error = data.get('error', 'unknown error')
                errors.append(str(error))
            except Exception:
                errors.append('Could not pass error info.')
                response = None

            zero = CryptoAmount(Amount.zero(), AssetRUNE)
            return SwapEstimate(
                TotalFees(destination_asset, zero, zero),
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
            errors.append(f'Input amount {input_amount.amount} is less than recommended min amount in '
                          f'{swap_quote.recommended_min_amount_in}')

        fee_asset = Asset.from_string_exc(swap_quote.fees.asset)

        return SwapEstimate(
            TotalFees(
                from_asset,
                affiliate_fee=CryptoAmount(Amount.from_base(swap_quote.fees.affiliate), fee_asset),
                outbound_fee=CryptoAmount(Amount.from_base(swap_quote.fees.outbound), fee_asset)
            ),
            slip_bps=int(swap_quote.slippage_bps),
            net_output=CryptoAmount(Amount(int(swap_quote.expected_amount_out)), destination_asset),
            outbound_delay_seconds=swap_quote.outbound_delay_seconds,
            inbound_confirmation_seconds=swap_quote.inbound_confirmation_seconds,
            can_swap=True,
            errors=errors,
            recommended_min_amount_in=int(swap_quote.recommended_min_amount_in),
            streaming_swap_interval=streaming_interval,
            details=swap_quote,
        )

    async def outbound_delay(self, outbound_amount: CryptoAmount) -> float:
        """
        Works out how long an outbound Tx will be held by THORChain before sending.
        See https://gitlab.com/thorchain/thornode/-/blob/develop/x/thorchain/manager_txout_current.go#L548
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

    async def get_fees_in(self, fees: TotalFees, asset: Asset) -> TotalFees:
        """
        Convenience method to convert TotalFees to a different CryptoAmount

        TotalFees are always calculated and returned in RUNE, this method can
        be used to show the equivalent fees in another Asset Type
        :param fees: TotalFees - the fees you want to convert
        :param asset: Asset - the asset you want the fees converted to
        :return: TotalFees in asset
        """
        outbound_fee, affiliate_fee = await asyncio.gather(
            self.cache.convert(fees.outbound_fee, asset),
            self.cache.convert(fees.affiliate_fee, asset)
        )
        return TotalFees(asset, outbound_fee, affiliate_fee)

    async def get_confirmation_counting(self, input_coin: CryptoAmount):
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
        Estimates a liquidity position for given crypto amount value, both asymmetrical and symetrical
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

        asset_wait_time_sec = await self.get_confirmation_counting(param.asset)
        rune_wait_time_sec = await self.get_confirmation_counting(param.rune)

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
        Checks the liquidity position of a given asset and address
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

        network_values = await self.cache.get_network_values()

        block = Block(
            current=self.cache.pluck_native_block_height(block),
            last_added=liquidity_provider.last_add_height,
            full_protection=network_values.get(Mimir.FULL_IL_PROTECTION_BLOCKS, 0),
        )

        current_lp = PositionDepositValue(
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

        impermanent_loss_protection = get_liquidity_protection_data(current_lp, pool_share, block)

        return LiquidityPosition(
            pool_share,
            liquidity_provider,
            f'{current_lp_growth:.2f} %',
            impermanent_loss_protection
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
            self.get_confirmation_counting(pool_share.asset / withdraw_part),
            self.get_confirmation_counting(pool_share.rune / withdraw_part)
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

        memo = THORMemo.withdraw().build() # todo

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
            impermanent_loss_protection=member_detail.impermanent_loss_protection,
            asset_pool=asset_pool.pool.asset,
            errors=[],
            memo=memo,
            inbound_address=inbound_address,
        )

    async def estimate_add_saver(self, add_amount: CryptoAmount) -> EstimateAddSaver:
        """
        Estimate the add liquidity with saver
        Derrived from https://dev.thorchain.org/thorchain-dev/connection-guide/savers-guide
        :param add_amount: CryptoAmount
        :return:
        """
        # check for errors before sending quote
        errors = await self.get_add_savers_estimate_errors(add_amount)

        if errors:
            return EstimateAddSaver.make_error(errors, add_amount.asset)

        # request param amount should always be in 1e8 which is why we pass in adjusted decimals if chain decimals != 8
        if add_amount.amount.decimals != DEFAULT_ASSET_DECIMAL:
            new_add_amount = get_base_amount_with_diff_decimals(add_amount, DEFAULT_ASSET_DECIMAL)
        else:
            new_add_amount = add_amount.amount.as_base

        deposit_quote: QuoteSaverDepositResponse = await self.cache.quote_api.quotesaverdeposit(
            asset=new_add_amount,
            amount=''
        )

        if not deposit_quote:
            errors.append(f"Thornode request quote failed")
        if hasattr(deposit_quote, 'error'):
            errors.append(f"Thornode request quote failed: {deposit_quote.error}")

        # The recommended minimum inbound amount for this transaction type & inbound asset.
        # Sending less than this amount could result in failed refunds
        if int(deposit_quote.recommended_min_amount_in) and \
                int(new_add_amount.amount) < int(deposit_quote.recommended_min_amount_in):
            errors.append(f"Amount {new_add_amount.amount} is less than recommended min amount in "
                          f"{deposit_quote.recommended_min_amount_in}")

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
            estimated_wait = await self.get_confirmation_counting(add_amount)

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
            slip_basis_points=int(deposit_quote.slippage_bps),
            saver_cap_filled_percent=saver_cap_filled_percent,
            errors=errors,
            recommended_min_amount_in=int(deposit_quote.recommended_min_amount_in),
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

        inbound_fee = calc_network_fee(add_amount.asset, inbound)
        if add_amount < inbound_fee:
            errors.append(f"Add amount does not cover fees")
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

        # Check to see if there is a position before calling withdraw quote
        check_position = await self.get_saver_position(asset, address)

        if check_position.errors:
            errors.extend(check_position.errors)
            return EstimateWithdrawSaver.make_error(errors, asset)

        # Request withdraw quote
        withdraw_quote = await self.cache.quote_api.quotesaverwithdraw(
            height=height,
            asset=str(asset),
            address=address,
            withdraw_bps=withdraw_bps
        )

        if not withdraw_quote:
            errors.append(f"Thornode request quote failed")
        elif hasattr(withdraw_quote, 'error'):
            errors.append(f"Thornode request quote failed: {withdraw_quote.error}")

        if errors:
            return EstimateWithdrawSaver.make_error(errors, asset)

        # Calculate transaction expiry time of the vault address
        current_date_time = datetime.now()
        minutes_to_add = DEFAULT_EXTRA_ADD_MINUTES
        expiry_date_time = current_date_time + timedelta(minutes=minutes_to_add)
        estimated_wait = int(withdraw_quote.outbound_delay_seconds)
        withdraw_asset = Asset.from_string_exc(withdraw_quote.fees.asset)

        return EstimateWithdrawSaver(
            CryptoAmount.from_base(withdraw_quote.expected_amount_out, asset),
            fee=SaverFees(
                CryptoAmount.from_base(withdraw_quote.fees.affiliate, withdraw_asset),
                withdraw_asset,
                CryptoAmount.from_base(withdraw_quote.fees.outbound, withdraw_asset)
            ),
            expiry=expiry_date_time,
            to_address=withdraw_quote.inbound_address,
            memo=withdraw_quote.memo,
            estimated_wait_time=estimated_wait,
            slip_basis_points=int(withdraw_quote.slippage_bps),
            dust_amount=CryptoAmount.from_base(withdraw_quote.dust_amount, withdraw_asset),
            errors=errors
        )

    async def get_saver_position(self, asset: Asset, address: str,
                                 inbound_details: Optional[InboundDetails] = None
                                 ) -> Optional[SaversPosition]:
        """
        Get the position of a saver
        :param inbound_details: Inbound details
        :param asset: asset (pool) to check
        :param address: saver's address
        :return:
        """
        errors = []
        if not inbound_details:
            inbound_details = await self.cache.get_inbound_details()

        block_data = await self.cache.get_last_block()
        block = next((item for item in block_data if item.chain == asset.chain), None)
        native_block = self.cache.pluck_native_block_height(block)

        pool_details = await self.cache.get_pool_for_asset(asset)

        all_savers: List[Saver] = self.cache.saver_api.savers(str(asset))  # todo: check if this is correct
        this_saver = next((item for item in all_savers if item.asset_address == address), None)

        if not pool_details or not pool_details.pool:
            errors.append(f"Could not get pool details for {asset}")

        if not block or not native_block:
            errors.append(f"Could not get thorchain block height for {asset.chain}")

        if not this_saver or not this_saver.last_add_height:
            errors.append(f"Could not find position for {address}")

        outbound_fee = calc_outbound_fee(asset, inbound_details[asset.chain])
        outbound_fee_8 = get_base_amount_with_diff_decimals(outbound_fee, DEFAULT_ASSET_DECIMAL)

        # For comparison use 1e8 since asset_redeem_value is returned in 1e8
        if int(this_saver.asset_redeem_value) < int(outbound_fee_8):
            errors.append(f"Unlikely to withdraw balance as outbound fee is greater than redeemable amount"
                          f"{this_saver.asset_redeem_value} < {outbound_fee_8}")

        owner_units = int(this_saver.units)
        last_added = int(this_saver.last_add_height)
        saver_units = int(pool_details.thornode_details.savers_units)
        asset_depth = int(pool_details.thornode_details.savers_depth)
        redeemable_value = (owner_units / saver_units) * asset_depth
        deposit_amount = CryptoAmount.from_base(this_saver.asset_deposit_value, asset)
        redeemable_asset_amount = CryptoAmount.from_base(redeemable_value, asset)

        savers_age = (int(native_block) - last_added) / (YEAR / self.native_block_time)
        saver_growth = (redeemable_asset_amount - deposit_amount) / deposit_amount * 100.0

        return SaversPosition(
            deposit_amount,
            redeemable_asset_amount,
            int(this_saver.last_add_height),
            float(saver_growth.amount.as_asset.amount),
            float(savers_age),
            float(savers_age * 365),
            errors,
            outbound_fee
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
        if hasattr(resp, 'error'):
            errors.append(f"Thornode request quote failed: {resp.error}")

        if resp.recommended_min_amount_in and amount.amount.as_base.amount < resp.recommended_min_amount_in:
            errors.append(f"Amount is less than recommended minimum amount in: {resp.recommended_min_amount_in}")

        if errors:
            # Todo: convenience type conversion
            return LoanOpenQuote(
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

        # Todo: convenience type conversion
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
        Get a quote for closing a loan
        :param amount: CryptoAmount (the asset amount in 1e8 decimals and asset the asset used to repay the loan)
        :param from_address: the address that is paying off the loan
        :param loan_asset: the collateral asset of the loan
        :param loan_owner: the owner of the loan collateral
        :param min_out: minimal threshold for output amount
        :param height: optional block height, defaults to current tip
        :return:
        """
        errors = []

        resp = await self.cache.quote_api.quoteloanclose(
            height=height,
            asset=str(amount.asset),
            amount=amount.amount.as_base.amount,
            from_address=from_address,
            loan_asset=str(loan_asset),
            loan_owner=loan_owner,
            min_out=min_out.as_base.amount
        )

        if hasattr(resp, 'error'):
            errors.append(f"Thornode request quote failed: {resp.error}")

        if errors:
            return LoanCloseQuote(
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
        Estimate the cost of registering or updating a THORName
        :param is_update: bool - True if updating an existing THORName
        :param thorname: str - the THORName to register or update
        :param expiry: datetime - the desired expiry date of the THORName
        :return:
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

    async def get_recommended_fee_rate(self, chain: Chain) -> int:
        """
        Get the recommended fee for a given chain from THORChain
        :param chain: Chain - the chain to get the fee for
        :return: int - the recommended fee rate
        """
        fee_number = await self.cache.get_fee_rates(chain)
        return fee_number

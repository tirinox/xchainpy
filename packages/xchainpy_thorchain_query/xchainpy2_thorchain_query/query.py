import asyncio
import math
from datetime import datetime, timedelta
from decimal import Decimal
from typing import Union, List

from xchainpy2_thornode import QuoteSwapResponse, QueueResponse, QuoteSaverDepositResponse
from xchainpy2_utils import DEFAULT_CHAIN_ATTRS, CryptoAmount, Asset, Address, RUNE_DECIMAL, Amount, MAX_BASIS_POINTS, \
    Chain, AssetRUNE, DEFAULT_ASSET_DECIMAL
from xchainpy2_utils.swap import get_base_amount_with_diff_decimals, calc_network_fee, calc_outbound_fee, \
    is_gas_asset, get_chain_gas_asset
from .cache import THORChainCache
from .const import DEFAULT_INTERFACE_ID, Mimir
from .liquidity import get_liquidity_units, get_pool_share, get_slip_on_liquidity, get_liquidity_protection_data
from .models import TxDetails, SwapEstimate, SwapOutput, TotalFees, LPAmount, EstimateAddLP, UnitData, LPAmountTotal, \
    LiquidityPosition, Block, PostionDepositValue, PoolRatios, WithdrawLiquidityPosition, EstimateWithdrawLP, \
    EstimateAddSaver, SaverFees


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

    async def quote_swap(self,
                         from_address: Address,
                         amount: Amount,
                         from_asset: Union[Asset, str],
                         destination_address: str,
                         destination_asset: Union[Asset, str],
                         tolerance_bps: int = 0,
                         interface_id=DEFAULT_INTERFACE_ID,
                         affiliate_bps=0,
                         affiliate_address='',
                         height=0,
                         ) -> TxDetails:
        """
        Quote a swap transaction
        :param from_address:
        :param amount:
        :param from_asset:
        :param destination_address:
        :param destination_asset:
        :param tolerance_bps:
        :param interface_id:
        :param affiliate_bps:
        :param affiliate_address:
        :param height:
        :return:
        """
        errors = []
        from_asset = str(from_asset) if isinstance(from_asset, Asset) else from_asset
        destination_asset = str(destination_asset) if isinstance(destination_asset, Asset) else destination_asset
        input_amount = get_base_amount_with_diff_decimals(amount, DEFAULT_ASSET_DECIMAL)

        try:
            swap_quote: QuoteSwapResponse
            swap_quote = await self.cache.quote_api.quoteswap(
                height=height, from_asset=from_asset, to_asset=destination_asset, amount=int(input_amount),
                destination=destination_address,
                from_address=from_address, tolerance_bps=tolerance_bps,
                affiliate_bps=affiliate_bps, affiliate=affiliate_address
            )
        except ValueError:
            response = self.cache.thornode_client.last_response
            error = response.data.get('error', 'unknown error')
            error.append(f'Thornode request quote: {error}')

            zero = CryptoAmount(Amount.zero(), AssetRUNE)
            return TxDetails(
                '', '', datetime.now(),
                SwapEstimate(
                    TotalFees(destination_asset, zero, zero),
                    0,
                    zero,
                    0, 0,
                    can_swap=False,
                    errors=errors
                )
            )

        fee_asset = Asset.from_string(swap_quote.fees.asset)

        return TxDetails(
            memo=self.construct_swap_memo(swap_quote.memo, interface_id),
            to_address=swap_quote.inbound_address,
            expiry=datetime.fromtimestamp(swap_quote.expiry),  # timezone?
            tx_estimate=SwapEstimate(
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
                errors=errors
            )
        )

    @staticmethod
    def construct_swap_memo(memo: str, interface_id: str) -> str:
        memo_parts = memo.split(':')
        if len(memo_parts) > 3:
            part3 = memo_parts[3]
            if len(part3) >= 3:
                #  memoPart[3].substring(0, memoPart[3].length - 3)
                part3 = part3[:-3] + interface_id
            else:
                part3 = interface_id
            memo_parts[3] = part3

            return ':'.join(memo_parts)

        return memo

    async def outbound_delay(self, outbound_amount: CryptoAmount) -> float:
        """
        Works out how long an outbound Tx will be held by THORChain before sending.
        See https://gitlab.com/thorchain/thornode/-/blob/develop/x/thorchain/manager_txout_current.go#L548
        :param outbound_amount: CryptoAmount  being sent.
        :return: required delay in seconds
        """
        values = await self.cache.get_network_values()

        min_tx_volume_threshold = CryptoAmount(
            values.get(Mimir.MIN_TX_OUT_VOLUME_THRESHOLD, 1),
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

        # Add OutboundAmount in rune to the oubound queue
        outbound_amount_total = outbound_amount + rune_value

        # calculate the if outboundAmountTotal is over the volume threshold
        volume_threshold = outbound_amount_total / min_tx_volume_threshold

        # check delay rate
        if tx_out_delay_rate - volume_threshold.amount.amount <= 1:
            tx_out_delay_rate = 1

        # calculate the minimum number of blocks in the future the txn has to be
        min_blocks = rune_value.amount.amount / tx_out_delay_rate

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
            current=self.cache.get_native_block(block),
            last_added=liquidity_provider.last_add_height,
            full_protection=network_values.get(Mimir.FULL_IL_PROTECTION_BLOCKS, 0),
        )

        current_lp = PostionDepositValue(
            asset=Amount.from_base(liquidity_provider.asset_deposit_value),
            rune=Amount.from_base(liquidity_provider.rune_deposit_value),
        )

        pool_share = get_pool_share(unit_data, pool_asset)

        # Liquidity Unit Value Index = sprt(assetdepth * runeDepth) / Poolunits
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

    async def estimate_withdraw_lp(self, param: WithdrawLiquidityPosition) -> EstimateWithdrawLP:
        """
        Estimate the withdrawal of liquidity
        :param param: WithdrawLiquidityPosition
        :return:
        """
        # Caution Dust Limits: BTC, BCH, LTC chains 10k sats; DOGE 1m Sats; ETH 0 wei; THOR 0 RUNE.
        asset_or_rune_address = param.rune_address if param.rune_address else param.asset_address
        member_detail = await self.check_liquidity_position(param.asset, asset_or_rune_address)
        dust_values = DEFAULT_CHAIN_ATTRS[param.asset.chain].dust
        asset_pool = await self.cache.get_pool_for_asset(param.asset)

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
        wait_time_sec_for_asset, wait_time_sec_for_rune = await asyncio.gather(
            self.get_confirmation_counting(pool_share.asset / (param.percentage / 100.0)),
            self.get_confirmation_counting(pool_share.rune / (param.percentage / 100.0))
        )

        wait_time_in_sec = 0
        # todo: is it cacao for maya?
        if member_detail.position.rune_address and member_detail.position.asset_address:
            wait_time_in_sec = max(wait_time_sec_for_asset, wait_time_sec_for_rune)
        elif member_detail.position.rune_address:
            wait_time_in_sec = wait_time_sec_for_rune
        else:
            wait_time_in_sec = wait_time_sec_for_asset

        all_inbound_details = await self.cache.get_inbound_details()
        inbound_details = all_inbound_details.get(param.asset.chain, None)

        rune_inbound = calc_network_fee(self.cache.native_asset, inbound_details)
        asset_inbound = calc_network_fee(param.asset, inbound_details)
        rune_outbound = calc_outbound_fee(self.cache.native_asset, inbound_details)
        asset_outbound = calc_outbound_fee(param.asset, inbound_details)

        # todo cacao?
        total_dust_in_rune, in_asset_fee_in_rune, out_asset_fee_in_rune = await asyncio.gather(
            self.cache.convert(dust_values.asset, self.cache.native_asset),
            self.cache.convert(asset_inbound, self.cache.native_asset),
            self.cache.convert(asset_outbound, self.cache.native_asset),
        )

        return EstimateWithdrawLP(
            member_detail.position.asset_address,
            member_detail.position.rune_address,
            slip_percent=slip * 100.0,
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

        # Error handling
        if errors:
            return EstimateAddSaver(
                add_amount,
                CryptoAmount.zero_from(add_amount),
                -1,
                SaverFees(
                    CryptoAmount.zero_from(add_amount),
                    add_amount.asset,
                    CryptoAmount.zero_from(add_amount),
                ),
                datetime.fromtimestamp(0),
                to_address='',
                memo='',
                saver_cap_filled_percent=-1,
                estimated_wait_time=-1,
                can_add_saver=False,
                errors=errors
            )

        # Calculate transaction expiry time of the vault address
        current_date_time = datetime.now()
        minutes_to_add = 15
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
            errors=errors
        )

    async def get_add_savers_estimate_errors(self, add_amount: CryptoAmount) -> List[str]:
        errors = []

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

    # ---- previous code ----

    async def is_swap_valid(self,
                            input_coin: CryptoAmount,
                            destination_asset: Asset,
                            destination_address: Address,
                            slip_limit=0.03,
                            affiliate_address='',
                            affiliate_fee_basis_points=0):
        """
        Basic Checks for swap information
        :param input_coin:
        :param destination_asset:
        :param destination_address:
        :param slip_limit:
        :param affiliate_address:
        :param affiliate_fee_basis_points:
        :return: bool
        """
        if input_coin.asset.is_rune_native or input_coin.asset.synth:
            if input_coin.amount.decimals != self.native_decimal:
                raise ValueError(f"input asset "
                                 f"{input_coin.asset!s} "
                                 f"must have decimals of {self.native_decimal}")

        pool = await self.cache.get_pool_for_asset(input_coin.asset)  # todo!
        native_decimals = pool.thornode_details.decimals
        if native_decimals and native_decimals != '-1' and input_coin.amount.decimals != native_decimals:
            raise ValueError(f"input asset "
                             f"{input_coin.asset!s} "
                             f"must have decimals of {native_decimals}")

        if input_coin.asset == destination_asset:
            raise ValueError(f"input_coin.asset and destination_asset cannot be the same ({destination_asset})")

        if input_coin.amount.internal_amount <= 0:
            raise ValueError(f"input_coin.amount cannot be negative ({input_coin.amount})")

        # Affiliate fee % can't exceed 10% because this is set by TC.
        if affiliate_fee_basis_points > 1000:
            raise ValueError(f"affiliate_fee_basis_points cannot exceed 1000 ({affiliate_fee_basis_points})")

        if affiliate_fee_basis_points < 0:
            raise ValueError(f"affiliate_fee_basis_points cannot be negative ({affiliate_fee_basis_points})")

        if slip_limit < 0.0 or slip_limit > 1.0:
            raise ValueError(f"slip_limit must be between 0.0 and 1.0 ({slip_limit})")

        return True

    async def calc_swap_estimate(self,
                                 input_coin: CryptoAmount,
                                 destination_asset: Asset,
                                 destination_address,
                                 slip_limit,
                                 affiliate_address,
                                 affiliate_fee_basis_points,
                                 interface_id,
                                 source_inbound_details,
                                 destination_inbound_details) -> SwapEstimate:
        # If input is already in 8 decimals skip the convert
        if input_coin.amount.decimals != RUNE_DECIMAL:
            input_coin = await self.cache.convert(input_coin, input_coin.asset)

        inbound_fee_in_inbound_gas_asset = calc_network_fee(input_coin.asset, source_inbound_details)
        outbound_fee_in_outbound_gas_asset = calc_outbound_fee(destination_asset, destination_inbound_details)

        # Check outbound fee is equal too or greater than 1 USD * need to find a more permanent solution to this.
        # referencing just 1 stable coin pool has problems
        if destination_asset.chain != self.cache.chain and not destination_asset.synth:
            deepest_usd_pool = await self.cache.get_deepest_usd_pool()
            usd_asset = deepest_usd_pool.asset
            usd_min_fee = CryptoAmount(
                Amount.from_asset("1", deepest_usd_pool.thornode_details.decimals), usd_asset
            )
            outbound_fee = await self.cache.convert(outbound_fee_in_outbound_gas_asset, usd_asset)
            if outbound_fee.amount.internal_amount < usd_min_fee.amount.internal_amount:
                # fixme: why native asset (RUNE)?
                outbound_fee_in_outbound_gas_asset = await self.cache.convert(usd_min_fee, self.native_asset)

        # --- Remove Fees from inbound before doing the swap ---

        inbound_fee_in_inbound_gas_asset = await self.cache.convert(inbound_fee_in_inbound_gas_asset, input_coin.asset)
        # if it is a gas asset, take away inbound fee, else leave it as is.
        # Still allow inboundFeeInInboundGasAsset to pass to swapEstimate.totalFees.inboundFee so user is aware
        # if the gas requirements.
        if is_gas_asset(input_coin.asset):
            input_minus_outbound_fee_in_asset = input_coin - inbound_fee_in_inbound_gas_asset
        else:
            input_minus_outbound_fee_in_asset = input_coin

        # remove any affiliateFee. netInput * affiliateFee (percentage) of the destination asset type
        if affiliate_fee_basis_points:
            affiliate_fee_percent = affiliate_fee_basis_points / MAX_BASIS_POINTS
        else:
            affiliate_fee_percent = 0

        affiliate_fee_in_asset = input_minus_outbound_fee_in_asset * affiliate_fee_percent

        if affiliate_fee_in_asset.asset == self.native_asset:  # rune/cacao
            affiliate_fee_swap_out_in_rune = SwapOutput(
                output=affiliate_fee_in_asset,
                swap_fee=CryptoAmount(Amount(0, self.native_decimal), self.native_asset),
                slip=Decimal(0),
            )
        else:
            affiliate_fee_swap_out_in_rune = await self.cache.get_expected_swap_output(
                affiliate_fee_in_asset,
                self.native_asset
            )

        # remove the affiliate fee from the input.
        input_net_in_asset = input_minus_outbound_fee_in_asset - affiliate_fee_in_asset

        # Now calculate swap output based on inputNetAmount
        swap_out_in_dest_asset = await self.cache.get_expected_swap_output(
            input_net_in_asset,
            destination_asset
        )
        # // ---------------- Remove Outbound Fee ---------------------- /

        outbound_fee_in_dest_asset = await self.cache.convert(
            outbound_fee_in_outbound_gas_asset, destination_asset
        )
        net_output_in_asset = swap_out_in_dest_asset.output - outbound_fee_in_dest_asset

        total_fees = TotalFees(
            inbound_fee=inbound_fee_in_inbound_gas_asset,
            swap_fee=swap_out_in_dest_asset.swap_fee,
            outbound_fee=outbound_fee_in_outbound_gas_asset,
            affiliate_fee=affiliate_fee_swap_out_in_rune.swap_fee,
        )

        swap_estimate = SwapEstimate(
            total_fees,
            swap_out_in_dest_asset.slip,
            net_output_in_asset,
            0,
            can_swap=False,  # will be set within EstimateSwap if canSwap = true
            errors=[]  # assume false for now, the getSwapEstimateErrors() step will flip this flag if required
        )

        return swap_estimate

    async def get_swap_estimate_errors(self,
                                       input_coin: CryptoAmount,
                                       destination_asset: Asset,
                                       destination_address,
                                       slip_limit,
                                       affiliate_address,
                                       affiliate_fee_basis_points,
                                       interface_id,
                                       swap_estimate,
                                       source_inbound_details,
                                       destination_inbound_details):
        pass  # todo

    async def get_outbound_delay(self, outbound_amount: CryptoAmount):
        """
        Works out how long an outbound Tx will be held by THORChain before sending.
        See: https://gitlab.com/thorchain/thornode/-/blob/develop/x/thorchain/manager_txout_current.go#L548
        :param outbound_amount: CryptoAmount  being sent.
        :return: required delay in seconds
        """
        network_values = await self.cache.get_network_values()
        min_tx_out_volume_threshold = CryptoAmount(
            Amount.from_base(network_values[Mimir.MIN_TX_OUT_VOLUME_THRESHOLD]),
            self.native_asset
        )
        max_tx_out_offset = network_values[Mimir.MAX_TX_OUT_OFFSET]
        tx_out_delay_rate = Amount.from_base(network_values[Mimir.TX_OUT_DELAY_RATE]).as_asset.amount

        queue = await self.cache.queue_api.queue()
        outbound_value = Amount.from_base(queue.outbound_value).as_asset.amount
        tc_block_time = self.native_chain_attributes.avg_block_time

        # If asset is equal to Rune set runeValue as outbound amount else set it to the asset's value in rune
        rune_value = await self.cache.convert(outbound_amount, self.native_asset)

        # Check rune value amount
        if rune_value < min_tx_out_volume_threshold:
            return tc_block_time

        # Rune value in the outbound queue
        if outbound_value is None:
            raise ValueError("Could not return Scheduled Outbound Value")

        # Add OutboundAmount in rune to the outbound queue
        outbound_total_amount = rune_value + outbound_value

        # calculate the if outboundAmountTotal is over the volume threshold
        volume_threshold = outbound_total_amount / min_tx_out_volume_threshold

        # check delay rate
        deduction = 1 if volume_threshold.amount.as_asset.amount < 1 else tx_out_delay_rate
        tx_out_delay_rate = tx_out_delay_rate - deduction

        # calculate the minimum number of blocks in the future the txn has to be
        min_blocks = rune_value.amount.as_asset.amount / tx_out_delay_rate  # fixme: potential zero-division here

        min_blocks = min(min_blocks, max_tx_out_offset)

        return min_blocks * tc_block_time

    @property
    def native_chain_attributes(self):
        return self.chain_attributes[self.native_asset.chain]

    @property
    def native_asset(self):
        return self.cache.native_asset

    @staticmethod
    def abbreviate_asset_string(asset: Asset, max_length=5):
        if asset.contract and len(asset.contract) > max_length:
            abrev = asset.contract[:max_length]
            asset = asset._replace(contract=abrev)
        return str(asset)

    async def estimate_swap(
            self,
            input_coin: CryptoAmount,
            destination_asset: Asset,
            destination_address: Address,
            slip_limit=0.03,
            affiliate_address='',
            affiliate_fee_basis_points=0,
            interface_id=DEFAULT_INTERFACE_ID,
    ) -> TxDetails:
        await self.is_swap_valid(input_coin,
                                 destination_asset,
                                 destination_address,
                                 slip_limit,
                                 affiliate_address,
                                 affiliate_fee_basis_points)

        inbound_details = await self.cache.get_inbound_details()
        source_inbound_details = inbound_details[input_coin.asset.chain]
        destination_inbound_details = inbound_details[destination_asset.chain]

        # Calculate swap estimate
        swap_estimate = await self.calc_swap_estimate(
            input_coin,
            destination_asset,
            destination_address,
            slip_limit,
            affiliate_address,
            affiliate_fee_basis_points,
            interface_id,
            source_inbound_details,
            destination_inbound_details
        )

        # Calculate transaction expiry time
        current_datetime = datetime.now()
        minutes_to_add = 15
        expiry = current_datetime + timedelta(minutes=minutes_to_add)

        # Check for errors
        errors = await self.get_swap_estimate_errors(
            input_coin,
            destination_asset,
            destination_address,
            slip_limit,
            affiliate_address,
            affiliate_fee_basis_points,
            interface_id,
            swap_estimate,
            source_inbound_details,
            destination_inbound_details
        )

        tx_details = TxDetails(
            memo='',
            to_address='',
            expiry=expiry,
            tx_estimate=swap_estimate
        )

        if errors:
            tx_details.tx_estimate.can_swap = False
            tx_details.tx_estimate.errors = errors
        else:
            tx_details.tx_estimate.can_swap = True

            inbound_details = await self.cache.get_inbound_details()
            inbound_asgard = inbound_details[input_coin.asset.chain]

            tx_details.to_address = inbound_asgard.address if inbound_asgard else ''

            # Work out LIM from the slip percentage
            lim_percentage = 1
            if slip_limit:
                lim_percentage = 1 - slip_limit
                # else allowed slip is 100%
            # Lim should allways be 1e8
            lim_asset_amount: CryptoAmount = swap_estimate.net_output * lim_percentage
            lim_asset_amount_8 = get_base_amount_with_diff_decimals(lim_asset_amount, DEFAULT_ASSET_DECIMAL)

            inbound_delay = await self.get_confirmation_counting(input_coin)
            outbound_delay = await self.get_outbound_delay(lim_asset_amount)

            tx_details.tx_estimate.wait_time_seconds = outbound_delay + inbound_delay

            # limit = Amount.from_base(lim_asset_amount_8, 8)
            # tx_details.memo = self.construct_swap_memo(???)
        return tx_details

import math
from datetime import datetime, timedelta
from decimal import Decimal
from typing import Union

from xchainpy2_thornode import QuoteApi
from xchainpy2_utils import DEFAULT_CHAIN_ATTRS, CryptoAmount, Asset, Address, RUNE_DECIMAL, Amount, AssetBTC, \
    MAX_BASIS_POINTS, Chain
from xchainpy2_utils.swap import get_base_amount_with_diff_decimals, calc_network_fee, calc_outbound_fee, \
    is_gas_asset, get_chain_gas_asset
from .cache import THORChainCache
from .const import DEFAULT_INTERFACE_ID, Mimir
from .liquidity import get_liquidity_units, get_pool_share
from .models import TxDetails, SwapEstimate, SwapOutput, TotalFees, LPAmount, EstimateAddLP, UnitData


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
                         tolerance_bps: int=0,
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
        input_amount = get_base_amount_with_diff_decimals(amount, 8)

        api: QuoteApi = self.cache.quote_api
        swap_quote = await self.cache.quote_api.quoteswap(
            height=height, from_asset=from_asset, to_asset=destination_asset, amount=int(input_amount),
            destination=destination_address,
            from_address=from_address, tolerance_bps=tolerance_bps,
            affiliate_bps=affiliate_bps, affiliate=affiliate_address
        )

        print(swap_quote)


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
            lim_asset_amount_8 = get_base_amount_with_diff_decimals(lim_asset_amount, 8)

            inbound_delay = await self.get_confirmation_counting(input_coin)
            outbound_delay = await self.get_outbound_delay(lim_asset_amount)

            tx_details.tx_estimate.wait_time_seconds = outbound_delay + inbound_delay

            limit = Amount.from_base(lim_asset_amount_8, 8)
            tx_details.memo = self.construct_swap_memo(
                input_coin,
                destination_asset,
                limit,
                destination_address,
                affiliate_address,
                affiliate_fee_basis_points,
                interface_id
            )
        return tx_details

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

    def construct_swap_memo(self,
                            input_coin,
                            destination_asset,
                            limit,
                            destination_address,
                            affiliate_address,
                            affiliate_fee_basis_points,
                            interface_id) -> str:
        lim_string = str(limit.amount)
        lim_string = lim_string[:-3]  # we don't want the decimal places? todo: check this
        dest_asset_str = {self.abbreviate_asset_string(destination_asset)}
        memo = f'=:{dest_asset_str}:{destination_address}:{lim_string}'

        # NOTE: we should validate affiliate address is EITHER: a thorname or valid thorchain address,
        # currently we cannot do this without importing xchain-thorchain
        if affiliate_address:
            # NOTE: we should validate destinationAddress address is valid destination address
            # for the asset type requested
            memo += f':{affiliate_address}:{affiliate_fee_basis_points}'

        # If memo length is too long for BTC, trim it
        if input_coin.asset == AssetBTC and len(memo) > 80:
            memo = f'=:{dest_asset_str}:{destination_address}:{lim_string}'  # fixme: wtf

        return memo

    @staticmethod
    def abbreviate_asset_string(asset: Asset, max_length=5):
        if asset.contract and len(asset.contract) > max_length:
            abrev = asset.contract[:max_length]
            asset = asset._replace(contract=abrev)
        return str(asset)

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

        pool_share = get_pool_share(unit_data, inbound_details)

        asset_wait_time_sec = await self.get_confirmation_counting(param.asset)
        rune_wait_time_sec = await self.get_confirmation_counting(param.rune)

        wait_time_sec = max(asset_wait_time_sec, rune_wait_time_sec)

        asset_inbound_fee = CryptoAmount(Amount.zero(), param.asset.asset)
        rune_inbound_fee = CryptoAmount(Amount.zero(), self.native_asset)

        if param.asset.amount > 0:
            asset_inbound_fee = calc_network_fee(param.asset.asset, inbound_details[param.asset.asset.chain])
            # if asset_inbound_fee.amount.times(3) > param.asset.amount:
            # todo!


"""
... (truncated)
    let assetInboundFee = new CryptoAmount(baseAmount(0), params.asset.asset)
    let runeInboundFee = new CryptoAmount(baseAmount(0), AssetRuneNative)

    if (!params.asset.assetAmount.eq(0)) {
      assetInboundFee = calcNetworkFee(params.asset.asset, inboundDetails[params.asset.asset.chain])
      if (assetInboundFee.assetAmount.amount().times(3).gt(params.asset.assetAmount.amount()))
        errors.push(`Asset amount is less than fees`)
    }
    if (!params.rune.assetAmount.eq(0)) {
      runeInboundFee = calcNetworkFee(params.rune.asset, inboundDetails[params.rune.asset.chain])
      if (runeInboundFee.assetAmount.amount().times(3).gt(params.rune.assetAmount.amount()))
        errors.push(`Rune amount is less than fees`)
    }
    const totalFees = (await this.convert(assetInboundFee, AssetRuneNative)).plus(runeInboundFee)
    const slip = getSlipOnLiquidity({ asset: params.asset, rune: params.rune }, assetPool)
    const estimateLP: EstimateAddLP = {
      assetPool: assetPool.pool.asset,
      slipPercent: slip.times(100),
      poolShare: poolShare,
      lpUnits: baseAmount(lpUnits),
      runeToAssetRatio: assetPool.runeToAssetRatio,
      inbound: {
        fees: {
          asset: assetInboundFee,
          rune: runeInboundFee,
          total: totalFees,
        },
      },
      estimatedWaitSeconds: waitTimeSeconds,
      errors,
      canAdd: errors.length > 0 ? false : true,
    }
    return estimateLP
  }
"""

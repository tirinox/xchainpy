from datetime import datetime, timedelta

from xchainpy2_utils import DEFAULT_CHAIN_ATTRS, CryptoAmount, Asset, Address, RUNE_DECIMAL, Amount, AssetBTC
from xchainpy2_utils.swap import get_base_amount_with_diff_decimals
from .cache import THORChainCache
from .const import DEFAULT_INTERFACE_ID
from .models import TxDetails, SwapEstimate


class THORChainQuery:
    def __init__(self,
                 cache: THORChainCache = None,
                 chain_attributes=DEFAULT_CHAIN_ATTRS,
                 interface_id=DEFAULT_INTERFACE_ID,
                 native_decimal=RUNE_DECIMAL):
        self.cache = cache
        self.chain_attributes = chain_attributes
        self.interface_id = interface_id
        self.native_decimal = native_decimal

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

            limit = Amount.from_base(lim_asset_amount_8.amount, 8)
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
        # todo...

        if input_coin.asset == destination_asset:
            raise ValueError("input_coin.asset and destination_asset cannot be the same")

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
        pass

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
        pass

    async def get_confirmation_counting(self, input_coin):
        return 0

    async def get_outbound_delay(self, lim_asset_amount):
        return 0

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

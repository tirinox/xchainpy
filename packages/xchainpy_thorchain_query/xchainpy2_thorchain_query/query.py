from xchainpy2_utils import DEFAULT_CHAIN_ATTRS, CryptoAmount, Asset, Address, RUNE_DECIMAL
from .cache import THORChainCache
from .const import DEFAULT_INTERFACE_ID
from .models import TxDetails


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
    ) -> TxDetails:
        return 0

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
            if input_coin.amount.decimal != self.native_decimal:
                raise ValueError(f"input asset "
                                 f"{input_coin.asset!s} "
                                 f"must have decimals of {self.native_decimal}")

        pool = await self.cache.get_pool_for_asset(input_coin.asset)  # todo!
        # todo...

        if input_coin.asset == destination_asset:
            raise ValueError("input_coin.asset and destination_asset cannot be the same")

        return True

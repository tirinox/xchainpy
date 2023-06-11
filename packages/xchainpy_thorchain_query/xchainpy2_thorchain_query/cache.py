import asyncio
import logging
import time
from decimal import Decimal
from itertools import chain
from typing import Dict, List, Optional

from xchainpy2_mayanode import PoolsApi as PoolsApiMaya, MimirApi as MimirApiMaya, NetworkApi as NetworkApiMaya, \
    TransactionsApi as TransactionsApiMaya, LiquidityProvidersApi as LiquidityProvidersApiMaya, \
    QueueApi as QueueApiMaya, QuoteApi as QuoteApiMaya
from xchainpy2_midgard import PoolDetail
from xchainpy2_midgard.api import DefaultApi as MidgardAPI
from xchainpy2_thornode import PoolsApi, MimirApi, NetworkApi, InboundAddress, TransactionsApi, LiquidityProvidersApi, \
    SaversApi, QueueApi, QuoteApi, LastBlock, LiquidityProviderSummary
from xchainpy2_utils import Asset, AssetRUNE, AssetCACAO, Chain, CryptoAmount, RUNE_DECIMAL, CACAO_DECIMAL, Amount, \
    Address, NetworkType
from xchainpy2_utils.swap import get_swap_fee, get_swap_output, get_single_swap, get_double_swap_output, \
    get_double_swap_slip
from .const import Mimir
from .env import URLs
from .midgard import MidgardAPIClient
from .models import PoolCache, InboundDetailCache, NetworkValuesCache, LiquidityPool, InboundDetail, SwapOutput, \
    InboundDetails
from .patch_clients import request_api_with_backup_hosts
from .thornode import ThornodeAPIClient

logger = logging.getLogger('THORChainCache')

SAME_ASSET_EXCHANGE_RATE = 1.0
TEN_MINUTES = 60 * 10

USD_ASSETS = {
    NetworkType.MAINNET: [
        Asset.from_string('BNB.BUSD-BD1'),
        Asset.from_string('ETH.USDC-0XA0B86991C6218B36C1D19D4A2E9EB0CE3606EB48'),
        Asset.from_string('ETH.USDT-0XDAC17F958D2EE523A2206206994597C13D831EC7'),
        Asset.from_string('AVAX.USDC-0XB97EF9EF8734C71904D8002F8B6BC66DD9C48A6E'),
    ],
    NetworkType.STAGENET: [
        Asset.from_string('ETH.USDT-0XDAC17F958D2EE523A2206206994597C13D831EC7')
    ],
    NetworkType.TESTNET: [
        Asset.from_string('BNB.BUSD-74E'),
        Asset.from_string('ETH.USDT-0XA3910454BF2CB59B8B3A401589A3BACC5CA42306')
    ]
}

DEFAULT_MIDGARD = MidgardAPIClient()
DEFAULT_MIDGARD.configuration.host = URLs.Midgard.MAINNET

DEFAULT_THORNODE = ThornodeAPIClient()
DEFAULT_THORNODE.configuration.host = URLs.THORNode.MAINNET


class THORChainCache:
    def __init__(self, midgard_client: MidgardAPIClient = DEFAULT_MIDGARD,
                 thornode_client: ThornodeAPIClient = DEFAULT_THORNODE,
                 expire_pool: float = TEN_MINUTES,
                 expire_inbound: float = TEN_MINUTES,
                 expire_network: float = TEN_MINUTES,
                 native_asset: Asset = AssetRUNE,
                 network: NetworkType = NetworkType.MAINNET):
        self.midgard_client = midgard_client
        self.thornode_client = thornode_client
        self._pool_cache = PoolCache(0, {})
        self._inbound_cache = InboundDetailCache(0, {})
        self._network_cache = NetworkValuesCache(0, {})
        self.expire_pool = expire_pool
        self.expire_inbound = expire_inbound
        self.expire_network = expire_network

        self.native_asset = native_asset
        self.network = network

        self.midgard_api = MidgardAPI(midgard_client)
        self.saver_api: Optional[SaversApi] = None
        if native_asset == AssetRUNE:
            self.t_pool_api = PoolsApi(thornode_client)
            self.mimir_api = MimirApi(thornode_client)
            self.network_api = NetworkApi(thornode_client)
            self.tx_api = TransactionsApi(thornode_client)
            self.lp_api = LiquidityProvidersApi(thornode_client)
            self.queue_api = QueueApi(thornode_client)
            self.saver_api = SaversApi(thornode_client)
            self.quote_api = QuoteApi(thornode_client)
            self.chain = Chain.THORChain
            self.native_decimals = RUNE_DECIMAL
        elif native_asset == AssetCACAO:
            self.t_pool_api = PoolsApiMaya(thornode_client)
            self.mimir_api = MimirApiMaya(thornode_client)
            self.network_api = NetworkApiMaya(thornode_client)
            self.tx_api = TransactionsApiMaya(thornode_client)
            self.lp_api = LiquidityProvidersApiMaya(thornode_client)
            self.queue_api = QueueApiMaya(thornode_client)
            self.saver_api = None  # no savers api for maya?
            self.quote_api = QuoteApiMaya(thornode_client)
            self.chain = Chain.Maya
            self.native_decimals = CACAO_DECIMAL
        else:
            raise ValueError('Invalid native asset. Must be RUNE or CACAO')

    def is_native_asset(self, a: Asset):
        return a == self.native_asset

    async def get_exchange_rate(self, a_from: Asset, a_to: Asset):
        if a_from == a_to:
            return SAME_ASSET_EXCHANGE_RATE
        elif self.is_native_asset(a_from):
            lp_to = await self.get_pool_for_asset(a_to)
            return lp_to.asset_to_rune_ratio
        elif self.is_native_asset(a_to):
            lp_from = await self.get_pool_for_asset(a_from)
            return lp_from.rune_to_asset_ratio
        else:
            lp_from = await self.get_pool_for_asset(a_from)
            lp_to = await self.get_pool_for_asset(a_to)
            return lp_from.rune_to_asset_ratio * lp_to.asset_to_rune_ratio

    async def get_pool_for_asset(self, asset: Asset) -> LiquidityPool:
        if self.is_native_asset(asset):
            raise Exception('Native Rune does not have a pool')
        pool = self._pool_cache.pools.get(str(asset))
        if not pool:
            raise LookupError(f'Pool for {asset} not found')
        return pool

    async def get_pools(self) -> Dict[str, LiquidityPool]:
        time_elapsed = time.monotonic() - self._pool_cache.last_refreshed
        if time_elapsed > self.expire_pool:
            await self.refresh_pool_cache()
        if self._pool_cache.pools:
            return self._pool_cache.pools
        raise LookupError('Could not refresh pools')

    async def refresh_pool_cache(self):
        thornode_pools, midgard_pools = await asyncio.gather(
            request_api_with_backup_hosts(self.t_pool_api, self.t_pool_api.pools),
            request_api_with_backup_hosts(self.midgard_client, self.midgard_api.get_pools)
        )

        if not thornode_pools or not midgard_pools:
            raise LookupError('Could not refresh pools')

        pool_map = {}
        midgard_pools: List[PoolDetail]
        for mdg_pool in midgard_pools:
            thornode_pool = next((p for p in thornode_pools if p.asset == mdg_pool.asset), None)
            if thornode_pool:
                raise LookupError(f'Pool {mdg_pool.asset} not found in both Midgard and THORNode')
            lp = LiquidityPool.from_pool_details(mdg_pool, thornode_pool)
            pool_map[str(lp.asset)] = lp
        self._pool_cache = PoolCache(time.monotonic(), pool_map)

    async def refresh_inbound_cache(self):
        """
        Refreshes the InboundDetailCache Cache
           * NOTE: do not call refresh_inbound_cache() directly, call get_inbound_details() instead
           * which will refresh the cache if it's expired
        """
        mimir, inbound_addresses = await asyncio.gather(
            request_api_with_backup_hosts(self.mimir_api, self.mimir_api.mimir),
            request_api_with_backup_hosts(self.network_api, self.network_api.inbound_addresses)
        )

        inbound_map = {}
        for inbound in inbound_addresses:
            inbound: InboundAddress

            if (
                    not inbound.chain or
                    not inbound.gas_rate or
                    not inbound.gas_rate_units or
                    not inbound.address or
                    not inbound.outbound_fee or
                    not inbound.outbound_tx_size
            ):
                raise LookupError('Missing required inbound info')

            halted = (
                    inbound.halted or
                    # is it necessary?
                    mimir.get(Mimir.HALT_CHAIN_GLOBAL, False) or
                    mimir.get(Mimir.halt_trading(inbound.chain), False)
            )

            halted_trading = (
                    inbound.global_trading_paused or
                    inbound.chain_trading_paused or
                    # is it necessary?
                    mimir.get(Mimir.HALT_TRADING, False) or
                    mimir.get(Mimir.halt_trading(inbound.chain), False)
            )

            halted_lp = (
                    inbound.chain_lp_actions_paused or
                    # is it necessary?
                    mimir.get(Mimir.PAUSE_LP, False) or
                    mimir.get(Mimir.pause_lp(inbound.chain))
            )

            inbound_map[inbound.chain] = InboundDetail(
                chain=Chain(inbound.chain),
                address=inbound.address,
                gas_rate=int(inbound.gas_rate),
                gas_rate_units=inbound.gas_rate_units,
                outbound_fee=int(inbound.outbound_fee),
                outbound_tx_size=int(inbound.outbound_tx_size),
                halted_chain=halted,
                halted_trading=halted_trading,
                halted_lp=halted_lp,
                router=inbound.router,
            )

        inbound_map[Chain.THORChain.value] = InboundDetail(
            chain=Chain.THORChain,
            address='',
            router='',
            gas_rate=0,
            gas_rate_units='',
            outbound_fee=0,
            outbound_tx_size=0,
            halted_chain=False,
            halted_trading=not (mimir.get(Mimir.HALT_TRADING, False)),
            halted_lp=False,
        )

        self._inbound_cache = InboundDetailCache(time.monotonic(), inbound_map)

    async def refresh_network_values(self):
        """
        Refreshes the NetworkValues Cache (Mimir and Constants combined)
        :return: Dict[str, int]
        """
        constants, mimir = await asyncio.gather(
            request_api_with_backup_hosts(self.network_api, self.network_api.constants),
            request_api_with_backup_hosts(self.mimir_api, self.mimir_api.mimir)
        )

        network_values = {}
        for k, v in chain(constants.items(), mimir.items()):
            network_values[k.upper()] = int(v)

        self._network_cache = NetworkValuesCache(time.monotonic(), network_values)

    async def get_network_values(self) -> Dict[str, int]:
        """
        Returns the NetworkValues Cache (Mimir and Constants combined)
        :return:
        """
        sec_since_last_refresh = time.monotonic() - self._network_cache.last_refreshed
        if sec_since_last_refresh > self.expire_network:
            await self.refresh_network_values()

        if not self._network_cache.network_values:
            raise LookupError('Could not refresh network values')

        return self._network_cache.network_values

    async def get_expected_swap_output(self, input_amount: CryptoAmount, dest_asset: Asset) -> SwapOutput:
        swap_output: SwapOutput
        if self.is_native_asset(input_amount.asset):
            # single swap from Rune -> asset
            pool = await self.get_pool_for_asset(dest_asset)
            swap_output = get_single_swap(input_amount, pool, False, self.native_asset)
        elif self.is_native_asset(dest_asset):
            # single swap from asset -> Rune
            pool = await self.get_pool_for_asset(input_amount.asset)
            swap_output = get_single_swap(input_amount, pool, True, self.native_asset)
        else:
            # double swap asset -> asset
            in_pool, out_pool = await asyncio.gather(
                self.get_pool_for_asset(input_amount.asset),
                self.get_pool_for_asset(dest_asset)
            )
            swap_output = await self.get_double_swap(input_amount, in_pool, out_pool)
        # Note this is needed to return a synth vs. a  native asset on swap out
        swap_output.output = CryptoAmount(swap_output.output.amount, dest_asset)
        return swap_output

    async def get_double_swap(self, input_amount, in_pool, out_pool) -> SwapOutput:
        double_output = get_double_swap_output(input_amount, in_pool, out_pool)
        double_fee = await self.get_double_swap_fee(input_amount, in_pool, out_pool)
        double_slip = get_double_swap_slip(input_amount, in_pool, out_pool)
        return SwapOutput(
            output=double_output,
            swap_fee=double_fee,
            slip=double_slip,
        )

    async def get_double_swap_fee(self, input_amount: CryptoAmount,
                                  pool1: LiquidityPool, pool2: LiquidityPool) -> CryptoAmount:
        """
        formula: getSwapFee1 + getSwapFee2
        """
        fee1_in_rune = get_swap_fee(input_amount, pool1, True)
        swap_output = get_swap_output(input_amount, pool1, True)
        fee2_in_asset = get_swap_fee(swap_output, pool2, False)
        fee2_in_rune = await self.convert(fee2_in_asset, self.native_asset)
        return fee1_in_rune + fee2_in_rune

    async def get_decimal_for_asset(self, asset: Asset) -> int:
        if asset == self.native_asset:
            return self.native_decimals
        else:
            pool = await self.get_pool_for_asset(asset)
            decimal = int(pool.thornode_details.decimals)
            return decimal if decimal > 0 else self.native_decimals

    async def convert(self, input_amount: CryptoAmount, out_asset: Asset) -> CryptoAmount:
        """
        Returns the exchange of a CryptoAmount to a different Asset
        Ex. convert(input:100 BUSD, outAsset: BTC) -> 0.0001234 BTC
        :param input_amount: amount/asset to convert to outAsset
        :param out_asset: the Asset you want to convert to
        :return: CryptoAmount of input
        """
        if input_amount.asset == out_asset:
            return input_amount

        exchange_rate = await self.get_exchange_rate(input_amount.asset, out_asset)
        out_decimals = await self.get_decimal_for_asset(out_asset)
        in_decimals = input_amount.amount.decimals
        base_amount_out = input_amount.amount * exchange_rate
        adjust_decimals = out_decimals - in_decimals
        base_amount_out *= Decimal(10 ** adjust_decimals)
        # noinspection PyTypeChecker
        amt = Amount.from_base(int(base_amount_out), out_decimals)
        return CryptoAmount(amt, out_asset)

    async def get_router_address_for_chain(self, chain: Chain) -> Address:
        inbound = await self.get_inbound_details()
        if not inbound[chain.value].router:
            raise Exception('router address is not defined')
        return inbound[chain.value].router

    async def get_inbound_details(self) -> InboundDetails:
        """
        Returns the inbound details for all chains
        :return: inbound details
        """
        time_elapsed = time.monotonic() - self._inbound_cache.last_refreshed
        if time_elapsed > self.expire_inbound:
            await self.refresh_inbound_cache()

        if self._inbound_cache:
            return self._inbound_cache.inbound_details
        else:
            raise Exception('Could not refresh inbound cache')

    async def get_deepest_usd_pool(self) -> LiquidityPool:
        usd_assets = USD_ASSETS[self.network]
        deepest_rune_depth = 0
        deepest_pool = None
        for usd_asset in usd_assets:
            usd_pool = await self.get_pool_for_asset(usd_asset)
            if usd_pool.rune_balance.amount > deepest_rune_depth:
                deepest_rune_depth = usd_pool.rune_balance.amount
                deepest_pool = usd_pool
        if not deepest_pool:
            raise Exception('no USD Pool found')
        return deepest_pool

    @property
    def is_thorchain(self):
        return self.native_asset == AssetRUNE

    @property
    def is_maya(self):
        return self.native_asset == AssetCACAO

    def get_native_block(self, data: LastBlock) -> int:
        key = 'thorchain' if self.is_thorchain else 'mayachain'
        return getattr(data, key)

    async def get_last_block(self) -> List[LastBlock]:
        last_block_obj = await self.network_api.lastblock()
        if not last_block_obj:
            raise ValueError("No last block")
        return last_block_obj

    def get_rune_address(self, lp: LiquidityProviderSummary):
        key = 'rune_address' if self.is_thorchain else 'cacao_address'
        return getattr(lp, key)

    async def get_liquidity_provider(self, asset: str, address: str, height: int = 0) -> LiquidityProviderSummary:
        lps = await self.lp_api.liquidity_providers(asset, height=height)
        return next((lp for lp in lps
                     if lp.asset_address == address or
                     self.get_rune_address(lp) == address),
                    None)

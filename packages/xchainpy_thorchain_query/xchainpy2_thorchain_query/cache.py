import asyncio
import logging
import time
from typing import Dict, List

from xchainpy2_midgard import PoolDetail
from xchainpy2_midgard.api import DefaultApi as MidgardAPI
from xchainpy2_thornode import PoolsApi, MimirApi, NetworkApi, InboundAddress
from xchainpy2_mayanode import PoolsApi as PoolsApiMaya, MimirApi as MimirApiMaya, NetworkApi as NetworkApiMaya
from xchainpy2_utils import Asset, AssetRUNE, AssetCACAO
from .env import Network, URLs
from .midgard import MidgardAPIClient
from .models import PoolCache, InboundDetailCache, NetworkValuesCache, LiquidityPool
from .patch_clients import request_api_with_backup_hosts
from .thornode import ThornodeAPIClient

logger = logging.getLogger('THORChainCache')

SAME_ASSET_EXCHANGE_RATE = 1.0
TEN_MINUTES = 60 * 10

USD_ASSETS = {
    Network.MAINNET: [
        Asset.from_string('BNB.BUSD-BD1'),
        Asset.from_string('ETH.USDC-0XA0B86991C6218B36C1D19D4A2E9EB0CE3606EB48'),
        Asset.from_string('ETH.USDT-0XDAC17F958D2EE523A2206206994597C13D831EC7'),
    ],
    Network.STAGENET: [
        Asset.from_string('ETH.USDT-0XDAC17F958D2EE523A2206206994597C13D831EC7')
    ],
    Network.TESTNET: [
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
                 native_asset: Asset = AssetRUNE):
        self.midgard_client = midgard_client
        self.thornode_client = thornode_client
        self._pool_cache = PoolCache(0, {})
        self._inbound_cache = InboundDetailCache(0, {})
        self._network_cache = NetworkValuesCache(0, {})
        self.expire_pool = expire_pool
        self.expire_inbound = expire_inbound
        self.expire_network = expire_network

        self.native_asset = native_asset

        self.midgard_api = MidgardAPI(midgard_client)
        if native_asset == AssetRUNE:
            self.t_pool_api = PoolsApi(thornode_client)
            self.mimir_api = MimirApi(thornode_client)
            self.network_api = NetworkApi(thornode_client)
        elif native_asset == AssetCACAO:
            self.t_pool_api = PoolsApiMaya(thornode_client)
            self.mimir_api = MimirApiMaya(thornode_client)
            self.network_api = NetworkApiMaya(thornode_client)
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
        mimir, inbound_addresses = await asyncio.gather(
            request_api_with_backup_hosts(self.mimir_api, self.mimir_api.mimir),
            request_api_with_backup_hosts(self.network_api, self.network_api.inbound_addresses)
        )

        inbound_map = {}
        for inbound in inbound_addresses:
            inbound: InboundAddress
            chain = inbound.chain

            # inbound_map[inbound.chain] = inbound
        self._inbound_cache = InboundDetailCache(time.monotonic(), inbound_map)

    async def refresh_network_values(self):
        ...

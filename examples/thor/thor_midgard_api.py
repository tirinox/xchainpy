import asyncio
import logging

from aiohttp_retry import ExponentialRetry

from xchainpy2_midgard.api import DefaultApi as MidgardAPI
from xchainpy2_thorchain_query import MidgardAPIClient, TC_RESERVE_ADDR, URLs
from xchainpy2_thorchain_query.cache import THORChainCache
from xchainpy2_thorchain_query.patch_clients import request_api_with_backup_hosts

logging.basicConfig(level=logging.DEBUG)


async def run_midgard_bad_host():
    mdg = MidgardAPIClient()
    mdg.configuration.host = 'https://noname.com'
    # mdg.configuration.retry_config = ExponentialRetry(1)

    mdg.configuration.backup_hosts = [
        URLs.Midgard.MAINNET,
        URLs.Midgard.THORSWAP,
    ]

    api = MidgardAPI(mdg)
    balance = await request_api_with_backup_hosts(MidgardAPI(mdg), api.get_balance, TC_RESERVE_ADDR)

    # balance = await MidgardAPI(mdg).get_balance(TC_RESERVE_ADDR)
    print(balance)

    await mdg.close()


async def run_midgard_pools():
    mdg = MidgardAPIClient()
    mdg.configuration.host = URLs.Midgard.MAINNET
    mdg.configuration.retry_config = ExponentialRetry(1)

    api = MidgardAPI(mdg)
    pools = await request_api_with_backup_hosts(api, api.get_pools)
    print(f"{type(pools)}: {pools}")
    pools = await api.get_pools()
    print(f"{type(pools)}: {pools}")

    await mdg.close()


async def run_thorchain_cache():
    tc = THORChainCache(expire_pool=10,
                        expire_inbound=10,
                        expire_network=10)
    await tc.refresh_pool_cache()


async def main():
    await run_midgard_pools()
    await run_thorchain_cache()


asyncio.run(main())

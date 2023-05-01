import asyncio

import xchainpy2_thornode as thor
import xchainpy2_mayanode as maya
from xchainpy2_thorchain_query import URLs


async def try_thornode():
    api_client = thor.ApiClient()
    api_client.configuration.host = URLs.THORNode.MAINNET
    pol = thor.POLApi(api_client)
    r = await pol.pol()
    print(f"{type(r)}: {r}")

    t_pool_api = thor.PoolsApi(api_client)

    r = await t_pool_api.pools()
    print(f"{type(r)}: {r}")

    mimir = thor.MimirApi(api_client)
    r = await mimir.mimir()
    print(f"{type(r)}: {r}")

    await api_client.rest_client.pool_manager.close()


async def try_mayanode():
    api_client = maya.ApiClient()
    api_client.configuration.host = URLs.THORNode.MAYACHAIN
    mimir = maya.MimirApi(api_client)
    r = await mimir.mimir()
    print(r)

    buckets = maya.BucketsApi(api_client)
    r = await buckets.buckets()
    print(r)

    await api_client.rest_client.pool_manager.close()


async def main():
    await try_thornode()
    await try_mayanode()


if __name__ == '__main__':
    asyncio.run(main())

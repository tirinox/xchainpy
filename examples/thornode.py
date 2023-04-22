import asyncio

import xchainpy2_thornode as thor
import xchainpy2_mayanode as maya


async def try_thornode():
    api_client = thor.ApiClient()
    api_client.configuration.host = 'https://thornode.ninerealms.com'
    pol = thor.POLApi(api_client)
    r = await pol.pol()
    print(r)

    mimir = thor.MimirApi(api_client)
    r = await mimir.mimir()
    print(r)

    await api_client.rest_client.pool_manager.close()


async def try_mayanode():
    api_client = maya.ApiClient()
    api_client.configuration.host = 'https://mayanode.mayachain.info/'
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

import asyncio

import mayanode_client
import thornode_client


async def try_thornode():
    api_client = thornode_client.ApiClient()
    api_client.configuration.host = 'https://thornode.ninerealms.com'
    pol = thornode_client.POLApi(api_client)
    r = await pol.pol()
    print(r)

    mimir = thornode_client.MimirApi(api_client)
    r = await mimir.mimir()
    print(r)

    await api_client.rest_client.pool_manager.close()


async def try_mayanode():
    api_client = mayanode_client.ApiClient()
    api_client.configuration.host = 'https://mayanode.mayachain.info/'
    mimir = mayanode_client.MimirApi(api_client)
    r = await mimir.mimir()
    print(r)

    buckets = mayanode_client.BucketsApi(api_client)
    r = await buckets.buckets()
    print(r)

    await api_client.rest_client.pool_manager.close()


async def main():
    await try_mayanode()


if __name__ == '__main__':
    asyncio.run(main())

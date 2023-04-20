import asyncio

from thornode_client import *


async def main():
    api_client = ApiClient()
    api_client.configuration.host = 'http://thornode.ninerealms.com'
    pol = POLApi(api_client)
    r = await pol.pol()
    print(r)

    mimir = MimirApi(api_client)
    r = await mimir.mimir()
    print(r)

    # Close aiohttp session
    await api_client.rest_client.pool_manager.close()


if __name__ == '__main__':
    asyncio.run(main())

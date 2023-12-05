import asyncio

import xchainpy2_mayanode as maya
from xchainpy2_thorchain_query import URLs


async def try_mayanode():
    api_client = maya.ApiClient()
    api_client.configuration.host = URLs.THORNode.MAYACHAIN

    health = maya.HealthApi(api_client)
    r = await health.ping()
    print(f'Maya Health: {r}')

    mimir = maya.MimirApi(api_client)
    r = await mimir.mimir()
    print(f'Maya Mimir: {r}')

    net_api = maya.NetworkApi(api_client)
    r = await net_api.network()
    print(f'Maya Network: {r}')

    nodes_api = maya.NodesApi(api_client)
    r = await nodes_api.nodes()
    print(f'Maya Nodes: {r}')

    await api_client.rest_client.pool_manager.close()


async def main():
    await try_mayanode()


if __name__ == '__main__':
    asyncio.run(main())

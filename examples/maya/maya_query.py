import asyncio

from xchainpy2_thorchain_query import THORChainQuery


async def main():
    query = THORChainQuery()
    await query.close()


asyncio.run(main())

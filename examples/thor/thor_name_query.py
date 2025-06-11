import asyncio

from xchainpy2_thorchain_query import THORChainQuery


async def main():
    query = THORChainQuery()

    details = await query.cache.get_name_details('t')
    print(f"THORName 't' details: {details}")

    test_address = 'thor1wpehtkayhru2q2j9lj800taqsud6qs8dwe585k'
    thor_names = await query.cache.get_names_with_details(test_address)
    print(f"Address {test_address!r} has THORNames: {thor_names}")

    await query.close()


asyncio.run(main())

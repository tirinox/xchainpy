import asyncio

from xchainpy2_thorchain_query import THORChainQuery


async def main():
    query = THORChainQuery()

    details = await query.cache.get_name_details('t')
    print(f"THORName 't' details: {details}")

    thor_names = await query.cache.get_names_with_details('thor160yye65pf9rzwrgqmtgav69n6zlsyfpgm9a7xk')
    print(f"Address 'thor160yye65pf9rzwrgqmtgav69n6zlsyfpgm9a7xk' has THORNames: {thor_names}")

    await query.close()


asyncio.run(main())

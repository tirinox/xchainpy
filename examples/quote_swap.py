import asyncio

from xchainpy2_thorchain_query import THORChainQuery
from xchainpy2_utils import Amount, AssetRUNE


async def main():
    query = THORChainQuery()

    q_swap = await query.quote_swap(
        'thor1z9xhmhtxn5gxd4ugfuxk7hg9hp03tw3qtqs3f3',
        Amount.from_asset(10000.0),
        AssetRUNE,
        '1KGMxAw3rxKvR4ECioUBtYFbgZRVFrDX2n',
        'BTC.BTC',
        1000,
        affiliate_bps=20,
        affiliate_address='thor1xnj33ppdvzf0gqk5gx2jqe9t3f5vdmvxuy7xc7',
    )
    print(q_swap)


if __name__ == "__main__":
    asyncio.run(main())

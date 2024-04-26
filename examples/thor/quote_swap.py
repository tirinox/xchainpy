import asyncio

from examples.common import sep
from xchainpy2_bitcoin import BTC_DECIMAL
from xchainpy2_thorchain_query import THORChainQuery
from xchainpy2_utils import Amount, AssetRUNE, AssetBTC, AssetETH, CryptoAmount


async def main():
    query = THORChainQuery()

    q_swap = await query.quote_swap(
        CryptoAmount(Amount.from_asset(10000.0), AssetRUNE),
        '1KGMxAw3rxKvR4ECioUBtYFbgZRVFrDX2n',
        'BTC.BTC',
        1000,
        affiliate_bps=20,
        affiliate_address='thor1xnj33ppdvzf0gqk5gx2jqe9t3f5vdmvxuy7xc7',
    )
    print("Swap Rune to BTC:")
    print(q_swap)

    sep()  # ------------------------------------

    btc_swap = await query.quote_swap(
        CryptoAmount(Amount.from_asset(1.0, BTC_DECIMAL), AssetBTC),
        destination_address='0xae2fc483527b8ef99eb5d9b44875f005ba1fae13',
        destination_asset=AssetETH,
        tolerance_bps=500,
        affiliate_bps=30,
        affiliate_address='t'
    )
    print("Swap BTC to ETH:")
    print(btc_swap)

    await query.close()


if __name__ == "__main__":
    asyncio.run(main())

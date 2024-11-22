import asyncio

from examples.common import sep
from xchainpy2_bsc import AssetBSC_USDT
from xchainpy2_thorchain_query import THORChainQuery
from xchainpy2_utils import Amount, CryptoAmount, AssetBSC, AssetBTC


async def main():
    query = THORChainQuery()

    quote = await query.estimate_add_saver(
        CryptoAmount(Amount.from_asset(200.0), AssetBSC),
    )
    print("Add Saver:")
    print(quote)

    sep()  # ------------------------------------

    quote = await query.estimate_add_saver(
        CryptoAmount(Amount.from_asset(3.0), AssetBTC),
    )
    print("Add Saver:")
    print(quote)

    sep()  # ------------------------------------

    # Should fail because there is no pool for BSC/USDT at the moment
    quote = await query.estimate_add_saver(
        CryptoAmount(Amount.from_asset(5000.0), AssetBSC_USDT),
    )
    print("Add Saver should fail:")
    print(quote)

    await query.close()


if __name__ == "__main__":
    asyncio.run(main())

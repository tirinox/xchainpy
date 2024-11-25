import asyncio

from examples.common import sep
from xchainpy2_bsc import AssetBSC_USDT
from xchainpy2_thorchain_query import THORChainQuery
from xchainpy2_utils import Amount, CryptoAmount, AssetBSC, AssetBTC


async def demo_quote_add(query):
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

    sep()  # ------------------------------------


async def demo_withdraw(query):
    quote = await query.estimate_withdraw_saver(
        # fixme: intentionally using wrong address to get an error
        AssetBTC, 'bc1p5d7rjq7g6rdk2yhzks9smlaqtedr4dekq08ge8ztwac72sfr9rusxg3297', 5000
    )
    print("Withdraw Saver:")
    print(quote)

    sep()  # ------------------------------------

    quote = await query.estimate_withdraw_saver(
        AssetBTC, 'bc1q7wath0z82x9yxzztv04qndu803uc74ysru6xvz', 5000
    )
    print("Withdraw Saver:")
    print(quote)

    sep()  # ------------------------------------


async def demo_get_saver_positions(query):

    position = await query.get_saver_position(
        'bc1q7wath0z82x9yxzztv04qndu803uc74ysru6xvz', AssetBTC
    )
    print("Saver Position:")
    print(position)

    sep()  # ------------------------------------


async def main():
    query = THORChainQuery()

    # await demo_quote_add(query)
    # await demo_withdraw(query)
    await demo_get_saver_positions(query)

    await query.close()


if __name__ == "__main__":
    asyncio.run(main())

import asyncio

from xchainpy2_thorchain_query import THORChainQuery
from xchainpy2_utils import AssetBTC, CryptoAmount, AssetETH


async def main():
    query = THORChainQuery()

    result = await query.get_pool_ratio(AssetBTC)
    print(f"Pool ratio for {AssetBTC}: {result}")

    input_amount = CryptoAmount.auto(0.5, AssetBTC)
    target_asset = AssetETH

    conv_res = await query.convert(input_amount, target_asset)
    print(f"I calculated that if you swap {input_amount} to {target_asset}, you probably get: {conv_res}")

    quote_res = await query.quote_swap(input_amount, "0x0074e26798Cd93bFc87917648cDec88CCe39669c",
                                       target_asset)
    print(f"Quote swap result: {quote_res.net_output}")

    await query.close()


asyncio.run(main())

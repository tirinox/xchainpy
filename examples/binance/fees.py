import asyncio

from xchainpy2_binance import BinanceChainClient


async def main():
    bnb = BinanceChainClient()

    fees = await bnb.get_fees()
    print(fees)


asyncio.run(main())

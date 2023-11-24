import asyncio

from xchainpy2_binance import BinanceChainClient


async def main():
    bnb = BinanceChainClient()

    fees = await bnb.get_fees()
    print(fees)

    balances = await bnb.get_balance('bnb17g92armmr926kd88umh7u90vglq4ghjtku6ssc')  # random address with tokens
    print(balances)


asyncio.run(main())

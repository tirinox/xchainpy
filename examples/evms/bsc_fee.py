import asyncio

from xchainpy2_bsc import BinanceSmartChainClient


async def main():
    cli = BinanceSmartChainClient()
    fee = await cli.get_last_fee()
    print(f'Last fee: {fee}')

    fees = await cli.get_fees()
    print(f'Fees: {fees}')


if __name__ == '__main__':
    asyncio.run(main())

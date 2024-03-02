import asyncio

from xchainpy2_bitcoin import BitcoinClient


async def main():
    btc = BitcoinClient()

    fees = await btc.get_fees()
    print(fees)


if __name__ == '__main__':
    asyncio.run(main())

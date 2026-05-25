import asyncio

from xchainpy2_bitcoincash import BitcoinCashClient
from xchainpy2_client import FeeOption


async def main():
    btc = BitcoinCashClient()

    fees = await btc.get_fees()
    print(fees)

    fastest_fee_rate = fees.select_as_int(FeeOption.FASTEST)
    print(f"Fastest fee rate: {fastest_fee_rate} sat/vB")


if __name__ == '__main__':
    asyncio.run(main())

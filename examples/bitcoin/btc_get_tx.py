import asyncio

from xchainpy2_bitcoin import BitcoinClient


async def main():
    btc = BitcoinClient()
    # swap
    tx = await btc.get_transaction_data('49618585E89A9DC4CC4C4A747AB9F6EE592C358BF6B29D4442A66366536C18A5')
    print(tx)


if __name__ == '__main__':
    asyncio.run(main())

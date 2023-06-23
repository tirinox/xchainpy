import asyncio
import logging
from pprint import pprint

from xchainpy2_cosmos import CosmosGaiaClient


async def demo_read_txs():
    demo_addy = 'cosmos1lxum6akwxgmvkcj5gut6vn85an2r428v7n92u5'

    client = CosmosGaiaClient()

    balance = await client.get_balance(demo_addy)
    pprint(balance)

    txs = await client.search_tx(message_sender=demo_addy)
    print(txs)


async def main():
    await demo_read_txs()


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    asyncio.run(main())

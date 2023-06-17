import asyncio

from xchainpy2_cosmos import CosmosGaiaClient


async def demo_read_txs():
    client = CosmosGaiaClient()
    txs = await client.search_tx(message_sender='cosmos1f9ta55rme2mwy9nwugzp5r9rl9h54a70yf8nfz')
    print('txs', txs)


async def main():
    await demo_read_txs()


if __name__ == '__main__':
    asyncio.run(main())

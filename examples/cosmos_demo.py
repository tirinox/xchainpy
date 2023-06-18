import asyncio

from xchainpy2_cosmos import CosmosGaiaClient


async def demo_read_txs():
    demo_addy = 'cosmos1f9ta55rme2mwy9nwugzp5r9rl9h54a70yf8nfz'

    client = CosmosGaiaClient(client_urls='https://api.cosmos.network')

    balance = await client.get_balance(demo_addy)
    print(balance)

    txs = await client.search_tx(message_sender=demo_addy)
    print('txs', txs)


async def main():
    await demo_read_txs()


if __name__ == '__main__':
    asyncio.run(main())

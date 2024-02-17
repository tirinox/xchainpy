import asyncio
import logging
from pprint import pprint

from xchainpy2_cosmos import CosmosGaiaClient


async def demo_read_txs():
    # random address from the explorer
    demo_addy = 'cosmos1vmnszddr75huvt7fcvx7nuvk7vje4qmxe9zc0u'

    client = CosmosGaiaClient()

    account = await client.get_account(demo_addy)
    pprint(account)

    balance = await client.get_balance(demo_addy)
    pprint(balance)

    tx_id = '72EF6969FACFAD016385BF1E0A0223D6522859E65AC767C27A5D1B6CB61A24A9'
    tx_data = await client.get_transaction_data(tx_id=tx_id)

    print(tx_data)

    txs = await client.search_tx_from_rpc(message_sender=demo_addy)
    print(txs)


async def main():
    await demo_read_txs()


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    asyncio.run(main())

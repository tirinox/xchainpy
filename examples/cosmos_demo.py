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

    txs = await client.search_tx(message_sender=demo_addy)
    print(txs)

    # tx_id = txs.tx_responses[0].txhash
    tx_id = '95759DFC5641143887A0064FDEF8BA3AC2F0F90DFF39BC4EF17B2DD3CBA3C917'
    tx_data = await client.get_transaction_data(tx_id=tx_id)
    print(tx_data)


async def main():
    await demo_read_txs()


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    asyncio.run(main())

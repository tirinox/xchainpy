import asyncio
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

    tx_id = 'AA3E2DCF40914416F83D16B16A9E85207E92369F9208CC6864A95F7710576947'
    tx_data = await client.get_transaction_data(tx_id=tx_id)

    print(tx_data)

    txs = await client.search_tx_from_rpc(message_sender=demo_addy)
    print(txs)


async def main():
    await demo_read_txs()


if __name__ == '__main__':
    # logging.basicConfig(level=logging.DEBUG)
    asyncio.run(main())

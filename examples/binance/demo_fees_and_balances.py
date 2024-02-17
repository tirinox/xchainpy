import asyncio

from examples.common import sep
from xchainpy2_binance import BinanceChainClient

TX_ID_SEND = 'D9168C1839259415ABDD98613E3FDB9DE01CF4F6D6AC03451F0E1A7262F18705'
TX_ID_SWAP = '720C118E02EF99CA3AE95909C7AD26905E3388B041ACED7A7B97C7D26A9CB439'


async def main():
    bnb = BinanceChainClient()

    txs = await bnb.get_transactions('bnb1f578ardgqq3gk9mamsr07g2a3ras6j3x8fg6uh', detailed=True)
    print(txs)
    sep()

    tx = await bnb.get_transaction_data(TX_ID_SEND)
    print(tx)
    sep()

    tx = await bnb.get_transaction_data(TX_ID_SWAP)
    print(tx)

    await bnb.close()


asyncio.run(main())

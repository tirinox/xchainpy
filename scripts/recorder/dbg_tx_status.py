import os
import asyncio

from scripts.recorder.recorder import TxStatusRecorder
from xchainpy2_thorchain_query import THORChainQuery
from xchainpy2_wallet import Wallet


async def run_tracker(tx_hash):
    query = THORChainQuery()

    tracker = query.tracker()

    # r = await tracker.tc_get_tx_status(tx_hash)
    # print(r)

    rec = TxStatusRecorder(tx_hash, query.tracker())
    await rec.load_db()

    # await rec.scan(18401899 - 200, 18401899 + 200)

    # await rec.save_db()

    # rec.clear_identical_states()
    #
    for block in rec.block_list:
        print('-' * 80)
        print(f'Block: #{block}')
        print(rec[block])
        input()

    # await rec.get_tx_status(18402326)
    # await rec.get_tx_status(18402336)
    # await rec.save_db()

    rec.print_db_map()


if __name__ == '__main__':
    asyncio.run(run_tracker('53A1BC9E7B45819452F53A09A8D9C3C49F7D4A81D933F90759F6D92249ABB609'))

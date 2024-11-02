import os
import asyncio
from xchainpy2_thorchain_query import THORChainQuery
from xchainpy2_wallet import Wallet


async def run_tracker(tx_hash):
    query = THORChainQuery()

    tracker = query.tracker()

    r = await tracker.tc_get_tx_status(tx_hash)
    print(r)


if __name__ == '__main__':
    asyncio.run(run_tracker('FBFB61966DB8F633BF8A489167E407C23F726A1D863B41D85169C43E3773F201'))

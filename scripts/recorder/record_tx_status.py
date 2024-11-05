import asyncio
import os

from examples.common import sep
from scripts.recorder.recorder import TxStatusRecorder
from xchainpy2_thorchain_query import TransactionTracker, THORChainQuery
from xchainpy2_utils import Chain
from xchainpy2_wallet import Wallet


async def run_tracker(tx_hash, in_chain: Chain, out_chain: Chain, start_block, end_block):
    query = THORChainQuery()
    wallet = Wallet(phrase=os.environ.get('PHRASE'),
                    enabled_chains=[
                        in_chain, out_chain
                    ])

    rec = TxStatusRecorder(tx_hash, query.tracker(wallet, in_chain, out_chain))
    await rec.load_db()

    await rec.scan(start_block, end_block)

    # sep('Poll')
    # async for status in rec.tracker.poll(tx_hash, interval=0.1):
    #     print(status)


async def case_swap_out_2_out():
    await run_tracker(
        tx_hash='FBFB61966DB8F633BF8A489167E407C23F726A1D863B41D85169C43E3773F200',
        in_chain=Chain.BitcoinCash,
        out_chain=Chain.Avalanche,
        start_block=18402326 - 200,
        end_block=18402326 + 200,
    )


async def case_swap_tc_2_out():
    await run_tracker(
        tx_hash='',
        in_chain=Chain.Ethereum,
        out_chain=Chain.Bitcoin,
        start_block=0,
        end_block=0,
    )


async def case_swap_out_2_tc():
    await run_tracker(
        tx_hash='',
        in_chain=Chain.Ethereum,
        out_chain=Chain.Bitcoin,
        start_block=0,
        end_block=0,
    )


async def case_add_liqudity():
    await run_tracker(
        tx_hash='',
        in_chain=Chain.Ethereum,
        out_chain=Chain.Bitcoin,
        start_block=0,
        end_block=0,
    )


async def case_withdraw_liquidity():
    await run_tracker(
        tx_hash='',
        in_chain=Chain.Ethereum,
        out_chain=Chain.Bitcoin,
        start_block=0,
        end_block=0,
    )


if __name__ == '__main__':
    call = case_swap_out_2_out()
    asyncio.run(call)

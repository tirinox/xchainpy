import asyncio

from aiohttp_retry import ExponentialRetry

from xchainpy2_midgard.api import DefaultApi as MidgardAPI
from xchainpy2_thorchain_query import MidgardAPIClient, TC_RESERVE_ADDR, URLs


async def run_midgard_protected():
    mdg = MidgardAPIClient()
    mdg.configuration.host = 'https://noname.com'
    mdg.configuration.retry_config = ExponentialRetry(1)
    mdg.configuration.backup_hosts = [
        URLs.Midgard.MAINNET,
        URLs.Midgard.THORSWAP,
    ]

    balance = await MidgardAPI(mdg).get_balance(TC_RESERVE_ADDR)
    print(balance)

    await mdg.close()


async def main():
    await run_midgard_protected()


asyncio.run(main())

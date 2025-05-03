import asyncio
import os.path
import sys

import aiofiles
import yaml

from examples.common import get_phrase
from xchainpy2_thorchain_amm import THORChainAMM
from xchainpy2_thorchain_query import THORChainQuery
from xchainpy2_utils import Chain
from xchainpy2_wallet import Wallet


async def load_config():
    config_file = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(__file__), "tcy_bot_config.yaml")
    async with aiofiles.open(config_file, mode='r') as f:
        content = await f.read()
    return yaml.safe_load(content)


async def main():
    cfg = await load_config()

    phrase = cfg['thor']['phrase']
    query = THORChainQuery.from_thornode_and_midgard(
        thornode_url=cfg['thor']['node_url'],
        midgard_url=cfg['thor']['midgard_url'],
    )

    wallet = Wallet(phrase, query, enabled_chains=Chain.THORChain)

    amm = THORChainAMM(wallet)

    balances = await wallet.get_all_balances()
    print(balances)

    await amm.close()
    await wallet.close()


if __name__ == "__main__":
    asyncio.run(main())

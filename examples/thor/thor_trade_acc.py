"""
This example demonstrates how to trade deposit and withdraw Trade Assets on the THORChain network.
Just don't forget to pass PHRASE environment variable that contains a mnemonic phrase of your wallet.
"""

import asyncio
import os

from xchainpy2_thorchain_amm import Wallet, THORChainAMM
from xchainpy2_utils import Chain


async def main(seed_phrase):
    wallet = Wallet(seed_phrase, enabled_chains={Chain.THORChain, Chain.Binance, Chain.Cosmos})
    async with THORChainAMM(wallet) as amm:
        # balances = await wallet.get_all_balances()
        # print(f"Balances: {balances}")

        # await thorchain_wait_tx_status(amm, tx_hash)

        tr_balance = await wallet.get_client(Chain.THORChain).get_trade_asset_balance(
            'thor14mh37ua4vkyur0l5ra297a4la6tmf95mt96a55')
        print(tr_balance)

        await amm.close()


if __name__ == "__main__":
    phrase = os.environ.get('PHRASE')
    if not phrase:
        raise Exception('Please pass PHRASE environment variable to run this example!')

    asyncio.run(main(phrase))

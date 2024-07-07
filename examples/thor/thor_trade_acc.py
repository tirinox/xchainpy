"""
This example demonstrates how to trade deposit and withdraw Trade Assets on the THORChain network.
Just don't forget to pass PHRASE environment variable that contains a mnemonic phrase of your wallet.
"""

import asyncio
import os

from examples.common import thorchain_wait_tx_status
from xchainpy2_thorchain_amm import Wallet, THORChainAMM
from xchainpy2_utils import Chain, CryptoAmount, AssetLTC


async def main(seed_phrase):
    wallet = Wallet(seed_phrase, enabled_chains={
        Chain.THORChain,
        Chain.Avalanche,
        Chain.Cosmos,
        Chain.Litecoin,
        Chain.BinanceSmartChain
    })
    async with THORChainAMM(wallet) as amm:
        balances = await wallet.get_all_balances()
        print(f"Balances: {balances}")

        tx_hash = await amm.deposit_to_trade_account(
            CryptoAmount.automatic(0.05, AssetLTC),
        )

        await thorchain_wait_tx_status(amm, tx_hash)

        await amm.close()


if __name__ == "__main__":
    phrase = os.environ.get('PHRASE')
    if not phrase:
        raise Exception('Please pass PHRASE environment variable to run this example!')

    asyncio.run(main(phrase))

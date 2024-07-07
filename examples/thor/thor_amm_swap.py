import asyncio
import os

from xchainpy2_thorchain_amm import Wallet, THORChainAMM
from xchainpy2_thorchain_query import TxDetails
from xchainpy2_utils import Chain, CryptoAmount, AssetATOM, AssetRUNE


async def main(seed_phrase):
    """
    This example requires a real wallet with some amount of Rune
    (1 Rune will be more than enough)
    Just don't forget to pass PHRASE environment variable that contains a mnemonic phrase of your wallet
    """
    wallet = Wallet(seed_phrase, enabled_chains={Chain.THORChain, Chain.Binance, Chain.Cosmos})
    amm = THORChainAMM(wallet)

    balances = await wallet.get_all_balances()
    print(f"Balances: {balances}")

    # tx_hash = await amm.do_swap(
    #     CryptoAmount.automatic("1.5", 'THOR.RUNE'),
    #     AssetATOM,
    #     tolerance_bps=3000,
    # )
    tx_hash = await amm.do_swap(
        CryptoAmount.automatic("1.38", AssetATOM),
        AssetRUNE,
        tolerance_bps=3000,
    )

    print(f"Swap has been broadcast. TX hash is {tx_hash}, {wallet.explorer_url_tx(tx_hash)}")

    tracker = amm.tracker()
    async for status in tracker.poll(tx_hash):
        status: TxDetails
        print(f'Status: {status.status}; stage: {status.stage}')

    await amm.close()


if __name__ == "__main__":
    phrase = os.environ.get('PHRASE')
    if not phrase:
        raise Exception('Please pass PHRASE environment variable to run this example!')

    asyncio.run(main(phrase))

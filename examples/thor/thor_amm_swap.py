import asyncio
import os

from xchainpy2_thorchain_amm import Wallet, THORChainAMM
from xchainpy2_thorchain_query import TransactionTracker
from xchainpy2_utils import CryptoAmount, AssetAVAX, Chain, AssetBNB, AssetATOM, Asset


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

    tx_hash = await amm.do_swap(
        CryptoAmount.automatic("2.0", 'THOR.RUNE'),
        Asset.from_string('BNB.BUSD-bd1'),
        tolerance_bps=1000,
    )
    print(f"Swap tx hash: {tx_hash}, {wallet.explorer_url_tx(tx_hash)}")

    tracker = amm.tracker()
    async for status in tracker.poll(tx_hash):
        print(f'Status: {status}')

    await wallet.close()


if __name__ == "__main__":
    phrase = os.environ.get('PHRASE')
    if not phrase:
        raise Exception('Please pass PHRASE environment variable to run this example!')

    asyncio.run(main(phrase))

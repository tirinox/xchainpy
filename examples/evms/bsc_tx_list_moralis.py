import asyncio
from pprint import pprint

from xchainpy2_bsc import BinanceSmartChainClient


# To run this script you need to install the following peer dependencies:
#    pip install moralis
# Then set MORALIS_API_KEY env var to your Moralis API key.
# Example:
#   MORALIS_API_KEY=your_moralis_api_key python examples/bsc/bsc_tx_list_moralis.py

async def main():
    import os
    phrase = os.environ.get('PHRASE')
    if not phrase:
        raise ValueError("PHRASE env var is empty!")

    cli = BinanceSmartChainClient(phrase=phrase)

    txs = await cli.get_transactions()

    pprint(txs)


if __name__ == '__main__':
    asyncio.run(main())

import asyncio

from examples.common import get_phrase
from xchainpy2_bitcoin import BitcoinClient
from xchainpy2_utils import NetworkType


async def main():
    phrase = get_phrase()
    # btc = BitcoinClient(phrase=phrase, network=NetworkType.DEVNET, provider_names=[])
    btc = BitcoinClient(phrase=phrase, network=NetworkType.TESTNET)
    print(f"BTC Address: {btc.get_address()}")

    balance = await btc.get_balance()
    print(f"Balance: {balance}")

    utxos = await btc.get_utxos()
    print(utxos)


if __name__ == '__main__':
    asyncio.run(main())

import asyncio

from examples.common import get_phrase
from xchainpy2_litecoin import LitecoinClient
from xchainpy2_utils import NetworkType


async def main():
    # Create a new client
    phrase = get_phrase()

    provider_names = []

    ltc = LitecoinClient(phrase=phrase, network=NetworkType.TESTNET, provider_names=provider_names)
    ltc2 = LitecoinClient(phrase=phrase, network=NetworkType.TESTNET, wallet_index=1, provider_names=provider_names)

    # Get the balance of the LTC wallet
    balance = await ltc.get_balance()
    print(f"Balance 1 ({ltc.get_address()}): {balance}")


asyncio.run(main())

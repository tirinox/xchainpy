import asyncio

from examples.common import get_phrase
from xchainpy2_litecoin import LitecoinClient
from xchainpy2_utils import NetworkType


async def main():
    # Create a new client
    phrase = get_phrase()

    provider_names = ['cryptoid', 'blockcypher', 'blockchair']

    ltc = LitecoinClient(phrase=phrase, network=NetworkType.MAINNET, provider_names=provider_names)
    ltc2 = LitecoinClient(phrase=phrase, network=NetworkType.MAINNET, wallet_index=1, provider_names=provider_names)

    # Get the balance of the LTC wallet
    balance1 = await ltc.get_balance()
    print(f"Balance 1 ({ltc.get_address()}): {balance1}")

    balance2 = await ltc2.get_balance()
    print(f"Balance 2 ({ltc2.get_address()}): {balance2}")

    if balance2 > balance1:
        print('Swapping addresses')
        ltc, ltc2 = ltc2, ltc

    tx = await ltc.transfer(ltc.gas_amount('0.0002'), ltc2.get_address(), memo='test')
    print(f"TX 1: {tx}; {ltc2.get_explorer_tx_url(tx)}")


asyncio.run(main())

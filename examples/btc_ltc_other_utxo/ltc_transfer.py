import asyncio

from examples.common import get_phrase
from xchainpy2_litecoin import LitecoinClient
from xchainpy2_utils import NetworkType


def create_ltc_client(phrase: str, network: NetworkType = NetworkType.MAINNET, wallet_index: int = 0):
    # url = 'https://litecoin.ninerealms.com'
    url = ''
    return LitecoinClient(phrase=phrase, network=network, wallet_index=wallet_index,
                          daemon_url=url)


async def main():
    # Create a new client
    phrase = get_phrase()

    ltc = create_ltc_client(phrase)
    ltc2 = create_ltc_client(phrase, wallet_index=1)

    providers = ltc.get_available_provider_names()
    print(f"Available providers: {providers}")

    ltc.recreate_service_with_providers(providers)

    # Get the balance of the LTC wallet
    show_balance = True
    if show_balance:
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

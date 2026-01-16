import asyncio

from examples.common import get_phrase
from xchainpy2_dogecoin import DogecoinClient
from xchainpy2_utils import NetworkType

DRY_RUN = True


def create_doge_client(phrase: str, network: NetworkType = NetworkType.MAINNET, wallet_index: int = 0):
    return DogecoinClient(phrase=phrase, network=network, wallet_index=wallet_index)


async def main():
    # Create a new client
    phrase = get_phrase()

    doge = create_doge_client(phrase)
    doge2 = create_doge_client(phrase, wallet_index=1)

    fees = await doge.get_fees()
    print(f"Current Doge fees: {fees}")

    providers = doge.get_available_provider_names()
    print(f"Available providers: {providers}")

    doge.recreate_service_with_providers(providers)
    doge2.recreate_service_with_providers(providers)

    # Get the balance of the Doge wallet
    show_balance = True
    if show_balance:
        balance1 = await doge.get_balance()
        print(f"Balance 1 ({doge.get_address()}): {balance1}")

        balance2 = await doge2.get_balance()
        print(f"Balance 2 ({doge2.get_address()}): {balance2}")

        if balance2 > balance1:
            print('Swapping addresses')
            doge, doge2 = doge2, doge

    tx = await doge.transfer(doge.gas_amount('0.02'), doge2.get_address(), memo='test', dry_run=DRY_RUN)
    print(f"TX 1: {tx}; {doge2.get_explorer_tx_url(tx)}")


asyncio.run(main())

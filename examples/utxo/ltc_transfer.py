import asyncio
import os

from examples.common import get_phrase
from xchainpy2_litecoin import LitecoinClient

DRY_RUN = False
SHOW_BALANCE = False
# LITECOIND_URL = 'https://litecoin.ninerealms.com/'
LITECOIND_URL = os.environ.get("LITECOIND_URL")


async def main():
    # Create a new client
    phrase = get_phrase()

    ltc = LitecoinClient(phrase=phrase, daemon_url=LITECOIND_URL)
    ltc2 = LitecoinClient(phrase=phrase, wallet_index=1, daemon_url=LITECOIND_URL)

    providers = ltc.get_available_provider_names()
    print(f"Available providers: {providers}")

    fees = await ltc.get_fees()
    print(f"Fees: {fees}")

    if SHOW_BALANCE:
        # Get the balance of the LTC wallet
        balance1 = await ltc.get_balance()
        print(f"Balance 1 ({ltc.get_address()}): {balance1}")

        balance2 = await ltc2.get_balance()
        print(f"Balance 2 ({ltc2.get_address()}): {balance2}")

        if balance2 > balance1:
            print('Swapping addresses')
            ltc, ltc2 = ltc2, ltc

    tx = await ltc.transfer(ltc.gas_amount('0.0002'), ltc2.get_address(), memo='test', dry_run=DRY_RUN)
    print(f"TX hash: {tx}; {ltc2.get_explorer_tx_url(tx)}")


asyncio.run(main())

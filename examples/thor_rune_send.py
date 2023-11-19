import asyncio
import os

from bech32 import bech32_decode, bech32_encode
from cosmpy.crypto.address import Address

from xchainpy2_thorchain import THORChainClient
from xchainpy2_thorchain_query import RUNE_NETWORK_FEE
from xchainpy2_utils import CryptoAmount, Amount, NetworkType, RUNE_DECIMAL, AssetRUNE

"""
This example requires a real wallet with some amount of Rune
(5 Cacao will be more than enough)
Just don't forget to pass "PHRASE" environment variable that contains a mnemonic phrase of your wallet
"""

NETWORK = NetworkType.MAINNET


async def main():
    phrase = os.environ.get('PHRASE')
    if not phrase:
        raise ValueError("PHRASE env var is empty!")

    client = THORChainClient(phrase=phrase, network=NETWORK)

    balance = await client.get_balance()
    print(f"{client.get_address()}'s balance is {balance}")

    dest_address = client.get_address(1)
    r = await client.transfer(CryptoAmount(Amount.automatic(0.1, RUNE_DECIMAL), AssetRUNE), dest_address)
    print(f"Transfer submitted: {client.get_explorer_tx_url(r)}")

    while True:
        print("Waiting for balance update...")
        await asyncio.sleep(6)
        balances = await client.get_balance(dest_address)
        print(f"{dest_address}'s balance is {balances}")

        rune_balance = CryptoAmount.pick(balances, AssetRUNE)

        if rune_balance.amount > 0.1:
            print(f"Balance updated: {rune_balance.amount} Rune! Let's transfer it back")
            break

    rune_balance -= RUNE_NETWORK_FEE
    r = await client.transfer(rune_balance, client.get_address(), wallet_index=1)
    print(f"Transfer submitted: {client.get_explorer_tx_url(r)}")


if __name__ == "__main__":
    asyncio.run(main())

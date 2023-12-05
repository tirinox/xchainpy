import asyncio
import os

from xchainpy2_thorchain import THORChainClient, THOR_BLOCK_TIME_SEC
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

    client_a = THORChainClient(phrase=phrase, network=NETWORK)
    client_b = THORChainClient(phrase=phrase, network=NETWORK, wallet_index=1)

    balance = await client_a.get_balance()
    print(f"{client_a.get_address()}'s balance is {balance}")

    temp_address = client_b.get_address()
    r = await client_a.transfer(CryptoAmount(Amount.automatic(0.1, RUNE_DECIMAL), AssetRUNE), temp_address)
    print(f"Transfer submitted: {client_a.get_explorer_tx_url(r)}")

    while True:
        print("Waiting for balance update...")
        await asyncio.sleep(THOR_BLOCK_TIME_SEC)
        balances = await client_b.get_balance()
        print(f"{temp_address} balance is {balances}")

        rune_balance = CryptoAmount.pick(balances, AssetRUNE)

        if rune_balance.amount > 0.1:
            print(f"Balance updated: {rune_balance.amount} Rune! Let's transfer it back")
            break

    rune_balance -= RUNE_NETWORK_FEE
    r = await client_b.transfer(rune_balance, client_a.get_address())
    print(f"Transfer submitted: {client_b.get_explorer_tx_url(r)}")


if __name__ == "__main__":
    asyncio.run(main())

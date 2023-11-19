import asyncio
import os

from xchainpy2_mayachain import MayaChainClient
from xchainpy2_thorchain_query import CACAO_NETWORK_FEE
from xchainpy2_utils import CryptoAmount, Amount, NetworkType, CACAO_DECIMAL, AssetCACAO

"""
This example requires a real wallet with some amount of Cacao
(5 Cacao will be more than enough)
Just don't forget to pass "PHRASE" environment variable that contains a mnemonic phrase of your wallet
"""

NETWORK = NetworkType.MAINNET


async def main():
    phrase = os.environ.get('PHRASE')
    if not phrase:
        raise ValueError("PHRASE env var is empty!")

    client = MayaChainClient(phrase=phrase, network=NETWORK)

    balance = await client.get_balance()
    print(f"{client.get_address()}'s balance is {balance}")

    dest_address = client.get_address(1)
    r = await client.transfer(CryptoAmount(Amount.automatic(0.1, CACAO_DECIMAL), AssetCACAO), dest_address)
    print(f"Transfer submitted: {client.get_explorer_tx_url(r)}")

    while True:
        print("Waiting for balance update...")
        await asyncio.sleep(6)
        balances = await client.get_balance(dest_address)
        print(f"{dest_address}'s balance is {balances}")

        cacao_balance = CryptoAmount.pick(balances, AssetCACAO)

        if cacao_balance.amount > 0.1:
            print(f"Balance updated: {cacao_balance.amount} Cacao! Let's transfer it back")
            break

    cacao_balance -= CACAO_NETWORK_FEE
    r = await client.transfer(cacao_balance, client.get_address(), wallet_index=1)
    print(f"Transfer submitted: {client.get_explorer_tx_url(r)}")


if __name__ == "__main__":
    asyncio.run(main())

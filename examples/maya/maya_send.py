import asyncio
import os

from xchainpy2_mayachain import MayaChainClient, MAYA_BLOCK_TIME_SEC
from xchainpy2_thorchain_query import DEFAULT_CACAO_NETWORK_FEE
from xchainpy2_utils import CryptoAmount, Amount, NetworkType, CACAO_DECIMAL, AssetCACAO

"""
This example requires a real wallet with some amount of Cacao
(5 Cacao will be more than enough)
Just don't forget to pass "PHRASE" environment variable that contains a mnemonic phrase of your wallet
"""

NETWORK = NetworkType.MAINNET

WHAT_SEND = CryptoAmount(
    Amount.automatic(1.0, CACAO_DECIMAL),
    AssetCACAO
)


async def main():
    phrase = os.environ.get('PHRASE')
    if not phrase:
        raise ValueError("PHRASE env var is empty!")

    client_a = MayaChainClient(phrase=phrase, network=NETWORK)
    client_b = MayaChainClient(phrase=phrase, network=NETWORK, wallet_index=1)

    balance = await client_a.get_balance()
    print(f"{client_a.get_address()}'s balance is {balance}")

    dest_address = client_b.get_address()
    r = await client_a.transfer(WHAT_SEND, dest_address)
    print(f"Transfer submitted: {client_a.get_explorer_tx_url(r)}")

    while True:
        print("Waiting for balance update...")
        await asyncio.sleep(MAYA_BLOCK_TIME_SEC)
        balances = await client_b.get_balance(dest_address)
        print(f"{dest_address}'s balance is {balances}")

        cacao_balance = CryptoAmount.pick(balances, AssetCACAO)

        if cacao_balance.amount > 0.1:
            print(f"Balance updated: {cacao_balance.amount} Cacao! Let's transfer it back")
            break

    cacao_balance -= DEFAULT_CACAO_NETWORK_FEE
    r = await client_b.transfer(cacao_balance, client_b.get_address())
    print(f"Transfer submitted: {client_b.get_explorer_tx_url(r)}")


if __name__ == "__main__":
    asyncio.run(main())

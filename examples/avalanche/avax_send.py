import asyncio

from examples.common import get_phrase
from xchainpy2_avalanche import AvalancheClient
from xchainpy2_client import FeeOption
from xchainpy2_ethereum import GasOptions
from xchainpy2_utils import NetworkType


async def main():
    phrase = get_phrase()
    avax1 = AvalancheClient(phrase=phrase, network=NetworkType.MAINNET, wallet_index=0)
    avax2 = AvalancheClient(phrase=phrase, network=NetworkType.MAINNET, wallet_index=1)

    print("Avax 1 address: ", avax1.get_address())
    print("Avax 2 address: ", avax2.get_address())

    balance1 = await avax1.get_gas_balance()
    balance2 = await avax2.get_gas_balance()
    print("Avax 1 balance: ", balance1)
    print("Avax 2 balance: ", balance2)

    if balance2 > balance1:
        avax1, avax2 = avax2, avax1
        balance1, balance2 = balance2, balance1

    gas = GasOptions.automatic(FeeOption.FAST)

    async def transfer_some_avax():
        input("Press Enter to send TX...")
        amount = balance1 * 0.1
        print(f"Transferring {amount} to {avax1.get_address()}")
        tx_hash = await avax1.transfer(amount, avax2.get_address(), gas=gas, memo="barfoo")
        print(f"Transfer tx hash {avax1.get_explorer_tx_url(tx_hash)}")

        await avax1.wait_for_transaction(tx_hash)
        print("Transaction mined")

    await transfer_some_avax()


if __name__ == "__main__":
    asyncio.run(main())

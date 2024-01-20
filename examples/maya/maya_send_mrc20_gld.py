import asyncio
import os
import sys

from xchainpy2_mayachain import MayaChainClient, MAYA_BLOCK_TIME_SEC
from xchainpy2_mayachain.mrc20.const import MRC20_DECIMALS, AssetGLD
from xchainpy2_utils import Amount, NetworkType, CryptoAmount, AssetCACAO

"""
This example requires a real wallet with some amount of Cacao for gas (1 Cacao will be enough)
Obviously, there must be also GLD to transfer

Just don't forget to pass "PHRASE" environment variable that contains a mnemonic phrase of your wallet
"""

NETWORK = NetworkType.MAINNET


def usage():
    print(f"Usage: python {sys.argv[0]} amount maya1DestAddress")
    exit(-1)


async def main():
    phrase = os.environ.get('PHRASE')
    if not phrase:
        raise ValueError("PHRASE env var is empty!")
    phrase = phrase.strip().strip('"')

    client = MayaChainClient(phrase=phrase, network=NETWORK)

    if len(sys.argv) != 3:
        usage()

    dest_address = sys.argv[2]
    if not client.validate_address(dest_address):
        print('Invalid dest address!')
        usage()

    amount = Amount.automatic(float(sys.argv[1]), MRC20_DECIMALS)
    if amount <= 0:
        print("Amount is <= 0")
        usage()

    balances = await client.get_balance()
    gld_balance = CryptoAmount.pick(balances, AssetGLD)
    print(f"Source {client.get_address()}'s balance is {gld_balance.amount}")

    if amount > gld_balance.amount:
        print("Insufficient GLD!")
        usage()

    dest_balance = await client.get_balance(dest_address)
    dest_gld_balance = CryptoAmount.pick(dest_balance, AssetGLD)
    print(f"Destination {client.get_address()}'s balance is {dest_gld_balance}")

    print(f"Sending {amount} GLD to {dest_address}")

    tx_id = await client.transfer(CryptoAmount(amount, AssetGLD), dest_address)
    print(f"Transaction has been broadcast: {client.get_explorer_tx_url(tx_id)}")

    while True:
        print("Waiting for balance update...")
        await asyncio.sleep(MAYA_BLOCK_TIME_SEC)
        balances = await client.get_balance(dest_address)
        print(f"Destination {dest_address}'s balance is {balances}")

        after_balance = CryptoAmount.pick(balances, AssetGLD)

        if after_balance.amount > dest_gld_balance.amount:
            print(f"Balance updated: {after_balance.amount} Gld!")
            break

    print('Done!')

    await client.close()


if __name__ == "__main__":
    asyncio.run(main())

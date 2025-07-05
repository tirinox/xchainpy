import asyncio
import os

from xchainpy2_thorchain import THORChainClient
from xchainpy2_utils import CryptoAmount, Amount, AssetRUNE, RUNE_DECIMAL, Asset, NetworkType

"""
This example requires a real wallet with some amount of Rune
(1 Rune will be more than enough)
Just don't forget to pass "PHRASE" environment variable that contains a mnemonic phrase of your wallet
"""

TRADE_BNB = Asset.from_string('BSC~BNB')
TARGET_ASSET = TRADE_BNB

NETWORK = NetworkType.MAINNET  # or NetworkType.STAGENET


async def swap_rune_to_target_asset(client, rune_amount):
    amount = CryptoAmount(Amount.auto(rune_amount, RUNE_DECIMAL), AssetRUNE)
    print(f'I will swap {amount} to {TARGET_ASSET} now.')

    out_address = client.get_address()

    tx_hash = await client.deposit(amount, memo=f'=:{TARGET_ASSET!s}:{out_address}')

    print(f"Swap TX submitted: {client.get_explorer_tx_url(tx_hash)}")


async def swap_back_to_rune(client, amount: CryptoAmount):
    print(f'I will swap {amount} of {TARGET_ASSET}` back to RUNE now.')

    out_address = client.get_address()

    tx_hash = await client.deposit(amount, memo=f'=:THOR.RUNE:{out_address}')

    print(f"Swap TX submitted: {client.get_explorer_tx_url(tx_hash)}")


async def check_for_target_trade_balance(client):
    balance = await client.get_balance()

    for b in balance:
        if b.asset == TARGET_ASSET:
            print(f'It seems we got {b}')
            return b
    else:
        print('Not received yet.')
        return CryptoAmount.zero(TARGET_ASSET, RUNE_DECIMAL)


async def main():
    phrase = os.environ.get('PHRASE')
    if not phrase:
        raise ValueError("PHRASE env var is empty!")

    client = THORChainClient(phrase=phrase, network=NETWORK)

    balance = await client.get_balance()
    print(f"{client.get_address()}'s balance is {balance}")

    # Now swap some Rune to the target asset (e.g., BNB)
    # await swap_rune_to_target_asset(client, 0.1)

    # Wait until it is done
    while True:
        print("Waiting until things settle down...")
        await asyncio.sleep(10.0)
        satoshi = await check_for_target_trade_balance(client)
        if satoshi:
            break

    # A little bit more sleep to be sure...
    print('Sleeping for 6 seconds...')
    await asyncio.sleep(6.0)

    # Swap all BTC/BTC back to RUNE
    await swap_back_to_rune(client, satoshi)

    # Close the client
    await client.close()


if __name__ == "__main__":
    asyncio.run(main())

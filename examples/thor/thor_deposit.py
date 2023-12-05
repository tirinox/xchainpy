import asyncio
import os

from xchainpy2_thorchain import THORChainClient
from xchainpy2_utils import CryptoAmount, Amount, AssetRUNE, RUNE_DECIMAL, Asset, NetworkType

"""
This example requires a real wallet with some amount of Rune
(1 Rune will be more than enough)
Just don't forget to pass "PHRASE" environment variable that contains a mnemonic phrase of your wallet
"""

SYNTH_BTC = Asset.from_string('BTC/BTC')

NETWORK = NetworkType.MAINNET


# NETWORK = NetworkType.STAGENET

async def swap_rune_to_synth_btc(client, rune_amount):
    print('I will swap 0.1 RUNE to BTC/BTC now.')

    out_address = client.get_address()

    tx_hash = await client.deposit(
        CryptoAmount(Amount.automatic(rune_amount, RUNE_DECIMAL), AssetRUNE),
        memo=f'=:BTC/BTC:{out_address}'
    )

    print(f"Swap TX submitted: {client.get_explorer_tx_url(tx_hash)}")


async def swap_synth_btc_back_to_rune(client, satoshi):
    print(f'I will swap {satoshi} of BTC/BTC back to RUNE now.')

    out_address = client.get_address()

    tx_hash = await client.deposit(
        CryptoAmount(Amount.automatic(satoshi, RUNE_DECIMAL), SYNTH_BTC),
        memo=f'=:THOR.RUNE:{out_address}'
    )

    print(f"Swap TX submitted: {client.get_explorer_tx_url(tx_hash)}")


async def check_for_synth_btc_balance(client) -> int:
    balance = await client.get_balance()

    for b in balance:
        if b.asset == SYNTH_BTC:
            print(f'It seems we got some synth {b.amount} synth BTC')
            satoshi = b.amount.internal_amount
            return satoshi
    else:
        print('No BTC yet.')
        return 0


async def demo_simple_deposit(client):
    # Swap 0.1 RUNE to BTC/BTC
    await swap_rune_to_synth_btc(client, 0.1)

    # Wait until it is done
    while True:
        print("Waiting until things settle down...")
        await asyncio.sleep(10.0)
        satoshi = await check_for_synth_btc_balance(client)
        if satoshi:
            break

    # A little bit more sleep to be sure...
    print('Sleeping for 6 seconds...')
    await asyncio.sleep(6.0)

    # Swap all BTC/BTC back to RUNE
    await swap_synth_btc_back_to_rune(client, satoshi)


async def main():
    phrase = os.environ.get('PHRASE')
    if not phrase:
        raise ValueError("PHRASE env var is empty!")

    client = THORChainClient(phrase=phrase, network=NETWORK)

    balance = await client.get_balance()
    print(f"{client.get_address()}'s balance is {balance}")

    await demo_simple_deposit(client)


if __name__ == "__main__":
    asyncio.run(main())

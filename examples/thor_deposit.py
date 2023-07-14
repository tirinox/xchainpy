import asyncio
import os

from xchainpy2_thorchain import THORChainClient
from xchainpy2_utils import CryptoAmount, Amount, AssetRUNE, RUNE_DECIMAL, Asset

SYNTH_BTC = Asset.from_string('BTC/BTC')


async def swap_rune_to_synth_btc(rune_amount):
    print('I will swap 0.1 RUNE to BTC/BTC now.')

    out_address = client.get_address()

    tx_hash = await client.deposit(
        CryptoAmount(Amount.automatic(rune_amount, RUNE_DECIMAL), AssetRUNE),
        memo=f'=:BTC/BTC:{out_address}'
    )

    print(f"Swap TX submitted: {client.get_explorer_tx_url(tx_hash)}")


async def swap_synth_btc_back_to_rune(satoshi):
    print(f'I will swap {satoshi} of BTC/BTC back to RUNE now.')

    out_address = client.get_address()

    tx_hash = await client.deposit(
        CryptoAmount(Amount.automatic(satoshi, RUNE_DECIMAL), SYNTH_BTC),
        memo=f'=:THOR.RUNE:{out_address}'
    )

    print(f"Swap TX submitted: {client.get_explorer_tx_url(tx_hash)}")


async def check_for_synth_btc_balance() -> int:
    balance = await client.get_balance()

    for b in balance:
        if b.asset == SYNTH_BTC:
            print(f'It seems we got some synth {b.amount} synth BTC')
            satoshi = b.amount.internal_amount
            return satoshi
    else:
        print('No BTC yet.')
        return 0


async def demo_simple_deposit():
    # Swap 0.1 RUNE to BTC/BTC
    # await swap_rune_to_synth_btc(0.1)

    # Wait until it is done
    while True:
        print("Waiting until things settle down...")
        await asyncio.sleep(10.0)
        satoshi = await check_for_synth_btc_balance()
        if satoshi:
            break

    # Swap all BTC/BTC back to RUNE
    await swap_synth_btc_back_to_rune(satoshi)


async def main():
    balance = await client.get_balance()
    print(f"{client.get_address()}'s balance is {balance}")

    await demo_simple_deposit()


if __name__ == "__main__":
    """
    This example requires a real wallet with some amount of Rune
    (1 Rune will be more than enough)
    Just don't forget to pass "PHRASE" environment variable that contains a mnemonic phrase of your wallet
    """
    phrase = os.environ.get('PHRASE')
    if not phrase:
        raise ValueError("PHRASE env var is empty!")

    client = THORChainClient(phrase=phrase)

    asyncio.run(main())

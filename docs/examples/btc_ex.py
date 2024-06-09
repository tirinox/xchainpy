import asyncio
import getpass

from xchainpy2_bitcoin import BitcoinClient
from xchainpy2_utils import NetworkType


async def send_btc():
    phrase = getpass.getpass('Enter a BIP39 mnemonic phrase: ')

    btc = BitcoinClient(phrase=phrase, network=NetworkType.TESTNET)
    btc2 = BitcoinClient(phrase=phrase, network=NetworkType.TESTNET, wallet_index=1)

    available_providers = btc.get_available_provider_names()
    print(f"Available providers: {available_providers}")

    source_address = btc.get_address()
    dest_address = btc2.get_address()

    print(f"First BTC Address: {source_address}")
    print(f"Second BTC Address: {dest_address}")

    balance1 = await btc.get_balance()
    print(f"Balance 1 ({source_address}): {balance1}")

    balance2 = await btc2.get_balance()
    print(f"Balance 2 ({dest_address}): {balance2}")

    if balance2 > balance1:
        print('Swapping addresses')
        btc, btc2 = btc2, btc

    tx_hash = await btc.transfer(btc2.gas_amount(0.00001234), dest_address, memo='test')

    print(f"Transfer hash: {tx_hash} ({btc2.get_explorer_tx_url(tx_hash)})")

    print("Waiting for transaction to complete (10 minutes)...")
    tx = await btc.wait_for_transaction(tx_hash)
    print(f"Transaction confirmed: {tx}")

    balance = await btc.get_balance()
    print(f"Balance 1 ({source_address}): {balance}")

    balance = await btc2.get_balance()
    print(f"Balance 2 ({dest_address}): {balance}")


async def main():
    await send_btc()


if __name__ == '__main__':
    asyncio.run(main())

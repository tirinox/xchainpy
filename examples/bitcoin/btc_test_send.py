import asyncio

from examples.common import get_phrase
from xchainpy2_bitcoin import BitcoinClient
from xchainpy2_utils import NetworkType


async def main():
    phrase = get_phrase()

    # btc = BitcoinClient(phrase=phrase, network=NetworkType.DEVNET, provider_names=[])

    # provider_names = ['blockstream']
    provider_names = ['mempool']

    btc = BitcoinClient(phrase=phrase, network=NetworkType.TESTNET, provider_names=provider_names)
    btc2 = BitcoinClient(phrase=phrase, network=NetworkType.TESTNET, wallet_index=1, provider_names=provider_names)

    source_address = btc.get_address()
    dest_address = btc2.get_address()

    print(f"First BTC Address: {source_address}")
    print(f"Second BTC Address: {dest_address}")

    balance = await btc.get_balance()
    print(f"Balance 1 ({source_address}): {balance}")

    utxos = await btc.get_utxos()
    print(f"UTXO of {source_address} are ({len(utxos)}) {utxos}")

    tx_hash = await btc.transfer(btc2.gas_amount(0.00011), dest_address, memo='test', fee_rate=4)
    # print(tx_hash)


if __name__ == '__main__':
    asyncio.run(main())

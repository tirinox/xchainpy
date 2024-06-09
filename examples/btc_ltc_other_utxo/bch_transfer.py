import asyncio

from examples.common import get_phrase
from xchainpy2_bitcoincash import BitcoinCashClient


async def main():
    phrase = get_phrase()
    bch_client1 = BitcoinCashClient(phrase=phrase)
    bch_client2 = BitcoinCashClient(phrase=phrase, wallet_index=1)

    balance1 = await bch_client1.get_balance()
    balance2 = await bch_client2.get_balance()
    print(f"{bch_client1.get_address()} has balance of {balance1}")
    print(f"{bch_client2.get_address()} has balance of {balance2}")

    if balance2 > balance1:
        print('Swapping addresses')
        bch_client1, bch_client2 = bch_client2, bch_client1

    tx_hash = await bch_client1.transfer(bch_client2.gas_amount(0.00001234),
                                         bch_client2.get_address(), memo='foobar')
    print(f"Transfer hash: {tx_hash} ({bch_client1.get_explorer_tx_url(tx_hash)})")

    print("Waiting for transaction to complete (up to 10 minutes)...")
    tx = await bch_client1.wait_for_transaction(tx_hash)
    print(f"Transaction confirmed: {tx}")

    balance1 = await bch_client1.get_balance()
    balance2 = await bch_client2.get_balance()
    print(f"{bch_client1.get_address()} has balance of {balance1}")
    print(f"{bch_client2.get_address()} has balance of {balance2}")


if __name__ == '__main__':
    asyncio.run(main())

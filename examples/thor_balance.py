import asyncio

from xchainpy2_crypto import generate_mnemonic
from xchainpy2_thorchain import THORChainClient
from xchainpy2_thorchain_query import TC_RESERVE_ADDR


async def main():
    client = THORChainClient(phrase=generate_mnemonic())

    addr = 'thor1z9xhmhtxn5gxd4ugfuxk7hg9hp03tw3qtqs3f3'
    # addr = client.get_address()
    reserve_account = await client.get_account(addr)
    print(f"Account of ({addr}) is {reserve_account}")

    balance = await client.get_balance()
    print(f"Balance of {client.get_address()} is {balance}")

    reserve_balance = await client.get_balance(TC_RESERVE_ADDR)
    print(f"Balance of the Reserve ({TC_RESERVE_ADDR}) is {reserve_balance}")


if __name__ == "__main__":
    asyncio.run(main())
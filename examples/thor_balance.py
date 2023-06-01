import asyncio

from xchainpy2_crypto import generate_mnemonic
from xchainpy2_thorchain import THORChainClient
from xchainpy2_thorchain_query import TC_RESERVE_ADDR


async def main():
    client = THORChainClient(phrase=generate_mnemonic())

    balance = await client.get_balance()
    print(f"Balance of {client.get_address()} is {balance}")

    reserve_balance = await client.get_balance(TC_RESERVE_ADDR)
    print(f"Balance of the Reserve ({TC_RESERVE_ADDR}) is {reserve_balance}")


if __name__ == "__main__":
    asyncio.run(main())
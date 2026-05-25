import asyncio

from xchainpy2_thorchain import THORChainClient
from xchainpy2_utils import NetworkType

NETWORK = NetworkType.MAINNET


async def main():
    client = THORChainClient(network=NETWORK)

    fees = await client.get_fees()
    print(f"THORChain TX fee is {fees.amount}")

    await client.close()


if __name__ == "__main__":
    asyncio.run(main())

import asyncio

from xchainpy2_mayachain import MayaChainClient
from xchainpy2_utils import NetworkType

NETWORK = NetworkType.MAINNET


async def main():
    client = MayaChainClient(network=NETWORK)

    fees = await client.get_fees()
    print(f"MayaChain TX fee is {fees.amount}")

    await client.close()


if __name__ == "__main__":
    asyncio.run(main())

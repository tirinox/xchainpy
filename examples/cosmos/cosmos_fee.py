import asyncio
import os

from xchainpy2_cosmos import CosmosGaiaClient
from xchainpy2_utils import CryptoAmount, AssetATOM


async def main():
    client = CosmosGaiaClient(phrase=os.environ.get('PHRASE'))
    r = await client.estimate_gas_of_transfer(
        CryptoAmount.auto(0.001, AssetATOM),
        "cosmos1c4k24jzduc365kywrsvf5ujz4ya6mwymy8vq4q",
        memo=""
    )
    print(r)


if __name__ == '__main__':
    asyncio.run(main())

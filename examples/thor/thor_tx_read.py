import asyncio

from xchainpy2_thorchain import THORChainClient


async def main():
    client = THORChainClient()
    tx_data = await client.get_transaction_data("058793B5A9447BD23462BEA3818F3A9517D40DD1974F3E4A04D87D8D28DF621E")
    print(tx_data)


if __name__ == "__main__":
    asyncio.run(main())

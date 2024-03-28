import asyncio
import os

from web3 import Web3

from xchainpy2_ethereum import EthereumClient


async def main():
    # Connect to the Ethereum network using the provider
    # You can obtain an Infura URL by creating a project at https://infura.io/
    url = '' or os.environ.get('INFURA_URL')
    if not url:
        raise ValueError('Please provide an ETH RPC URL')

    provider = Web3.HTTPProvider(url)

    cli = EthereumClient(provider=provider)
    fee = await cli.get_last_fee()
    print(f'Last fee: {fee}')

    fees = await cli.get_fees()
    print(f'Fees: {fees}')


if __name__ == '__main__':
    asyncio.run(main())

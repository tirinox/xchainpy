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

    balances = await cli.get_balance('0x3AA5196038f1Dff8E2E93fa43F4DC4501809D6b0')
    print(balances)

    balance_erc20 = await cli.get_erc20_token_balance('0xdAC17F958D2ee523a2206206994597C13D831ec7',
                                                      '0x3AA5196038f1Dff8E2E93fa43F4DC4501809D6b0')
    print(balance_erc20)


if __name__ == "__main__":
    asyncio.run(main())

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

    tx_data = await cli.get_transaction_data('0x63f452705edac36dcbce4b37c29654be1f170fe53fe477c558c20ca90a6b274a')
    # tx_data = await cli.get_transaction_data('0xbb743b931be4b6a8ba557162a4a0cd555b7fbef709871bc9bf2d38d62514b906')  # pending
    print(f'Tx data: {tx_data}')



if __name__ == "__main__":
    asyncio.run(main())

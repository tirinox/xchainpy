import asyncio
import os

from web3 import Web3

from examples.common import sep
from xchainpy2_ethereum import EthereumClient


async def main():
    # Connect to the Ethereum network using the provider
    # You can obtain an Infura URL by creating a project at https://infura.io/
    url = '' or os.environ.get('INFURA_URL')
    if not url:
        raise ValueError('Please provide an ETH RPC URL')

    provider = Web3.HTTPProvider(url)

    cli = EthereumClient(provider=provider)

    # many ERC20 transfers
    # tx_data = await cli.get_transaction_data('0xf26d7a27a133f19c4abba00e8a92da346d33f79fb83c622d6fdd1bb141a2e012')

    #
    # tx_data = await cli.get_transaction_data('0x63f452705edac36dcbce4b37c29654be1f170fe53fe477c558c20ca90a6b274a')

    # transfer out
    tx_data = await cli.get_transaction_data('0xe428554d1293a410b444ba46168a516982b268406c469bfa2d52fe3cea4d800d')

    print(f'Tx data: {tx_data}')
    sep()
    for tr in tx_data.transfers:
        print(f'{tr.amount} {tr.asset}: {tr.from_address} -> {tr.to_address}')
        sep()


if __name__ == "__main__":
    asyncio.run(main())

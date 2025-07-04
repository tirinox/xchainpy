import asyncio
import os

from xchainpy2_client import FeeOption, Gas
from xchainpy2_ethereum import EthereumClient
from xchainpy2_utils import CryptoAmount, AssetETH


async def main():
    cli = EthereumClient(
        phrase=os.getenv('PHRASE'),
        provider=os.getenv('WEB3_PROVIDER'),
    )
    fee = await cli.get_last_fee()
    print(f'Last fee: {fee}')

    fees = await cli.get_fees()
    print(f'Fees: {fees!s}')

    gas = await cli.estimate_gas_of_transfer(
        CryptoAmount.auto(0.001, AssetETH), "", "test message",
        nonce=1,
        gas=Gas.auto(FeeOption.FAST)
    )
    print(f'Gas of ETH transfer: {gas}')


if __name__ == '__main__':
    asyncio.run(main())

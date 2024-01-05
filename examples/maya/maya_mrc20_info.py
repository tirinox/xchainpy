import asyncio

from xchainpy2_mayachain import MayaChainClient
from xchainpy2_mayachain.mrc20.const import AssetGLD
from xchainpy2_utils import NetworkType

"""
This example requires a real wallet with some amount of Cacao for gas (1 Cacao will be enough)
Obviously, there must be also GLD to transfer

Just don't forget to pass "PHRASE" environment variable that contains a mnemonic phrase of your wallet
"""

NETWORK = NetworkType.MAINNET


async def main():
    client = MayaChainClient(network=NETWORK)

    mrc20_tokens = await client.maya_scan.get_all_tokens()
    print(f'Total MRC20 tokens: {len(mrc20_tokens)}')
    print(f'First token: {mrc20_tokens[0]}')

    gld_price = await client.maya_scan.get_price(AssetGLD)
    print(f'GLD price: {gld_price}\n')

    order_book = await client.maya_scan.get_orderbook(AssetGLD)
    print(f'Order book: {order_book[:3]}, ...\n')

    addr = 'maya1eengpj4yac7vwnnxr2jytyvpw2kusqrzqggsc4'
    nft_balance = await client.maya_scan.get_nft_balance(addr)
    print(f'NFT balance of {client.get_explorer_address_url(addr)} is {nft_balance}\n')

    staking_balance = await client.maya_scan.get_staking_balance(addr, AssetGLD)
    print(f'Staking balance is {staking_balance}\n')

    await client.close()

if __name__ == "__main__":
    asyncio.run(main())

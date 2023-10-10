import asyncio

from xchainpy2_crypto import generate_mnemonic
from xchainpy2_thorchain import THORChainClient, NodeURL, DEFAULT_CLIENT_URLS
from xchainpy2_utils import NetworkType

TC_RESERVE_ADDR = 'thor1dheycdevq39qlkxs2a6wuuzyn4aqxhve4qxtxt'

# Standard public node (maybe protected by Cloudflare, so won't work from Python)
# MY_CLIENT_URLS = DEFAULT_CLIENT_URLS

# In case, you can use your own full node like
MY_CLIENT_URLS = {
    NetworkType.MAINNET: NodeURL(
        'https://thorchain.fullnode.runepool.com',
        'https://rpc.fullnode.runepool.com'
    ),
}


async def main():
    print(f'{DEFAULT_CLIENT_URLS=}')
    print(f'{MY_CLIENT_URLS=}')

    client = THORChainClient(phrase=generate_mnemonic(), client_urls=MY_CLIENT_URLS)

    balance = await client.get_balance()
    print(f"Balance of {client.get_address()} is {balance}. <- Unsurprisingly empty, because it's a new address")

    address = 'thor1z9xhmhtxn5gxd4ugfuxk7hg9hp03tw3qtqs3f3'
    account = await client.get_account(address)
    print(f"Account of ({address}) is {account}")
    balance = await client.get_balance(address)
    print(f"Balance of ({address}) is {balance}")

    reserve_balance = await client.get_balance(TC_RESERVE_ADDR)
    print(f"Balance of the Reserve ({TC_RESERVE_ADDR}) is {reserve_balance}")


if __name__ == "__main__":
    asyncio.run(main())

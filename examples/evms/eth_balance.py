import asyncio

from xchainpy2_ethereum import EthereumClient

USDT_CONTRACT = '0xdAC17F958D2ee523a2206206994597C13D831ec7'
EXAMPLE_ADDRESS = '0x3AA5196038f1Dff8E2E93fa43F4DC4501809D6b0'
EXAMPLE_SPENDER = '0x8103ab477AFB5321cCa0C068DCA439E232B6BB78'


async def main():
    cli = EthereumClient()

    balances = await cli.get_balance(EXAMPLE_ADDRESS)
    # balances = await cli.get_balance(EXAMPLE_ADDRESS, with_erc20=True)  # requires PRO API key
    print(balances)

    balance_erc20 = await cli.get_erc20_token_balance(USDT_CONTRACT, EXAMPLE_ADDRESS)
    print(balance_erc20)

    approved = await cli.get_erc20_allowance(USDT_CONTRACT, EXAMPLE_SPENDER, EXAMPLE_ADDRESS)
    print(f'Address {EXAMPLE_ADDRESS} approved {approved} to spend USDT for {EXAMPLE_SPENDER}')


if __name__ == "__main__":
    asyncio.run(main())

import asyncio

from examples.common import get_phrase
from xchainpy2_base import BaseClient
from xchainpy2_client import FeeOption
from xchainpy2_ethereum import GasOptions
from xchainpy2_utils import NetworkType, CryptoAmount

# all upper address will bypass the checksum validation
BASE_USDT_CONTRACT = '0xfde4C96c8593536E31F229EA8f37b2ADa2699bb2'.upper()


async def main():
    phrase = get_phrase()
    base1 = BaseClient(phrase=phrase, network=NetworkType.MAINNET, wallet_index=0)
    base2 = BaseClient(phrase=phrase, network=NetworkType.MAINNET, wallet_index=1)

    print("Base address: ", base1.get_address())
    print("Base address: ", base2.get_address())

    balance1 = await base1.get_gas_balance()
    balance2 = await base2.get_gas_balance()
    print("Base balance: ", balance1)
    print("Base balance: ", balance2)

    if balance2 > balance1:
        base1, base2 = base2, base1
        balance1, balance2 = balance2, balance1

    fees = await base1.get_fees()
    print(f'Base fees: {fees}')

    gas = GasOptions.automatic(FeeOption.FAST)

    # gas = GasOptions.legacy(gas_price=50, gas_limit=210000)
    # gas = GasOptions.eip1559_in_gwei(max_fee_per_gas=1, max_priority_fee_per_gas=1, gas_limit=210000)

    async def transfer_some_eth():
        input("Press Enter to send TX...")
        amount = balance1 * 0.1
        print(f"Transferring {amount} to {base2.get_address()}")
        tx_hash = await base1.transfer(amount, base2.get_address(), gas=gas, memo="barfoo")
        print(f"Transfer tx hash {base2.get_explorer_tx_url(tx_hash)}")
        await base1.wait_for_transaction(tx_hash)
        print("Transaction mined")

    await transfer_some_eth()

    #
    # async def approve_some_eth():
    #     usdt = await base1.get_erc20_token_info(base_USDT_CONTRACT)
    #
    #     print("Before approve")
    #     allowance = await base1.get_erc20_allowance(usdt.as_asset.contract, ROUTER)
    #     print(f"Allowance of {base1.get_address()} for spender {base_USDT_CONTRACT} is {allowance}")
    #     input("Press Enter to send TX...")
    #
    #     tx = await base1.approve_erc20_token(base_PANCAKE_ROUTER, usdt.amount_of(0.1), gas)
    #     print(f"Approve tx hash {base1.get_explorer_tx_url(tx)}")
    #
    #     print("Waiting for transaction to be mined...")
    #     await base1.wait_for_transaction(tx)
    #
    #     print("After approve")
    #     allowance = await base1.get_erc20_allowance(usdt.as_asset.contract, ROUTER)
    #     print(f"Allowance of {base1.get_address()} for spender {base_USDT_CONTRACT} is {allowance}")
    #
    # async def transfer_some_usdt():
    #     usdt_balance = await base1.get_erc20_token_balance(base_USDT_CONTRACT)
    #     print(usdt_balance)
    #
    #     input("Press Enter to send TX...")
    #     amount = usdt_balance * 0.1
    #     tx_hash = await base1.transfer(amount, base2.get_address(), gas=gas)
    #     print(f"Transfer tx hash {base1.get_explorer_tx_url(tx_hash)}")
    #
    #     await base1.wait_for_transaction(tx_hash)
    #     print("Transaction mined")
    #


if __name__ == "__main__":
    asyncio.run(main())

import asyncio

from examples.common import get_phrase
from xchainpy2_bsc import BinanceSmartChainClient
from xchainpy2_client import FeeOption
from xchainpy2_ethereum import GasOptions
from xchainpy2_utils import NetworkType, CryptoAmount

# all upper address will bypass the checksum validation
BSC_USDT_CONTRACT = '0x55d398326f99059ff775485246999027b3197955'.upper()
BSC_PANCAKE_ROUTER = '0x13f4ea83d0bd40e75c8222255bc855a974568dd4'.upper()


async def main():
    phrase = get_phrase()
    bsc1 = BinanceSmartChainClient(phrase=phrase, network=NetworkType.MAINNET, wallet_index=0)
    bsc2 = BinanceSmartChainClient(phrase=phrase, network=NetworkType.MAINNET, wallet_index=1)

    print("BSC1 address: ", bsc1.get_address())
    print("BSC2 address: ", bsc2.get_address())

    balance1 = await bsc1.get_gas_balance()
    balance2 = await bsc2.get_gas_balance()
    print("BSC1 balance: ", balance1)
    print("BSC2 balance: ", balance2)

    if balance2 > balance1:
        bsc1, bsc2 = bsc2, bsc1
        balance1, balance2 = balance2, balance1

    gas = GasOptions.automatic(FeeOption.FAST)

    # gas = GasOptions.legacy(gas_price=50, gas_limit=210000)
    # gas = GasOptions.eip1559_in_gwei(max_fee_per_gas=1, max_priority_fee_per_gas=1, gas_limit=210000)

    async def transfer_some_bnb():
        input("Press Enter to send TX...")
        amount = balance1 * 0.01
        print(f"Transferring {amount} to {bsc2.get_address()}")
        tx_hash = await bsc1.transfer(amount, bsc2.get_address(), gas=gas, memo="barfoo")
        print(f"Transfer tx hash {bsc1.get_explorer_tx_url(tx_hash)}")

        await bsc1.wait_for_transaction(tx_hash)
        print("Transaction mined")

    async def approve_some_bnb():
        usdt = await bsc1.get_erc20_token_info(BSC_USDT_CONTRACT)

        print("Before approve")
        allowance = await bsc1.get_erc20_allowance(usdt.asset.contract, BSC_PANCAKE_ROUTER)
        print(f"Allowance of {bsc1.get_address()} for spender {BSC_USDT_CONTRACT} is {allowance}")
        input("Press Enter to send TX...")

        tx = await bsc1.approve_erc20_token(BSC_PANCAKE_ROUTER, usdt.change_amount(0.1), gas)
        print(f"Approve tx hash {bsc1.get_explorer_tx_url(tx)}")

        print("Waiting for transaction to be mined...")
        await bsc1.wait_for_transaction(tx)

        print("After approve")
        allowance = await bsc1.get_erc20_allowance(usdt.asset.contract, BSC_PANCAKE_ROUTER)
        print(f"Allowance of {bsc1.get_address()} for spender {BSC_USDT_CONTRACT} is {allowance}")

    async def transfer_some_usdt():
        usdt_balance = await bsc1.get_erc20_token_balance(BSC_USDT_CONTRACT)
        print(usdt_balance)

        input("Press Enter to send TX...")
        amount = usdt_balance * 0.1
        tx_hash = await bsc1.transfer(amount, bsc2.get_address(), gas=gas)
        print(f"Transfer tx hash {bsc1.get_explorer_tx_url(tx_hash)}")

        await bsc1.wait_for_transaction(tx_hash)
        print("Transaction mined")

    # await transfer_some_usdt()
    # await approve_some_bnb()
    await transfer_some_bnb()


if __name__ == "__main__":
    asyncio.run(main())

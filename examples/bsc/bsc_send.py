import asyncio

from examples.common import get_phrase
from xchainpy2_bsc import BinanceSmartChainClient
from xchainpy2_client import FeeOption
from xchainpy2_ethereum import GasOptions
from xchainpy2_utils import NetworkType, CryptoAmount

BSC_USDT_CONTRACT = '0x55d398326f99059ff775485246999027b3197955'
BSC_PANCAKE_ROUTER = '0x13f4ea83d0bd40e75c8222255bc855a974568dd4'


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
        amount = balance1 * 0.1
        tx_hash = await bsc1.transfer(amount, bsc2.get_address(), gas=gas, memo="barfoo")
        print(f"Transfer tx hash {bsc1.get_explorer_tx_url(tx_hash)}")

    async def approve_some_bnb():
        usdt = await bsc1.get_erc20_token_info(BSC_USDT_CONTRACT)
        tx = await bsc1.approve_erc20_token(BSC_PANCAKE_ROUTER, usdt.change_amount(0.1), gas)
        print(f"Approve tx hash {bsc1.get_explorer_tx_url(tx)}")

    async def transfer_some_usdt():
        usdt_balance = await bsc1.get_erc20_token_balance(BSC_USDT_CONTRACT)
        print(usdt_balance)

        amount = usdt_balance * 0.1
        tx_hash = await bsc1.transfer(amount, bsc2.get_address(), gas=gas)
        print(f"Transfer tx hash {bsc1.get_explorer_tx_url(tx_hash)}")

    await transfer_some_usdt()


if __name__ == "__main__":
    asyncio.run(main())

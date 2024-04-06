import asyncio

from examples.common import get_phrase
from xchainpy2_bsc import BinanceSmartChainClient
from xchainpy2_client import FeeOption
from xchainpy2_ethereum import GasOptions
from xchainpy2_utils import NetworkType


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

    amount = balance1 * 0.1
    # gas = GasOptions.legacy(gas_price=50, gas_limit=210000)
    # gas = GasOptions.eip1559_in_gwei(max_fee_per_gas=1, max_priority_fee_per_gas=1, gas_limit=210000)
    gas = GasOptions.automatic(FeeOption.FAST)
    tx_hash = await bsc1.transfer(amount, bsc2.get_address(), gas=gas, memo="barfoo")
    print(f"Transfer tx hash {bsc1.get_explorer_tx_url(tx_hash)}")


if __name__ == "__main__":
    asyncio.run(main())

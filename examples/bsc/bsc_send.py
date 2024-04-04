import asyncio

from examples.common import get_phrase
from xchainpy2_bsc import BinanceSmartChainClient
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

    amount = balance1 * 0.7
    tx_hash = await bsc1.transfer(amount, bsc2.get_address())
    print(f"Transfer tx hash {bsc1.get_explorer_tx_url(tx_hash)}")


if __name__ == "__main__":
    asyncio.run(main())

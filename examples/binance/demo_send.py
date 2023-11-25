import asyncio

from examples.common import get_phrase
from xchainpy2_binance import BinanceChainClient
from xchainpy2_utils import NetworkType, CryptoAmount

NETWORK = NetworkType.MAINNET


async def main():
    bnb = BinanceChainClient(phrase=get_phrase(), network=NETWORK)
    bnb2 = BinanceChainClient(phrase=get_phrase(), wallet_index=2, network=NETWORK)

    print(f'Address 1: {bnb.get_address()}; address 2: {bnb2.get_address()}')

    balances = await bnb.get_balance()
    print(balances)

    max_sendable = await bnb.max_gas_amount(balances)
    print(f"{max_sendable = }")

    tx = await bnb.transfer(bnb.gas_amount(0.001), bnb2.get_address())
    print(tx)

    await bnb.close_session()
    await bnb2.close_session()


asyncio.run(main())

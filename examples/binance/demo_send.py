import asyncio

from examples.common import get_phrase
from xchainpy2_binance import BinanceChainClient
from xchainpy2_utils import NetworkType

NETWORK = NetworkType.MAINNET


async def main():
    bnb = BinanceChainClient(phrase=get_phrase(), network=NETWORK)
    bnb2 = BinanceChainClient(phrase=get_phrase(), wallet_index=2, network=NETWORK)

    print(f'Address 1: {bnb.get_address()}; address 2: {bnb2.get_address()}')

    balances = await bnb.get_balance()
    print(balances)

    tx = await bnb.transfer(bnb.gas_base_amount(3330), bnb2.get_address())
    print(f'Tx broadcast: {bnb.get_explorer_tx_url(tx)}')

    print(f'Sleeping until things settle down...')
    await asyncio.sleep(6.0)

    max_sendable = await bnb2.max_gas_amount()
    print(f"I will send back {max_sendable} to {bnb.get_address()}")
    tx = await bnb2.transfer(max_sendable, bnb.get_address())
    print(f'Tx broadcast: {bnb.get_explorer_tx_url(tx)}')

    await bnb.close()
    await bnb2.close()


asyncio.run(main())

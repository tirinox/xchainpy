import asyncio

from examples.common import get_phrase
from xchainpy2_bsc import BinanceSmartChainClient
from xchainpy2_client import FeeOption
from xchainpy2_ethereum import GasOptions
from xchainpy2_thorchain_amm import THORChainAMM, Wallet
from xchainpy2_thorchain_query import MidgardAPIClient, THORChainCache, THORChainQuery, TxDetails
from xchainpy2_thorchain_query.thornode import THORNodeAPIClient
from xchainpy2_utils import NetworkType, CryptoAmount, Chain, Asset, BSC_DECIMALS


async def main():
    # midgard = MidgardAPIClient()
    # node = THORNodeAPIClient()
    # cache = THORChainCache(midgard, node)

    phrase = get_phrase()
    wallet = Wallet(phrase)

    query = THORChainQuery()
    amm = THORChainAMM(wallet, query)

    bsc1: BinanceSmartChainClient = wallet.get_client(Chain.BinanceSmartChain)
    print("BSC1 address: ", bsc1.get_address())

    balance1 = await bsc1.get_gas_balance()
    print("BSC1 balance: ", balance1)

    gas = GasOptions.automatic(FeeOption.FAST)
    # gas = GasOptions.legacy(gas_price=50, gas_limit=210000)
    # gas = GasOptions.eip1559_in_gwei(max_fee_per_gas=1, max_priority_fee_per_gas=1, gas_limit=210000)

    async def swap_bnb_to_usdt():
        print("I will swap little BNB to USDT.")
    #    input("Press Enter to send TX...")
        tx_hash = await amm.do_swap(
            CryptoAmount.automatic(0.05, 'BSC.BNB', BSC_DECIMALS),
            Asset.automatic('BSC.USDT-0x55d398326f99059ff775485246999027b3197955').upper(),
        )
        print(f"Swap tx hash {bsc1.get_explorer_tx_url(tx_hash)}")

        print("Waiting for transaction to be mined...")
        await bsc1.wait_for_transaction(tx_hash)
        print("Transaction mined.")

        print("Waiting for transaction to be executed by THORChain...")
        tracker = amm.tracker()
        async for status in tracker.poll(tx_hash):
            status: TxDetails
            print(f'Status: {status.status}; stage: {status.stage}')

    await swap_bnb_to_usdt()

    await asyncio.sleep(1)
    await amm.close()


if __name__ == "__main__":
    asyncio.run(main())

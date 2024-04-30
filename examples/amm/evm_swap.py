import asyncio

from examples.common import get_phrase
from xchainpy2_avalanche import AVAX_DECIMALS
from xchainpy2_bsc import BinanceSmartChainClient
from xchainpy2_client import FeeOption
from xchainpy2_ethereum import GasOptions
from xchainpy2_thorchain_amm import THORChainAMM, Wallet, AMMException, NO_SWAP_LIMIT
from xchainpy2_thorchain_query import THORChainQuery, TxDetails
from xchainpy2_utils import CryptoAmount, Chain, Asset, BSC_DECIMALS


async def main():
    # midgard = MidgardAPIClient()
    # node = THORNodeAPIClient()
    # cache = THORChainCache(midgard, node)

    phrase = get_phrase()
    wallet = Wallet(phrase)

    query = THORChainQuery()
    amm = THORChainAMM(wallet, query)

    # noinspection PyTypeChecker
    bsc: BinanceSmartChainClient = wallet.get_client(Chain.BinanceSmartChain)
    avax = wallet.get_client(Chain.Avalanche)
    print("BSC1 address: ", bsc.get_address())

    balance_bsc = await bsc.get_gas_balance()
    print("BSC balance: ", balance_bsc)
    balance_avax = await avax.get_gas_balance()
    print("AVAX balance: ", balance_avax)

    my_address = bsc.get_address()

    gas = GasOptions.automatic(FeeOption.FAST)
    # gas = GasOptions.legacy(gas_price=50, gas_limit=210000)
    # gas = GasOptions.eip1559_in_gwei(max_fee_per_gas=1, max_priority_fee_per_gas=1, gas_limit=210000)

    async def swap_bnb_and_avax(from_avax_to_bnb: bool):
        if from_avax_to_bnb:
            from_amount = CryptoAmount.automatic(0.6, 'AVAX.AVAX', AVAX_DECIMALS)
            to_asset = Asset.automatic('BSC.BNB').upper()
        else:
            from_amount = CryptoAmount.automatic(0.033, 'BSC.BNB', BSC_DECIMALS)
            to_asset = Asset.automatic('AVAX.AVAX').upper()

        if from_avax_to_bnb:
            print(f"I will swap {from_amount} to BNB.")
        else:
            print(f"I will swap {from_amount} to AVAX.")

        input("Press Enter to send TX...")

        # r = await amm.query.quote_swap(
        #     input_amount=CryptoAmount.automatic(0.05, 'BSC.BNB', BSC_DECIMALS),
        #     # destination_asset=Asset.automatic('BSC.USDT-0x55d398326f99059ff775485246999027b3197955').upper(),
        #     destination_asset=Asset.automatic('AVAX.AVAX').upper(),
        #     destination_address=bsc1.get_address(),
        #     tolerance_bps=500,
        # )
        # print(r)
        # return

        try:
            tx_hash = await amm.do_swap(
                input_amount=from_amount,
                destination_asset=to_asset,
                destination_address=my_address,
                tolerance_bps=NO_SWAP_LIMIT,
                gas_options=gas,
            )
        except AMMException as e:
            print(f"Error: {e}")
            return

        if from_avax_to_bnb:
            tx_hash_url = avax.get_explorer_tx_url(tx_hash)
        else:
            tx_hash_url = bsc.get_explorer_tx_url(tx_hash)
        print(f"Swap tx hash {tx_hash_url}")

        print("Waiting for transaction to be mined...")

        if from_avax_to_bnb:
            await avax.wait_for_transaction(tx_hash)
        else:
            await bsc.wait_for_transaction(tx_hash)

        print("Transaction mined.")

        print("Waiting for transaction to be executed by THORChain...")
        tracker = amm.tracker()
        async for status in tracker.poll(tx_hash):
            status: TxDetails
            print(f'Status: {status.status}; stage: {status.stage}')

    await swap_bnb_and_avax(from_avax_to_bnb=True)

    await asyncio.sleep(1)
    await amm.close()


if __name__ == "__main__":
    asyncio.run(main())

import asyncio

from xchainpy2_thorchain_amm import THORChainAMM, Wallet, NO_SWAP_LIMIT, FeeOption, GasOptions
from xchainpy2_thorchain_query import TxDetails
from xchainpy2_utils import Chain, AssetAVAX


async def main():
    phrase = "your secret phrase here"
    wallet = Wallet(phrase)

    amm = THORChainAMM(wallet)

    bsc = wallet.get_client(Chain.BinanceSmartChain)
    avax = wallet.get_client(Chain.Avalanche)

    balance_bsc = await bsc.get_gas_balance()
    balance_avax = await avax.get_gas_balance()
    print(f"BSC balance: {balance_bsc} and AVAX balance: {balance_avax}")

    tx_hash = await amm.do_swap(
        input_amount=bsc.gas_amount(1.0),  # 1 BNB
        destination_asset=AssetAVAX,
        tolerance_bps=NO_SWAP_LIMIT,
        gas_options=GasOptions.automatic(FeeOption.FAST),
    )

    print(f"Swap TX hash {bsc.get_explorer_tx_url(tx_hash)}")

    await bsc.wait_for_transaction(tx_hash)

    tracker = amm.tracker()
    async for status in tracker.poll(tx_hash):
        status: TxDetails
        print(f'Status: {status.status}; stage: {status.stage}')

    await amm.close()


if __name__ == "__main__":
    asyncio.run(main())

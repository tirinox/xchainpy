import asyncio

from examples.common import get_phrase
from xchainpy2_bsc import BinanceSmartChainClient, AssetBSC_USDT, GasOptions, FeeOption
from xchainpy2_thorchain_amm import THORChainAMM, AMMException, NO_SWAP_LIMIT
from xchainpy2_thorchain_query import THORChainQuery
from xchainpy2_utils import CryptoAmount, Chain, Asset
from xchainpy2_wallet import Wallet

DRY_RUN = False


async def main():
    phrase = get_phrase()
    wallet = Wallet(phrase)

    query = THORChainQuery()
    amm = THORChainAMM(wallet, query, dry_run=DRY_RUN)

    # noinspection PyTypeChecker
    bsc: BinanceSmartChainClient = wallet.get_client(Chain.BinanceSmartChain)
    print("BSC1 address: ", bsc.get_address())
    source_client = bsc

    balances = await source_client.get_balance(with_erc20=True)
    print('Balances: ')
    for b in balances:
        print(f'{b.amount.format()} {b.asset}')

    # balance_bsc = await source_client.get_gas_balance()
    # print("BSC balance: ", balance_bsc)
    #
    # usdt = await source_client.get_erc20_token_info(AssetBSC_USDT)
    # print(f"BSC USDT: {usdt}")
    #
    # balance_bsc_usdt = await source_client.get_erc20_token_balance(AssetBSC_USDT)
    # print(f"BSC.USDT balance: {balance_bsc_usdt}")

    my_address = source_client.get_address()

    # pick a gas option
    gas = GasOptions.automatic(FeeOption.FAST)
    # gas = GasOptions.legacy(gas_price=50, gas_limit=210000)
    # gas = GasOptions.eip1559_in_gwei(max_fee_per_gas=1, max_priority_fee_per_gas=1, gas_limit=210000)

    from_amount = CryptoAmount.automatic(5.0, AssetBSC_USDT)

    if await amm.is_tc_router_approved_to_spend(from_amount):
        print("Router is approved to spend the asset.")
    else:
        print("Router is not approved to spend the asset.")
        print("Approving...")
        tx_hash = await amm.approve_tc_router_to_spend(from_amount, gas_options=gas)
        print(f"Approval tx hash {tx_hash} ({source_client.get_explorer_tx_url(tx_hash)})")

    to_asset = Asset.automatic('AVAX.AVAX').upper()

    print(f"I will swap {from_amount} to {to_asset}.")
    input("Press Enter to send TX...")

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

    print(f"Swap tx hash {tx_hash} ({source_client.get_explorer_tx_url(tx_hash)})")

    await source_client.wait_for_transaction(tx_hash)

    print("Transaction mined.")

    await asyncio.sleep(1)
    await amm.close()


if __name__ == "__main__":
    asyncio.run(main())

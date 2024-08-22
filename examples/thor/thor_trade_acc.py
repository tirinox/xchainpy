"""
This example demonstrates how to trade deposit and withdraw Trade Assets on the THORChain network.
Just don't forget to pass PHRASE environment variable that contains a mnemonic phrase of your wallet.
"""

import asyncio
import os

from examples.common import thorchain_wait_tx_status
from xchainpy2_thorchain_amm import Wallet, THORChainAMM
from xchainpy2_utils import Chain, CryptoAmount, AssetLTC, AssetBSC, RUNE_DECIMAL


async def display_trade_balances(amm: THORChainAMM):
    print('Loading your balances...')
    balances = await amm.wallet.get_all_balances()
    print(f"Balances: ")
    for i, chain_bal in  enumerate(balances.balances.values(), start=1):
        print(f'  {i}. {chain_bal.address}:')
        for bal in chain_bal.balances:
            print(f'    * {bal}')


async def main(seed_phrase):
    wallet = Wallet(seed_phrase, enabled_chains={
        Chain.THORChain,
        # Chain.Avalanche,
        # Chain.Cosmos,
        Chain.Litecoin,
        Chain.BinanceSmartChain
    })
    async with THORChainAMM(wallet) as amm:
        await display_trade_balances(amm)

        # ---------------------- DEPOSIT L1 to Trade Account ----------------------

        amt_to_deposit = CryptoAmount.automatic(0.05, AssetLTC)
        if input(f'Do you want to deposit Trade Asset {amt_to_deposit}? (y/n): ').lower() == 'y':
            print(f'Deposit {amt_to_deposit} to Trade Account is in progress...')
            tx_hash = await amm.deposit_to_trade_account(amt_to_deposit)
            await thorchain_wait_tx_status(amm, tx_hash)
            await display_trade_balances(amm)

        # -------------------------------- SWAP -----------------------------------

        amt_to_swap = CryptoAmount.automatic(0.05, AssetLTC.as_trade)
        dest_asset = AssetBSC.as_trade  # to trade BSC~BNB
        if input(f'Do you want to swap Trade Asset {amt_to_swap}? (y/n): ').lower() == 'y':
            print(f'Swapping {amt_to_swap} to is in progress...')
            tx_hash = await amm.do_swap(
                amt_to_swap,
                dest_asset,
            )
            await thorchain_wait_tx_status(amm, tx_hash)
            await display_trade_balances(amm)

        # ---------------------- WITHDRAW Trade Account to L1 ----------------------

        amt_to_withdraw = CryptoAmount.automatic(0.005, AssetBSC.as_trade)
        amt_to_withdraw = amt_to_withdraw.changed_decimals(RUNE_DECIMAL)
        if input(f'Do you want to withdraw Trade Asset {amt_to_withdraw}? (y/n): ').lower() == 'y':
            print(f'Withdraw {amt_to_withdraw} from Trade Account is in progress...')
            tx_hash = await amm.withdraw_from_trade_account(amt_to_withdraw)
            await thorchain_wait_tx_status(amm, tx_hash)
            await display_trade_balances(amm)


if __name__ == "__main__":
    phrase = os.environ.get('PHRASE')
    if not phrase:
        raise Exception('Please pass PHRASE environment variable to run this example!')

    asyncio.run(main(phrase))

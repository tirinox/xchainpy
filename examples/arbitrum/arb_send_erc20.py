import asyncio

from examples.common import get_phrase, sep
from xchainpy2_arbitrum import ArbitrumClient
from xchainpy2_client import FeeOption
from xchainpy2_ethereum import GasOptions
from xchainpy2_utils import NetworkType, Asset, CryptoAmount

Asset_USDC_ARB = Asset.from_string("ARB.USDC-0xaf88d065e77c8cc2239327c5edb3a432268e5831").upper()


async def main():
    phrase = get_phrase()
    arb1 = ArbitrumClient(phrase=phrase, network=NetworkType.MAINNET, wallet_index=0)
    arb2 = ArbitrumClient(phrase=phrase, network=NetworkType.MAINNET, wallet_index=1)

    arb1.gas_limit_estimation = True

    print("Arbitrum 1 address: ", arb1.get_address())
    print("Arbitrum 2 address: ", arb2.get_address())
    sep("BEFORE")

    balance1 = await arb1.get_gas_balance()
    print(f"Arbitrum 1 balance: {balance1}")

    usdc1 = await arb1.get_erc20_token_balance(Asset_USDC_ARB)

    print(f"Arbitrum 1 USDC balance: {usdc1}")

    ## manual
    # gas = GasOptions.legacy(161224000, 200000)
    ## set from block
    # gas_price = arb1.web3.eth.gas_price
    # print("Gas price: ", gas_price)
    # gas = GasOptions.legacy(gas_price, 100000)

    ## automatic fee
    gas = GasOptions.automatic(FeeOption.FAST)

    amount = CryptoAmount.automatic(0.01, Asset_USDC_ARB, 6)
    print(f"Transferring {amount} to {arb1.get_address()}")
    # input("Press Enter to send TX...")

    # note! memo is not supported for ERC20 transfers
    tx_hash = await arb1.transfer(amount, arb2.get_address(), gas=gas)
    print(f"Transfer tx hash {arb1.get_explorer_tx_url(tx_hash)}")

    await arb1.wait_for_transaction(tx_hash)
    print("Transaction mined")

    sep("AFTER")
    usdc1 = await arb1.get_erc20_token_balance(Asset_USDC_ARB)
    usdc2 = await arb2.get_erc20_token_balance(Asset_USDC_ARB)

    print(f"Arbitrum 1 USDC balance: {usdc1}")
    print(f"Arbitrum 2 USDC balance: {usdc2}")


if __name__ == "__main__":
    asyncio.run(main())

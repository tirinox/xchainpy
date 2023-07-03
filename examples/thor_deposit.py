import asyncio

from xchainpy2_crypto import generate_mnemonic
from xchainpy2_thorchain import THORChainClient, build_deposit_tx_unsigned
from xchainpy2_utils import CryptoAmount, Amount, AssetRUNE


async def low_level_demo_build_deposit_tx(phrase=None):
    phrase = phrase or generate_mnemonic()
    client = THORChainClient(phrase=phrase)

    public_key = client.get_public_key()
    address = client.get_address()

    account = await client.get_account(address)

    tx = build_deposit_tx_unsigned(
        CryptoAmount(Amount.zero(), AssetRUNE),
        '=:BTC/BTC',
        public_key,
        fee=client.get_amount_string(0),
        prefix=client.prefix,
        sequence_num=account.sequence,
    )

    tx.sign(
        client.get_private_key_cosmos(),
        client.get_chain_id(),
        account_number=account.number
    )

    print(tx)


async def main():
    await low_level_demo_build_deposit_tx()


if __name__ == "__main__":
    asyncio.run(main())

import asyncio

from xchainpy2_crypto import generate_mnemonic
from xchainpy2_thorchain import THORChainClient, build_deposit_tx_unsigned
from xchainpy2_utils import CryptoAmount, Amount, AssetRUNE, RUNE_DECIMAL


async def low_level_demo_build_deposit_tx(client: THORChainClient, broadcast=False):
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
    tx.complete()

    if broadcast:
        result = await client.broadcast_tx(tx.tx.SerializeToString())
        return result
    else:
        return tx


async def demo_simple_deposit(client: THORChainClient):
    txhash = await client.deposit(
        CryptoAmount(Amount.automatic(2.0, RUNE_DECIMAL), AssetRUNE),
        memo='=:BTC/BTC'
    )
    print(f"TX sumbitted: {txhash}!")


async def main(phrase=None):
    phrase = phrase or generate_mnemonic()
    client = THORChainClient(phrase=phrase)

    await low_level_demo_build_deposit_tx(client)


if __name__ == "__main__":
    asyncio.run(main())

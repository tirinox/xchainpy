import asyncio
import os

from xchainpy2_crypto import generate_mnemonic
from xchainpy2_thorchain import THORChainClient, build_deposit_tx_unsigned
from xchainpy2_utils import CryptoAmount, Amount, AssetRUNE


async def main():
    """
    This example requires a real wallet with some amount of Rune
    (1 Rune will be more than enough)
    Just don't forget to pass PHRASE environment variable that contains a mnemonic phrase of your wallet
    """
    public_key = client.get_public_key()
    address = client.get_address()
    print(f'Your address: {address}')

    account = await client.get_account(address)
    if not account:
        raise Exception('Account not found')

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

    result = await client.broadcast_tx(tx.tx.SerializeToString())
    print(f'TX submitted: {result}')


if __name__ == "__main__":
    phrase = os.environ.get('PHRASE')
    if not phrase:
        raise Exception('Please pass PHRASE environment variable to run this example!')

    client = THORChainClient(phrase=phrase)

    asyncio.run(main())

import asyncio

from examples.common import get_phrase
from xchainpy2_bitcoincash import BitcoinCashClient
from xchainpy2_thorchain_query import THORChainQuery
from xchainpy2_utils import Chain


async def main():
    phrase = get_phrase()
    bch_client1 = BitcoinCashClient(phrase=phrase)
    bch_client2 = BitcoinCashClient(phrase=phrase, wallet_index=1)
    print(f"Address1: {bch_client1.get_address()}")
    print(f"Address2: {bch_client2.get_address()}")

    # balance = await bch_client.get_balance('bitcoincash:qpcjl9qak89t5fexnspfpvzqs6tcaytzcqeex48k8t')
    # print(balance)

    # tx_contents = await bch_client1.get_transaction_data('A914E88F070440754D7967607D4D1447F6229117B715308749DE3A912373E831')
    # print(tx_contents)
    #
    transactions = await bch_client1.get_transactions('bitcoincash:qq2m0assgsqq3ek7currz4grzka9hxcdpu3q43wezh')
    print(transactions)

    # query = THORChainQuery()
    # fee = await query.get_recommended_fee_rate(Chain.BitcoinCash)
    # print(fee)
    #
    # tx_hash = await bch_client1.transfer(
    #     what=bch_client1.gas_amount(0.0001),
    #     recipient=bch_client2.get_address(),
    #     memo="test memo",
    #     fee_rate=fee,
    # )
    # print(f"TxHash: {tx_hash}, {bch_client1.get_explorer_tx_url(tx_hash)}")
    #


if __name__ == '__main__':
    asyncio.run(main())
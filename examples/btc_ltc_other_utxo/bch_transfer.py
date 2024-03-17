import asyncio

from examples.common import get_phrase
from xchainpy2_bitcoincash import BitcoinCashClient


async def main():
    phrase = get_phrase()
    bch_client = BitcoinCashClient(phrase=phrase)
    print(bch_client.get_address())

    balance = await bch_client.get_balance('bitcoincash:qpcjl9qak89t5fexnspfpvzqs6tcaytzcqeex48k8t')
    print(balance)


if __name__ == '__main__':
    asyncio.run(main())
import asyncio
import datetime
import os

from xchainpy2_client import TxType
from xchainpy2_crypto import generate_mnemonic
from xchainpy2_thorchain import THORChainClient, make_client_urls_from_ip_address
from xchainpy2_utils import AssetRUNE

# >> Default Client (9R provider), the public nodes are severely rate-limited
client = THORChainClient()

# >> In case you have own full-node:
# ip = os.environ.get('THORNODE_IP_ADDRESS') or '1.2.3.4'
# client = THORChainClient(phrase=generate_mnemonic(),
#                          client_urls=make_client_urls_from_ip_address(ip))

EXAMPLE_TX_SEND = '03F2F2C29F2F1E6FE318065F775BC6E3E47053BD7AE2910A406FF22351792CEA'

EXAMPLE_TX_SYNTH_SEND = 'B81A5E86501CFC4FBA5BCF940A505C94A544247A353E0BEF273359973BAEAE73'
EXAMPLE_TX_BOND = '729A5F240A183C91A94D0D0D6C9AD87E73778DF935DFFEFAE66ADB6F465B9CF0'

# Rune => synth BTC
EXAMPLE_TX_SWAP = 'A24A2F707A8B030519194170809107391AE4DC45F70A7E259FE4917AAF279EEE'

# TWT => BUSD
EXAMPLE_TX_SWAP_2 = 'DB5C52697308CA453C36A23113E732E4851495F22A9314CDCFD1846A0BE9DC45'

# This is ETH tx, but it's THORChain inbound, so it also must be loaded
EXAMPLE_INBOUND_ETH_TX = 'F81B40BBCF35313702D99FB1CB1B5CEB83A2570543161E4161D5B739F2866C8E'


async def tx_test_send():
    tx_id = EXAMPLE_TX_SEND

    tx_data = await client.get_transaction_data(tx_id)
    print(tx_data)
    assert tx_data
    assert tx_data.height == 11_689_548
    assert tx_data.date == datetime.datetime(2023, 7, 13, 16, 0, 28)

    assert tx_data.transfers
    from0 = tx_data.inbound_txs[0]
    assert from0.amount.internal_amount == 33666111337
    assert from0.amount.decimals == 8
    assert from0.asset == AssetRUNE
    assert from0.from_address == 'thor1vl9tf7dsc82f6g76hmdtjzdn73pw5w3wm9fqaq'

    assert tx_data.outbound_txs
    to0 = tx_data.outbound_txs[0]
    assert to0.address == 'thor1gyap83aenguyhce3a0y3gprap32ypuc99m4wfg'
    assert to0.asset == AssetRUNE
    assert to0.amount == from0.amount

    assert tx_data.type == TxType.TRANSFER


async def tx_test_swap1():
    tx_id = EXAMPLE_TX_SWAP

    tx_data = await client.get_transaction_data(tx_id)
    print(tx_data)


async def tx_test_swap_external():
    tx_id = EXAMPLE_INBOUND_ETH_TX
    tx_data = await client.get_transaction_data(tx_id)
    print(tx_data)


async def read_txs_of_address():
    txs = await client.get_transactions('thor1cghgr0dneyymxx6fjq3e72q83z0qz7c3yttadx')
    print(txs)


async def main(phrase=None):
    # await read_txs_of_address()
    await tx_test_send()
    # await tx_test_swap1()
    # await tx_test_swap_external()


if __name__ == "__main__":
    asyncio.run(main())

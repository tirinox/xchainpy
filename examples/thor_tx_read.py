import asyncio
import os

from examples.common import sep
from xchainpy2_thorchain import THORChainClient
from xchainpy2_utils import AssetRUNE, AssetBTC, AssetETH

# >> Default Client (9R provider), the public nodes are severely rate-limited
# client = THORChainClient()


# >> In case you have own full-node:
ip = os.environ.get('THORNODE_IP_ADDRESS') or '1.2.3.4'
client = THORChainClient.from_node_ip(ip)


async def demo_read_external_tx_in_out():
    sep('Inbound TX')
    tx_id = '31605D8C2287482EFCDE76D07B1B641C4A1955C8977D1430A7BC80A7667951EA'  # BTC
    print(client.get_explorer_tx_url(tx_id))
    tx = await client.get_transaction_data(tx_id)
    print(tx)
    assert tx.asset == AssetBTC
    assert tx.height == 13382572
    assert len(tx.transfers) == 1
    assert tx.transfers[0].amount.internal_amount == 6000000
    assert tx.transfers[0].amount.decimals == 8
    assert tx.transfers[0].from_address == 'bc1qy9pluaye4ggdhlcf7q3e5n0p68rxum4m83rxgm'
    assert tx.memo == '=:ETH.ETH:0x71E5eED74c467b5a33290e11b0e458977F4C1681:0/1/0:te:0'

    sep('Outbound TX')
    tx_id = '623C57606865B78F2AA7F51BF6F9E41D229C37BE3899915DA3DA7B54BA141E9E'
    print(client.get_explorer_tx_url(tx_id))
    tx = await client.get_transaction_data(tx_id)
    print(tx)
    assert tx.asset == AssetETH
    assert tx.height == 13382652
    assert len(tx.transfers) == 1
    assert tx.transfers[0].amount.internal_amount == 103543345
    assert tx.transfers[0].amount.decimals == 8  # 8 decimals for all in TC
    assert tx.transfers[0].to_address == '0x71E5eED74c467b5a33290e11b0e458977F4C1681'
    assert tx.transfers[0].from_address == '0x1f3b3c6ac151bf32409fe139a5d55f3d9444729c'


async def demo_read_tx_internal_transfer():
    # this is a swap in Maya, but from TC's viewpoint, it is a regular native transfer
    tx_id = '03F2F2C29F2F1E6FE318065F775BC6E3E47053BD7AE2910A406FF22351792CEA'
    print(client.get_explorer_tx_url(tx_id))
    tx = await client.get_transaction_data(tx_id)
    print(tx)
    assert len(tx.transfers) == 1
    assert tx.hash == tx_id
    assert tx.height == 13379930
    assert tx.asset == AssetRUNE
    assert tx.transfers[0].amount.as_asset == 950.0
    assert tx.transfers[0].asset == AssetRUNE
    assert tx.transfers[0].to_address == 'thor1l9ftj9w47pmdhcs6rhgtyg2yyy8264ld2fwpcp'
    assert tx.transfers[0].from_address == 'thor198w2r5cwlamwmw0uyj90hvd6qp5svjvxa65jc2'
    assert tx.transfers[0].outbound

    # Swap (msg.Deposit)
    tx_id = '113E0389463871FAD2E115EEFAFDCBAD1A0BF25A516D3F71978FC1B9B22F5EFD'
    print(client.get_explorer_tx_url(tx_id))
    tx = await client.get_transaction_data(tx_id)
    print(tx)
    assert len(tx.transfers) == 1
    assert tx.transfers[0].amount.internal_amount == 31139000
    assert tx.transfers[0].asset == AssetETH.as_synth
    assert tx.transfers[0].from_address == 'thor166n4w5039meulfa3p6ydg60ve6ueac7tlt0jws'
    assert tx.transfers[0].to_address == 'thor1g98cy3n9mmjrpn0sxmn63lztelera37n8n67c0'  # pool
    assert tx.transfers[0].outbound


async def read_txs_of_address():
    txs = await client.get_transactions('thor1cghgr0dneyymxx6fjq3e72q83z0qz7c3yttadx')
    print(txs)
    assert txs.total >= 85
    assert len(txs.txs) == 20


async def main():
    # await demo_read_tx_internal_transfer()
    # await demo_read_external_tx_in_out()
    await read_txs_of_address()


if __name__ == "__main__":
    asyncio.run(main())

import pytest

from xchainpy2_client import TxType
from xchainpy2_cosmos import CosmosGaiaClient, COSMOS_DECIMAL
from xchainpy2_crypto import generate_mnemonic
from xchainpy2_utils import AssetATOM, Chain, NetworkType, Amount


@pytest.fixture
def cosm_client():
    return CosmosGaiaClient(phrase=generate_mnemonic())


def test_create(cosm_client):
    assert cosm_client._denom == 'uatom'
    assert cosm_client._gas_asset == AssetATOM
    assert cosm_client.chain == Chain.Cosmos
    assert cosm_client.network == NetworkType.MAINNET


def test_address():
    mn = generate_mnemonic()
    for i in range(100):
        cosm_client = CosmosGaiaClient(phrase=mn, wallet_index=i)
        address = cosm_client.get_address()
        assert cosm_client.validate_address(address)
        assert len(cosm_client.get_private_key()) == 64
        assert cosm_client.get_private_key_cosmos()
        assert len(cosm_client.get_public_key().public_key_bytes) == 33


def test_explorer(cosm_client):
    assert cosm_client.get_explorer_address_url('cosmos1mn7yrfn5ycmxsmtqvhvcac8yzyh34aknzpdkf7') \
           == 'https://www.mintscan.io/cosmos/account/cosmos1mn7yrfn5ycmxsmtqvhvcac8yzyh34aknzpdkf7'

    assert cosm_client.get_explorer_tx_url('212418055DB195796242BFDC5F26956BFBE81EF44151B73361A5BEACA989D096') \
           == 'https://www.mintscan.io/cosmos/txs/' \
              '212418055DB195796242BFDC5F26956BFBE81EF44151B73361A5BEACA989D096'


@pytest.mark.asyncio
async def test_balance(cosm_client):
    assert await cosm_client.get_balance() == []
    real_bal = await cosm_client.get_balance('cosmos1p3ucd3ptpw902fluyjzhq3ffgq4ntddac9sa3s')
    assert real_bal and isinstance(real_bal, list)
    for bal in real_bal:
        if bal.asset == AssetATOM:
            assert bal.amount.internal_amount > 100


@pytest.mark.asyncio
async def test_get_tx(cosm_client):
    tx_id = '6E5A04808C558AA35624487522B16D48275DC3D368330811ACD3020A7BDB6183'
    tx = await cosm_client.get_transaction_data(tx_id)
    assert tx
    assert tx.height == 17_945_199
    assert tx.type == TxType.TRANSFER
    assert len(tx.transfers) == 1
    tr = tx.transfers[0]
    assert tr.from_address == 'cosmos1qes70g8hc3nv7gdcyg2npjjxy4nwmxc0ege93f'
    assert tr.to_address == 'cosmos1hfdkewc9cuzdkh4f498a8e4a3hh0qpqm83s82k'
    assert tr.asset == AssetATOM
    assert tx.asset == AssetATOM
    assert tr.amount == Amount.from_base(715197, COSMOS_DECIMAL)


def test_pk_init(cosm_client):
    client2 = CosmosGaiaClient(private_key=cosm_client.get_private_key())
    assert client2.get_address() == cosm_client.get_address()
    assert client2.get_private_key() == cosm_client.get_private_key()
    assert client2.get_public_key().public_key_bytes == cosm_client.get_public_key().public_key_bytes

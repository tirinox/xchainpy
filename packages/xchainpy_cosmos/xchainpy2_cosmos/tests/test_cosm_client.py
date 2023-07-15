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
    assert cosm_client.native_asset == AssetATOM
    assert cosm_client.chain == Chain.Cosmos
    assert cosm_client.network == NetworkType.MAINNET


def test_address(cosm_client):
    for i in range(100):
        address = cosm_client.get_address(i)
        assert cosm_client.validate_address(address)

        assert len(cosm_client.get_private_key(i)) == 64
        assert cosm_client.get_private_key_cosmos(i)
        assert len(cosm_client.get_public_key(i).public_key_bytes) == 33


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
    tx_id = 'D171BD459167FB159FD68CA1BF24110FF1CC635B769067853917366503434CBE'
    tx = await cosm_client.get_transaction_data(tx_id)
    assert tx
    assert tx.height == 16_143_708
    assert tx.type == TxType.TRANSFER
    assert len(tx.to_txs) == 1 and len(tx.from_txs) == 1
    assert tx.to_txs[0].address == 'cosmos1j8pp7zvcu9z8vd882m284j29fn2dszh05cqvf9'
    assert tx.from_txs[0].from_address == 'cosmos1mn7yrfn5ycmxsmtqvhvcac8yzyh34aknzpdkf7'
    assert tx.to_txs[0].amount == Amount.automatic(1470000, COSMOS_DECIMAL) == tx.from_txs[0].amount
    assert tx.to_txs[0].asset == tx.from_txs[0].asset == AssetATOM

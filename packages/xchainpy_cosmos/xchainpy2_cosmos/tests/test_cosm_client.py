import pytest

from xchainpy2_cosmos import CosmosGaiaClient
from xchainpy2_crypto import generate_mnemonic
from xchainpy2_utils import AssetATOM, Chain, NetworkType


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


@pytest.mark.asyncio
async def test_balance(cosm_client):
    assert await cosm_client.get_balance() == []
    real_bal = await cosm_client.get_balance('cosmos1p3ucd3ptpw902fluyjzhq3ffgq4ntddac9sa3s')
    assert real_bal and isinstance(real_bal, list)
    for bal in real_bal:
        if bal.asset == AssetATOM:
            assert bal.amount.internal_amount > 100

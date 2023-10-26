import pytest
import pytest_asyncio

from xchainpy2_client import XcTx, TxType
from xchainpy2_utils import Chain, AssetBTC, AssetLTC, Amount
# noinspection PyUnresolvedReferences
from .helpers import event_loop
from .. import BlockCypherProvider


@pytest_asyncio.fixture(scope="module")
async def bc():
    bc = BlockCypherProvider.default_bitcoin()
    yield bc
    await bc.session.close()


@pytest_asyncio.fixture(scope="module")
async def bc_litecoin():
    bc = BlockCypherProvider.default_litecoin()
    yield bc
    await bc.session.close()


def test_init(bc):
    assert bc.chain == Chain.Bitcoin
    assert bc.asset.chain == 'BTC'
    assert str(bc.asset) == 'BTC.BTC'
    assert bc.asset_decimal == 8


@pytest.mark.asyncio
async def test_get_txs(bc):
    r = await bc._api_get_txs('1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa', limit=1)
    assert len(r) > 0


@pytest.mark.asyncio
async def test_get_txs_normal(bc):
    txs = await bc.get_transactions('1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa', limit=10)

    assert len(txs) > 1


@pytest.mark.asyncio
async def test_get_tx_data(bc):
    tx = await bc.get_transaction_data('dbc6c7c1f4bf7c040655a9718ee4c2e1f7426f4a01ebaaaacee575bdf2d27ff8')
    assert isinstance(tx, XcTx)
    assert len(tx.to_txs) == 2
    assert len(tx.from_txs) == 2
    assert tx.type == TxType.TRANSFER
    assert tx.asset == AssetBTC
    assert tx.height == 813956
    print(tx)

    # non-existent
    tx = await bc.get_transaction_data('123456789123456789')
    assert tx is None


@pytest.mark.asyncio
async def test_get_txs_balance(bc):
    balances = await bc.get_balance('1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa', confirmed_only=True)
    assert len(balances) == 1
    balance = balances[0]
    assert balance.asset == bc.asset == AssetBTC
    assert float(balance.amount) > 72.71


@pytest.mark.asyncio
async def test_init_litecoin(bc_litecoin):
    assert bc_litecoin.chain == Chain.Litecoin
    assert bc_litecoin.asset.chain == 'LTC'
    assert str(bc_litecoin.asset) == 'LTC.LTC'
    assert bc_litecoin.asset_decimal == 8


@pytest.mark.asyncio
@pytest.mark.parametrize(('address', 'expected_balance'), [
    ('MU4ZU2ewr2vsvcdiuzzYckJiwEo7ARYK8v', 100_000),
    ('ltc1qx2x5cqhymfcnjtg902ky6u5t5htmt7fvqztdsm028hkrvxcl4t2s300al6', 100_000),
    ('ltcNotExists', -1),  # not
])
async def test_get_txs_balance_ltc(bc_litecoin, address, expected_balance):
    balances = await bc_litecoin.get_balance(address, confirmed_only=True)
    if expected_balance < 0:
        assert len(balances) == 0
    else:
        assert len(balances) == 1
        balance = balances[0]
        assert balance.asset == bc_litecoin.asset == AssetLTC
        assert float(balance.amount) > expected_balance

@pytest.mark.asyncio
async def test_get_tx_data_ltc(bc_litecoin):
    # non-existent
    tx = await bc_litecoin.get_transaction_data('123456789098765432123456789098765432123456789876543')
    assert tx is None

    tx = await bc_litecoin.get_transaction_data('a42d1959613152c786134305ffca5c42c0008aa23aa4fd1405ad96bdf9cb95f4')
    assert isinstance(tx, XcTx)
    assert tx.asset == AssetLTC
    assert tx.height == 2568095
    assert len(tx.from_txs) == 4
    assert len(tx.to_txs) == 2
    assert tx.from_txs[3].amount == Amount.from_asset(0.30042918, 8).as_base
    assert tx.from_txs[3].asset == AssetLTC
    assert tx.from_txs[3].from_address == 'ltc1qq7l2aplmmzqlkacekuauqr6unwfytutuzgkgwq'

    assert tx.to_txs[0].address == 'ltc1qp4zm5e0a2s36cw5h5gfr64lzverrxvzn0ef9kg'
    assert tx.to_txs[0].amount == Amount.from_asset(0.06260656, 8).as_base
    assert tx.to_txs[0].asset == AssetLTC

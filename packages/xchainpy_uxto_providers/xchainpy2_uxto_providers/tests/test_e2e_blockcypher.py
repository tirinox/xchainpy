import asyncio

import pytest
import pytest_asyncio

from xchainpy2_utils import Chain, AssetBTC
from .. import BlockCypherProvider


# to fix broader scope
@pytest.fixture(scope="session")
def event_loop():
    return asyncio.get_event_loop()


@pytest_asyncio.fixture(scope="module")
async def bc():
    bc = BlockCypherProvider.default_bitcoin()
    yield bc
    await bc.session.close()


def test_init(bc):
    assert bc.chain == Chain.Bitcoin
    assert bc.asset.chain == 'BTC'
    assert str(bc.asset) == 'BTC.BTC'
    assert bc.asset_decimal == 8


@pytest.mark.asyncio
async def test_get_txs(bc):
    r = await bc._get_txs_api('1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa', limit=1)
    assert len(r) > 0


@pytest.mark.asyncio
async def test_get_txs_normal(bc):
    txs = await bc.get_transactions('1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa', limit=10)

    assert len(txs) == 10


@pytest.mark.asyncio
async def test_get_txs_balance(bc):
    balances = await bc.get_balance('1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa', confirmed_only=True)
    assert len(balances) == 1
    balance = balances[0]
    assert balance.asset == bc.asset == AssetBTC
    assert float(balance.amount) > 72.71

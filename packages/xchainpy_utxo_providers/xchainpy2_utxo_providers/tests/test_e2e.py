"""
    All the UTXO data providers must return the same data
    That's why we run the same test for every provider that supports certain blockchain
"""
from xchainpy2_client import XcTx, TxType
from xchainpy2_utils import Chain, AssetBTC
from .helpers import *
from .. import BlockCypherProvider, HaskoinProvider


@pytest.fixture
def bitcoin_providers(provider_getter: callable):
    return (
        provider_getter(HaskoinProvider.default_bitcoin),
        provider_getter(BlockCypherProvider.default_bitcoin),

        # At the moment, SochainProvider requires a paid API key, so we can't test it
        # provider_getter(SochainProvider.default_bitcoin),
    )


def test_init_btc(bitcoin_providers):
    for provider in bitcoin_providers:
        assert provider.chain == Chain.Bitcoin
        assert provider.asset.chain == 'BTC'
        assert str(provider.asset) == 'BTC.BTC'
        assert provider.asset_decimal == 8


@pytest.mark.parametrize(('address',), [
    ('bc1qlfwzwzjt4klxc6rxw34r29svecgymz25a94rnh',),
    ('1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa',),
])
@pytest.mark.asyncio
async def test_get_txs_btc(bitcoin_providers, address):
    for provider in bitcoin_providers:
        txs = await provider.get_transactions(address, limit=10)
        assert len(txs) > 1


@pytest.mark.asyncio
async def test_get_tx_data_btc(bitcoin_providers):
    for provider in bitcoin_providers:
        tx = await provider.get_transaction_data('dbc6c7c1f4bf7c040655a9718ee4c2e1f7426f4a01ebaaaacee575bdf2d27ff8')
        assert isinstance(tx, XcTx)
        assert len(tx.to_txs) == 2
        assert len(tx.from_txs) == 2
        assert tx.type == TxType.TRANSFER
        assert tx.asset == AssetBTC
        assert tx.height == 813956
        print(tx)

        # non-existent
        tx = await provider.get_transaction_data('123456789123456789')
        assert tx is None


# @pytest.mark.asyncio
# async def test_get_txs_balance(block_cypher_btc):
#     balances = await block_cypher_btc.get_balance('1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa', confirmed_only=True)
#     assert len(balances) == 1
#     balance = balances[0]
#     assert balance.asset == block_cypher_btc.asset == AssetBTC
#     assert float(balance.amount) > 72.71
#
#
# @pytest.mark.asyncio
# async def test_init_litecoin(block_cypher_ltc):
#     assert block_cypher_ltc.chain == Chain.Litecoin
#     assert block_cypher_ltc.asset.chain == 'LTC'
#     assert str(block_cypher_ltc.asset) == 'LTC.LTC'
#     assert block_cypher_ltc.asset_decimal == 8
#
#
# @pytest.mark.asyncio
# @pytest.mark.parametrize(('address', 'expected_balance'), [
#     ('MU4ZU2ewr2vsvcdiuzzYckJiwEo7ARYK8v', 100_000),
#     ('ltc1qx2x5cqhymfcnjtg902ky6u5t5htmt7fvqztdsm028hkrvxcl4t2s300al6', 100_000),
#     ('ltcNotExists', -1),  # not
# ])
# async def test_get_txs_balance_ltc(block_cypher_ltc, address, expected_balance):
#     balances = await block_cypher_ltc.get_balance(address, confirmed_only=True)
#     if expected_balance < 0:
#         assert len(balances) == 0
#     else:
#         assert len(balances) == 1
#         balance = balances[0]
#         assert balance.asset == block_cypher_ltc.asset == AssetLTC
#         assert float(balance.amount) > expected_balance
#
#
# @pytest.mark.asyncio
# async def test_get_tx_data_ltc(block_cypher_ltc):
#     # non-existent
#     tx = await block_cypher_ltc.get_transaction_data('123456789098765432123456789098765432123456789876543')
#     assert tx is None
#
#     tx = await block_cypher_ltc.get_transaction_data('a42d1959613152c786134305ffca5c42c0008aa23aa4fd1405ad96bdf9cb95f4')
#     assert isinstance(tx, XcTx)
#     assert tx.asset == AssetLTC
#     assert tx.height == 2568095
#     assert len(tx.from_txs) == 4
#     assert len(tx.to_txs) == 2
#     assert tx.from_txs[3].amount == Amount.from_asset(0.30042918, 8).as_base
#     assert tx.from_txs[3].asset == AssetLTC
#     assert tx.from_txs[3].from_address == 'ltc1qq7l2aplmmzqlkacekuauqr6unwfytutuzgkgwq'
#
#     assert tx.to_txs[0].address == 'ltc1qp4zm5e0a2s36cw5h5gfr64lzverrxvzn0ef9kg'
#     assert tx.to_txs[0].amount == Amount.from_asset(0.06260656, 8).as_base
#     assert tx.to_txs[0].asset == AssetLTC

"""
    All the UTXO data providers must return the same data
    That's why we run the same test for every provider that supports certain blockchain
"""
from xchainpy2_client import XcTx, TxType, UtxoOnlineDataProvider
from xchainpy2_utils import Chain, AssetBTC, AssetLTC
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


@pytest.fixture
def litecoin_providers(provider_getter: callable):
    return (
        provider_getter(BlockCypherProvider.default_litecoin),
    )


@pytest.fixture
def doge_providers(provider_getter: callable):
    return (
        provider_getter(BlockCypherProvider.default_doge),
    )


@pytest.fixture
def dash_providers(provider_getter: callable):
    return (
        provider_getter(BlockCypherProvider.default_dash),
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
        in_0 = tx.from_txs[0]
        out_1 = tx.to_txs[1]

        assert in_0.amount == amt(0.00503255)
        assert in_0.asset == AssetBTC
        assert in_0.from_address == '3DjWJHahgCo44QVDeF8oT5E96pqfxt5SG7'

        assert out_1.amount == amt(0.00752373)
        assert out_1.address == '3HHCPo96xJN8JbpGuPMoc2hxsFSDMWY53o'
        assert out_1.asset == AssetBTC

        # non-existent
        with pytest.raises(Exception):
            await provider.get_transaction_data('123456789123456789')


VALID_BUT_OLD_TX_HASH = ("02000000000101f232bf6b783b6049a4b6639ad4647ce9dd05e81ba2ba23b2b250b47dfa2ac26e0200000000"
                         "ffffffff0380ec360700000000160014f55f6537a0c9cdf76f63e7a7c6fdf4bd136666ad0000000000000000"
                         "456a433d3a4254432f4254433a74686f723137756e66746b64657577637971727378333277707a71736d6a6a"
                         "796c37796d356e61356671663a3132303630343235352f312f304cf40e0000000000160014fa5c270a4badbe"
                         "6c6866746a35160cce104d89540247304402203c581116c41319e3faa2c55cad2d376d9ca68bf54462fd479d"
                         "ebcf206c0bde6a02201be41d2f5feea648e2f84561d743c31a9f2eea6ac890d90610e8f2800b33fb27012103"
                         "4fdeebd1c8d8d8380da4332801283e13acbf498c84b957fffdda647d1688178100000000")


@pytest.mark.asyncio
async def test_broadcast(bitcoin_providers):
    for provider in bitcoin_providers:
        provider: UtxoOnlineDataProvider

        await provider.broadcast_tx(VALID_BUT_OLD_TX_HASH)


@pytest.mark.asyncio
async def test_get_txs_balance(bitcoin_providers):
    for provider in bitcoin_providers:
        balances = await provider.get_balance('1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa', confirmed_only=True)
        assert len(balances) == 1
        balance = balances[0]
        assert balance.asset == provider.asset == AssetBTC
        assert float(balance.amount) > 72.71


@pytest.mark.asyncio
async def test_get_txs_balance_not_exists(bitcoin_providers):
    for provider in bitcoin_providers:
        with pytest.raises(Exception):
            await provider.get_balance('1A1zPnonExistsAddress', confirmed_only=True)


@pytest.mark.asyncio
async def test_init_litecoin(litecoin_providers):
    for provider in litecoin_providers:
        assert provider.chain == Chain.Litecoin
        assert provider.asset.chain == 'LTC'
        assert str(provider.asset) == 'LTC.LTC'
        assert provider.asset_decimal == 8


@pytest.mark.asyncio
@pytest.mark.parametrize(('address', 'expected_balance'), [
    ('MU4ZU2ewr2vsvcdiuzzYckJiwEo7ARYK8v', 100_000),
    ('ltc1qx2x5cqhymfcnjtg902ky6u5t5htmt7fvqztdsm028hkrvxcl4t2s300al6', 100_000),
    ('ltcNotExists', -1),  # not
])
async def test_get_txs_balance_ltc(litecoin_providers, address, expected_balance):
    for provider in litecoin_providers:
        if expected_balance < 0:
            with pytest.raises(Exception):
                balances = await provider.get_balance(address, confirmed_only=True)
                assert len(balances) == 0
        else:
            balances = await provider.get_balance(address, confirmed_only=True)
            assert len(balances) == 1
            balance = balances[0]
            assert balance.asset == provider.asset == AssetLTC
            assert float(balance.amount) > expected_balance


@pytest.mark.asyncio
async def test_get_tx_data_ltc(litecoin_providers):
    for provider in litecoin_providers:
        # non-existent
        with pytest.raises(Exception):
            await provider.get_transaction_data('123456789098765432123456789098765432123456789876543')

        # normal
        tx = await provider.get_transaction_data('a42d1959613152c786134305ffca5c42c0008aa23aa4fd1405ad96bdf9cb95f4')
        assert isinstance(tx, XcTx)
        assert tx.asset == AssetLTC
        assert tx.height == 2568095
        assert len(tx.from_txs) == 4
        assert len(tx.to_txs) == 2
        assert tx.from_txs[3].amount == amt(0.30042918)
        assert tx.from_txs[3].asset == AssetLTC
        assert tx.from_txs[3].from_address == 'ltc1qq7l2aplmmzqlkacekuauqr6unwfytutuzgkgwq'

        assert tx.to_txs[0].address == 'ltc1qp4zm5e0a2s36cw5h5gfr64lzverrxvzn0ef9kg'
        assert tx.to_txs[0].amount == amt(0.06260656)
        assert tx.to_txs[0].asset == AssetLTC

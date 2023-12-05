from cosmpy.aerial.client import Coin

from xchainpy2_client import TxType
from xchainpy2_cosmos import load_logs
from xchainpy2_thorchain import convert_coin_to_crypto_amount, get_thor_address_prefix, get_asset_from_denom, \
    crypto_amount_to_msg_coin
from xchainpy2_utils import CryptoAmount, Amount, AssetRUNE, RUNE_DECIMAL, Asset, NetworkType, AssetBNB
from xchainpy2_utils.testing_utils import load_example_json


def test_convert_coin_to_crypto_amount():
    convert = convert_coin_to_crypto_amount
    assert convert(Coin(100000000, 'rune')) == CryptoAmount(Amount.from_asset(1, RUNE_DECIMAL).as_base, AssetRUNE)
    assert convert(Coin(10, 'uatom')) == CryptoAmount(Amount.from_base(10), Asset.from_string('THOR.UATOM'))
    assert convert(Coin(333, 'uatom')) == CryptoAmount.from_base('333', Asset.from_string('THOR.UATOM'))

    a = convert(Coin(7777, 'btc/btc'))
    assert a.amount == Amount.from_base(7777)
    assert a.asset == Asset.from_string('THOR.BTC/BTC')
    assert a.asset.synth


def test_prefix():
    assert get_thor_address_prefix(NetworkType.MAINNET) == 'thor'
    assert get_thor_address_prefix(NetworkType.TESTNET) == 'tthor'
    assert get_thor_address_prefix(NetworkType.STAGENET) == 'sthor'


def test_asset_from_denom():
    assert get_asset_from_denom('rune') == AssetRUNE
    assert get_asset_from_denom('bnb.bnb') == AssetBNB


def test_crypto_amount_to_msg_coin():
    a = crypto_amount_to_msg_coin(CryptoAmount(
        Amount.from_base(100, 8),
        AssetRUNE
    ))

    assert a.decimals == 8
    assert a.amount == "100"
    assert not a.asset.synth
    assert a.asset.chain == 'THOR'
    assert a.asset.ticker == 'RUNE'
    assert a.asset.symbol == 'RUNE'

    a = crypto_amount_to_msg_coin(CryptoAmount(
        Amount.from_base(333, 6),
        Asset.from_string('BTC/BTC')
    ))
    assert a.decimals == 6
    assert a.amount == "333"
    assert a.asset.synth
    assert a.asset.chain == 'BTC'
    assert a.asset.ticker == 'BTC'
    assert a.asset.symbol == 'BTC'

    a = crypto_amount_to_msg_coin(CryptoAmount(
        Amount.from_base(987654321, 18),
        Asset.from_string('ETH.ETH-0xdac17f958d2ee523a2206206994597c13d831ec7')
    ))
    assert a.decimals == 18
    assert a.amount == "987654321"
    assert not a.asset.synth
    assert a.asset.chain == 'ETH'
    assert a.asset.ticker == 'ETH'
    assert a.asset.symbol == 'ETH-0xdac17f958d2ee523a2206206994597c13d831ec7'

#
# def test_get_deposit_tx_from_logs():
#     tx_swap = load_example_json(__file__,
#                                 'mock/samples/tx/swap-1C10434D59A460FD0BE76C46A333A583B8C7761094E26C0B2548D07A5AF28356.json')
#     logs = load_logs(tx_swap['tx_response']['logs'])
#     r = get_deposit_tx_from_logs(logs, 'thor1g3nvdxgmdte8cfhl8592lz5tuzjd9hjsglazhr')
#     assert len(r.from_txs) == len(r.to_txs) == 2
#     assert r.from_txs[0].amount == Amount.from_base(2000000, 8)
#     assert r.from_txs[0].from_address == 'thor1g3nvdxgmdte8cfhl8592lz5tuzjd9hjsglazhr'
#     assert r.from_txs[1].amount == Amount.from_base(3600000000000, 8)
#     assert r.from_txs[1].from_address == 'thor1g3nvdxgmdte8cfhl8592lz5tuzjd9hjsglazhr'
#     assert r.to_txs[0].address == 'thor1dheycdevq39qlkxs2a6wuuzyn4aqxhve4qxtxt'
#     assert r.to_txs[1].address == 'thor1g98cy3n9mmjrpn0sxmn63lztelera37n8n67c0'
#     assert r.to_txs[0].amount == Amount.from_base(2000000, 8)
#     assert r.to_txs[1].amount == Amount.from_base(3600000000000, 8)
#
#     assert r.type == TxType.TRANSFER
#
#     # --- bond ---
#     tx_bond = load_example_json(__file__,
#                                 'mock/samples/tx/bond-tn-8F241485970BE3CFCDE21A1F9C8E1EDD42DFF2F78B9B17358E2F81276F46173C.json')
#     logs = load_logs(tx_bond['tx_response']['logs'])
#     r = get_deposit_tx_from_logs(logs, 'thor1q3x003230jsuva7g5s2lpla4ln53hv25pvd7xu')
#
#     assert len(r.from_txs) == len(r.to_txs) == 1
#     assert r.from_txs[0].amount == Amount.from_base(1400000000000, 8)
#     assert r.from_txs[0].from_address == 'thor1q3x003230jsuva7g5s2lpla4ln53hv25pvd7xu'
#     assert r.to_txs[0].address == 'thor17gw75axcnr8747pkanye45pnrwk7p9c3cqncsv'
#     assert r.to_txs[0].amount == Amount.from_base(1400000000000, 8)
#     assert r.type == TxType.TRANSFER
#
#     # --- send ---
#     tx_send = load_example_json(__file__,
#                                 'mock/samples/tx/send-DBEE3FF8DC82EBB490ECE26FD761955BD6E3740BE064E8D5D27CB5F618BE6360.json')
#     logs = load_logs(tx_send['tx_response']['logs'])
#     r = get_deposit_tx_from_logs(logs, 'thor1t2pfscuq3ctgtf5h3x7p6zrjd7e0jcvuszyvt5')
#
#     assert len(r.from_txs) == len(r.to_txs) == 1
#     assert r.from_txs[0].amount == Amount.from_base(730625600000, 8)
#     assert r.from_txs[0].from_address == 'thor1t2pfscuq3ctgtf5h3x7p6zrjd7e0jcvuszyvt5'
#     assert r.to_txs[0].address == 'thor1uz4fpyd5f5d6p9pzk8lxyj4qxnwq6f9utg0e7k'
#     assert r.to_txs[0].amount == Amount.from_base(730625600000, 8)
#     assert r.type == TxType.TRANSFER
#

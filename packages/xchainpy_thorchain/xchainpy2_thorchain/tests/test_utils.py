from cosmpy.aerial.client import Coin

from xchainpy2_thorchain import convert_coin_to_crypto_amount, get_thor_address_prefix, get_asset_from_denom, \
    crypto_amount_to_msg_coin
from xchainpy2_utils import CryptoAmount, Amount, AssetRUNE, RUNE_DECIMAL, Asset, NetworkType, AssetBNB


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

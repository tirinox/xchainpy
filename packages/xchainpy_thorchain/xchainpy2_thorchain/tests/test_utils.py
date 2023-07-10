from cosmpy.aerial.client import Coin

from xchainpy2_thorchain import convert_coin_to_crypto_amount, get_thor_address_prefix
from xchainpy2_utils import CryptoAmount, Amount, AssetRUNE, RUNE_DECIMAL, Asset, NetworkType


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


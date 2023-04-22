from xchainpy2_utils import *

def test_asset_rune():
    assert AssetRune.chain == Chain.THORChain.value
    assert AssetRune.symbol == 'RUNE'


def test_asset_equals():
    asset = Asset('BNB', 'BNB', 'BNB')
    asset2 = Asset('BNB', 'BNB', 'BNB')
    assert asset == asset2

    assert AssetBNB == asset
    assert AssetBNB != AssetETH
    assert AssetRune == AssetRune


def test_asset_from_string():
    asset = Asset.from_string('BNB.BNB')
    assert asset.chain == 'BNB'
    assert asset.symbol == 'BNB'
    assert asset.contract == ''
    assert not asset.synth
    assert str(asset) == 'BNB.BNB'

    asset = Asset.from_string('BNB.BNB-1A2')
    assert asset.chain == 'BNB'
    assert asset.symbol == 'BNB'
    assert asset.contract == '1A2'
    assert not asset.synth
    assert str(asset) == 'BNB.BNB-1A2'

    asset = Asset.from_string('ETH.USDT-0xdac17f958d2ee523a2206206994597c13d831ec7')
    assert asset.chain == 'ETH'
    assert asset.symbol == 'USDT'
    assert asset.contract == '0xdac17f958d2ee523a2206206994597c13d831ec7'
    assert not asset.synth
    assert str(asset) == 'ETH.USDT-0xdac17f958d2ee523a2206206994597c13d831ec7'

    asset = Asset.from_string('BTC/BTC')
    assert asset.chain == 'BTC'
    assert asset.symbol == 'BTC'
    assert asset.contract == ''
    assert asset.synth
    assert str(asset) == 'BTC/BTC'


def test_convert_synth():
    asset = Asset.from_string('BTC.BTC')
    assert str(asset.as_synth) == 'BTC/BTC'
    assert asset.as_synth.synth

    asset = Asset.from_string('BTC/BTC')
    assert str(asset.as_native) == 'BTC.BTC'
    assert asset.as_synth == asset
    assert asset.as_synth.as_native == Asset('BTC', 'BTC')

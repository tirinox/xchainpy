import pytest

from xchainpy2_utils import *


def test_asset_rune():
    assert AssetRUNE.chain == Chain.THORChain.value
    assert AssetRUNE.symbol == 'RUNE'


def test_asset_equals():
    asset = Asset('BNB', 'BNB')
    asset2 = Asset('BNB', 'BNB')
    assert asset == asset2

    assert AssetBNB == asset
    assert AssetBNB != AssetETH
    assert AssetRUNE == AssetRUNE


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

    asset = Asset.from_string('AVAX')
    assert asset.chain == 'AVAX'
    assert asset.symbol == 'AVAX'
    assert not asset.synth

    with pytest.raises(ValueError):
        Asset.from_string_exc('')

    with pytest.raises(ValueError):
        Asset.from_string_exc('x.y.z.w')


def test_convert_synth():
    asset = Asset.from_string('BTC.BTC')
    assert str(asset.as_synth) == 'BTC/BTC'
    assert asset.as_synth.synth

    asset = Asset.from_string('BTC/BTC')
    assert str(asset.as_native) == 'BTC.BTC'
    assert asset.as_synth == asset
    assert asset.as_synth.as_native == Asset('BTC', 'BTC')


def test_well_known_assets():
    assert AssetRUNE != AssetBTC != AssetETH

    assert AssetRUNE.chain == 'THOR' and AssetRUNE.symbol == 'RUNE' and AssetRUNE.contract == '' and not AssetRUNE.synth
    assert AssetCACAO.chain == 'MAYA' and AssetCACAO.symbol == 'CACAO' and AssetCACAO.contract == '' \
           and not AssetCACAO.synth
    assert AssetBTC.chain == 'BTC' == AssetBTC.symbol and AssetBTC.contract == '' and not AssetBTC.synth
    assert AssetETH.chain == 'ETH' == AssetETH.symbol and AssetETH.contract == '' and not AssetETH.synth
    assert AssetBNB.chain == 'BNB' == AssetBNB.symbol and AssetBNB.contract == '' and not AssetBNB.synth

    for asset in (AssetBNB, AssetRUNE, AssetBTC, AssetATOM, AssetAVAX, AssetBCH, AssetCACAO, AssetDOGE, AssetLTC):
        assert asset.is_valid

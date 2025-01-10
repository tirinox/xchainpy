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


def test_equality():
    camel = 'etH.UsDt-0XDAC17F958D2EE523a2206206994597C13D831Ec7'
    a = Asset.from_string(camel)
    b = Asset.from_string(camel.upper())
    c = Asset.from_string(camel.lower())
    assert a == b == c

    c = c.synth
    assert a != c
    b = b.synth
    assert c == b

    fox = 'etH.UsDt-0XDAC17F958D2EE523a2206206994597C13D831Ec8'  # 8 != 7
    d = Asset.from_string(fox)
    assert a != d


@pytest.mark.parametrize('source, expected', [
    ('r', AssetRUNE),
    ('b', AssetBTC),
    ('e', AssetETH),
    ('n', AssetBNB),
    ('g', AssetATOM),
    ('d', AssetDOGE),
    ('l', AssetLTC),
    ('c', AssetBCH),
    ('a', AssetAVAX),
    ('s', AssetBSC),
    ('f', AssetBaseETH),
    ('BTC.BTC', AssetBTC),
    ('THOR.RUNE', AssetRUNE),
    ('ETH/ETH', AssetETH.as_synth),
    (AssetBTC, AssetBTC),
    (AssetRUNE, AssetRUNE),
    (AssetETH, AssetETH),
    (AssetBNB, AssetBNB),
    (AssetBCH, AssetBCH),
    (AssetLTC, AssetLTC),
    (AssetBaseETH, AssetBaseETH),
])
def test_automatic_creating(source, expected):
    assert Asset.automatic(source) == expected


def test_trade_asset():
    a = Asset.automatic('BTC~BTC')
    assert a.kind == AssetKind.TRADE
    assert a.is_trade
    assert not a.is_normal and not a.is_synth
    assert a.symbol == 'BTC'
    assert a.chain == 'BTC'
    assert a.delimiter == TRADE_DELIMITER

    assert str(a) == 'BTC~BTC'

    assert a.as_native == AssetBTC
    assert a.as_trade == a
    assert a.as_synth == AssetBTC.as_synth

    a = Asset.automatic('ETH~USDT-0xdac17f958d2ee523a2206206994597c13d831ec7')
    assert a == Asset('ETH', 'USDT', '0xdac17f958d2ee523a2206206994597c13d831ec7', AssetKind.TRADE)
    assert a.as_trade and a.is_valid

    a = AssetBTC
    assert not a.is_trade
    b = a.as_trade
    assert b.is_trade
    assert str(b) == 'BTC~BTC'


def test_derived_asset():
    a = Asset.automatic('THOR.BTC')
    assert a.chain == Chain.THORChain.value
    assert a.symbol == 'BTC'
    assert a.kind == AssetKind.DERIVED and a.is_derived

    a = AssetAVAX.as_derived
    assert a.chain == Chain.THORChain.value
    assert a.symbol == 'AVAX'
    assert a.kind == AssetKind.DERIVED and a.is_derived
    assert str(a) == 'THOR.AVAX'


@pytest.mark.parametrize('source, expected', [
    ('BTC', 'b'),
    (AssetBTC, 'b'),
    (AssetLTC, 'l'),
    ('BASE.ETH', 'f'),
    (AssetBaseETH, 'f'),
])
def test_get_short_code(source, expected):
    assert get_short_code(source) == expected

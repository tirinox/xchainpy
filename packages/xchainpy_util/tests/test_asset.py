from asset import Asset
from consts import AssetBNB, AssetETH, AssetRune, Chain


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

import pytest

from xchainpy2_utils import *


def test_asset_rune():
    assert AssetRUNE.chain == Chain.THORChain.value
    assert AssetRUNE.symbol == 'RUNE'


def test_asset_equals():
    asset = Asset('BSC', 'BNB')
    asset2 = Asset('BSC', 'BNB')
    assert asset == asset2

    assert AssetBSC == asset
    assert AssetBSC != AssetETH
    assert AssetRUNE == AssetRUNE


@pytest.mark.parametrize(
    'input_string, expected_chain, expected_symbol, expected_contract, expected_synth, expected_str', [
        ('BSC.BNB', 'BSC', 'BNB', '', False, 'BSC.BNB'),
        ('ETH.USDT-0xdac17f958d2ee523a2206206994597c13d831ec7', 'ETH', 'USDT',
         '0xdac17f958d2ee523a2206206994597c13d831ec7', False, 'ETH.USDT-0xdac17f958d2ee523a2206206994597c13d831ec7'),
        ('BTC/BTC', 'BTC', 'BTC', '', True, 'BTC/BTC'),
        ('AVAX', 'AVAX', 'AVAX', '', False, None),
        ('XRP-OMG', 'XRP', 'OMG', '', False, 'XRP-OMG'),
        ('ETH-USDT-0xdac17f958d2ee523a2206206994597c13d831ec7', 'ETH', 'USDT',
         '0xdac17f958d2ee523a2206206994597c13d831ec7', False, 'ETH-USDT-0xdac17f958d2ee523a2206206994597c13d831ec7'),
        ('XRP~OMG', 'XRP', 'OMG', '', False, 'XRP~OMG'),
    ])
def test_asset_from_string(input_string, expected_chain, expected_symbol, expected_contract, expected_synth,
                           expected_str):
    asset = Asset.from_string(input_string)
    assert asset.chain == expected_chain
    assert asset.symbol == expected_symbol
    assert asset.contract == expected_contract
    assert asset.synth == expected_synth
    if expected_str is not None:
        assert str(asset) == expected_str


@pytest.mark.parametrize('invalid_input', [
    '',  # Empty string
    'x.y.z.w',  # Uncomment if needed for additional invalid cases
    ".",
    "~",
    "-",
    "BTC.",
    ".ETH",
])
def test_asset_from_string_invalid_cases(invalid_input):
    with pytest.raises(ValueError):
        Asset.from_string(invalid_input)


def test_convert_synth():
    asset = Asset.from_string('BTC.BTC')
    assert str(asset.as_synth) == 'BTC/BTC'
    assert asset.as_synth.synth

    asset = Asset.from_string('BTC/BTC')
    assert str(asset.as_native) == 'BTC.BTC'
    assert asset.as_synth == asset
    assert asset.as_synth.as_native == Asset('BTC', 'BTC')

    assert asset.as_secured.is_secured


def test_well_known_assets():
    assert AssetRUNE != AssetBTC != AssetETH

    assert AssetRUNE.chain == 'THOR' and AssetRUNE.symbol == 'RUNE' and AssetRUNE.contract == '' and not AssetRUNE.synth
    assert AssetCACAO.chain == 'MAYA' and AssetCACAO.symbol == 'CACAO' and AssetCACAO.contract == '' \
           and not AssetCACAO.synth
    assert AssetBTC.chain == 'BTC' == AssetBTC.symbol and AssetBTC.contract == '' and not AssetBTC.synth
    assert AssetETH.chain == 'ETH' == AssetETH.symbol and AssetETH.contract == '' and not AssetETH.synth
    assert AssetBSC.chain == 'BSC' and AssetBSC.contract == '' and not AssetBSC.synth
    assert AssetBSC.symbol == 'BNB'

    for asset in (
            AssetRUNE, AssetBTC, AssetATOM, AssetAVAX, AssetBCH, AssetCACAO, AssetDOGE, AssetLTC, AssetBSC,
            AssetXRP, AssetDASH, AssetAEth, AssetTCY, AssetSOL
    ):
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

    assert Asset.from_string(camel.lower()) == Asset.from_string(camel.upper())
    assert AssetETH == Asset("ETH", "eth", "", kind=AssetKind.NATIVE)

    assert AssetRUNE == AssetRUNE
    assert AssetRUNE != AssetBTC
    assert AssetBTC != AssetRUNE


@pytest.mark.parametrize('source, expected', [
    ('r', AssetRUNE),
    ('b', AssetBTC),
    ('e', AssetETH),
    ('g', AssetATOM),
    ('ad', AssetADA),
    ('d', AssetDOGE),
    ('do', AssetDOT),
    ('l', AssetLTC),
    ('m', AssetXMR),
    ('o', AssetSOL),
    ('p', AssetPOL),
    ('c', AssetBCH),
    ('a', AssetAVAX),
    ('s', AssetBSC),
    ('ta', AssetTAO),
    ('tr', AssetTRX),
    ('u', AssetSUI),
    ('f', AssetBaseETH),
    ('x', AssetXRP),
    ('z', AssetZEC),
    ('BTC.BTC', AssetBTC),
    ('THOR.RUNE', AssetRUNE),
    ('ETH/ETH', AssetETH.as_synth),
    (AssetBTC, AssetBTC),
    (AssetRUNE, AssetRUNE),
    (AssetETH, AssetETH),
    (AssetBCH, AssetBCH),
    (AssetLTC, AssetLTC),
    (AssetADA, AssetADA),
    (AssetDOT, AssetDOT),
    (AssetBaseETH, AssetBaseETH),
    (AssetXMR, AssetXMR),
    (AssetSOL, AssetSOL),
    (AssetPOL, AssetPOL),
    (AssetTAO, AssetTAO),
    (AssetTRX, AssetTRX),
    (AssetSUI, AssetSUI),
    (AssetZEC, AssetZEC),
])
def test_auto_creating(source, expected):
    assert Asset.auto(source) == expected


def test_trade_asset():
    a = Asset.auto('BTC~BTC')
    assert a.kind == AssetKind.TRADE
    assert a.is_trade
    assert not a.is_native and not a.is_synth
    assert a.symbol == 'BTC'
    assert a.chain == 'BTC'
    assert a.delimiter == TRADE_DELIMITER

    assert str(a) == 'BTC~BTC'

    assert a.as_native == AssetBTC
    assert a.as_trade == a
    assert a.as_synth == AssetBTC.as_synth

    a = Asset.auto('ETH~USDT-0xdac17f958d2ee523a2206206994597c13d831ec7')
    assert a == Asset('ETH', 'USDT', '0xdac17f958d2ee523a2206206994597c13d831ec7', AssetKind.TRADE)
    assert a.as_trade and a.is_valid

    a = AssetBTC
    assert not a.is_trade
    b = a.as_trade
    assert b.is_trade
    assert str(b) == 'BTC~BTC'


def test_derived_asset():
    a = Asset.auto('THOR.BTC')
    assert a.chain == Chain.THORChain.value
    assert a.symbol == 'BTC'
    assert a.kind == AssetKind.NATIVE
    assert a.as_derived.is_derived

    a = AssetAVAX.as_derived
    assert a.chain == Chain.THORChain.value
    assert a.symbol == 'AVAX'
    assert a.kind == AssetKind.DERIVED and a.is_derived
    assert str(a) == 'THOR.AVAX'


@pytest.mark.parametrize('source, expected', [
    ('BTC', 'b'),
    (AssetBSC, 's'),
    (AssetBTC, 'b'),
    (AssetLTC, 'l'),
    ('ADA.ADA', 'ad'),
    (AssetADA, 'ad'),
    ('DOT.DOT', 'do'),
    (AssetDOT, 'do'),
    ('BASE.ETH', 'f'),
    (AssetBaseETH, 'f'),
    ('XMR.XMR', 'm'),
    (AssetXMR, 'm'),
    ('SOL.SOL', 'o'),
    (AssetSOL, 'o'),
    ('POL.POL', 'p'),
    (AssetPOL, 'p'),
    ('TAO.TAO', 'ta'),
    (AssetTAO, 'ta'),
    ('TRON.TRX', 'tr'),
    (AssetTRX, 'tr'),
    ('SUI.SUI', 'u'),
    (AssetSUI, 'u'),
    (AssetXRP, 'x'),
    ('ZEC.ZEC', 'z'),
    (AssetZEC, 'z'),
])
def test_get_short_code(source, expected):
    assert get_short_code(source) == expected
    assert Asset.auto(expected) == Asset.auto(source)


def test_dimensionless():
    a = Asset.dimensionless()
    assert a.is_dimensionless
    assert not a.symbol
    assert a.chain == Chain.THORChain.value

    b = AssetRUNE
    assert not b.is_dimensionless


@pytest.mark.parametrize('source_asset, expected', [
    ("", AssetKind.UNKNOWN),
    ("foobar", AssetKind.UNKNOWN),
    ("THOR?BTC", AssetKind.UNKNOWN),
    ("BTC.BTC", AssetKind.NATIVE),
    ("ETH.USDT-0xdac17f958d2ee523a2206206994597c13d831ec7", AssetKind.NATIVE),
    ("BTC~BTC", AssetKind.TRADE),
    ("BTC-BTC", AssetKind.SECURED),
    ("ETH/ETH", AssetKind.SYNTH),
    # weird but true:
    (".", AssetKind.NATIVE),
    ("~", AssetKind.TRADE),
    ("-", AssetKind.SECURED),
])
def test_asset_kind_recognize(source_asset, expected):
    assert AssetKind.recognize(source_asset) == expected


Asset_USDC_ARB = Asset.from_string("ARB.USDC-0XAF88D065E77C8CC2239327C5EDB3A432268E5831").upper()


# test for Asset repr
@pytest.mark.parametrize('asset, expected_repr', [
    (AssetRUNE, "Asset(chain='THOR', symbol='RUNE', contract='', kind='native')"),
    (AssetBTC, "Asset(chain='BTC', symbol='BTC', contract='', kind='native')"),
    (AssetBTC.as_trade, "Asset(chain='BTC', symbol='BTC', contract='', kind='trade')"),
    (AssetETH, "Asset(chain='ETH', symbol='ETH', contract='', kind='native')"),
    (AssetETH.as_secured, "Asset(chain='ETH', symbol='ETH', contract='', kind='secured')"),
    (AssetBSC, "Asset(chain='BSC', symbol='BNB', contract='', kind='native')"),
    (Asset_USDC_ARB,
     "Asset(chain='ARB', symbol='USDC', contract='0XAF88D065E77C8CC2239327C5EDB3A432268E5831', kind='native')"),
    (Asset_USDC_ARB.as_synth,
     "Asset(chain='ARB', symbol='USDC', contract='0XAF88D065E77C8CC2239327C5EDB3A432268E5831', kind='synth')"),
])
def test_asset_repr(asset, expected_repr):
    assert repr(asset) == expected_repr

from decimal import Decimal

import pytest

from xchainpy2_utils import CryptoAmount, Amount, Asset, AssetRUNE, AssetCACAO, AssetBTC, AssetETH


def test_zero():
    assert CryptoAmount.zero(AssetRUNE) == CryptoAmount(Amount.zero(8), AssetRUNE)
    assert CryptoAmount.zero(AssetCACAO) == CryptoAmount(Amount.zero(10), AssetCACAO)
    assert CryptoAmount.zero("SOME.ASSET", 4) == CryptoAmount(Amount.zero(4), Asset.from_string("SOME.ASSET"))


def test_pick():
    balances = [
        CryptoAmount(Amount(500, 8), Asset.from_string(AssetBTC)),
        CryptoAmount(Amount(42, 8), AssetRUNE),
    ]
    assert CryptoAmount.pick(balances, AssetRUNE) == CryptoAmount(Amount(42, 8), AssetRUNE)
    assert CryptoAmount.pick(balances, AssetBTC) == CryptoAmount(Amount(500, 8), Asset.from_string(AssetBTC))
    assert CryptoAmount.pick(balances, AssetCACAO) == CryptoAmount.zero(AssetCACAO)


def test_fee_subtract():
    amt = CryptoAmount(Amount(100, 8), AssetRUNE)
    fee = CryptoAmount(Amount(1, 8), AssetRUNE)
    assert amt - fee == CryptoAmount(Amount(99, 8), AssetRUNE)


def test_auto():
    assert CryptoAmount.auto_base(555111, 'THOR.RUNE') == CryptoAmount(Amount(555111, 8), AssetRUNE)
    assert CryptoAmount.auto_base(0.1, 'THOR.RUNE') == CryptoAmount.zero(AssetRUNE)
    assert CryptoAmount.auto_base("123.4", 'THOR.RUNE') == CryptoAmount(Amount(123, 8), AssetRUNE)

    assert CryptoAmount.auto(1, 'THOR.RUNE') == CryptoAmount(Amount(100000000, 8), AssetRUNE)
    assert CryptoAmount.auto(134, 'THOR.RUNE') == CryptoAmount(Amount(13400000000, 8), AssetRUNE)
    assert CryptoAmount.auto(1.0, 'THOR.RUNE') == CryptoAmount(Amount.auto(1.0, 8), AssetRUNE)

    assert (
            CryptoAmount.auto(
                333.5, 'ETH.USDT-0XDAC17F958D2EE523A2206206994597C13D831EC7')
            == CryptoAmount(
        Amount.auto(333.5, 6),
        Asset.from_string('ETH.USDT-0XDAC17F958D2EE523A2206206994597C13D831EC7'))
    )

    assert (CryptoAmount.auto(40.0, AssetCACAO) == CryptoAmount(Amount.automatic(40.0, 10), AssetCACAO))


@pytest.mark.parametrize(
    'amount, asset, decimals, expected',
    [
        (1, 'THOR.RUNE', 8, CryptoAmount(Amount(100000000, 8), AssetRUNE)),
        (134, 'THOR.RUNE', 8, CryptoAmount(Amount(13400000000, 8), AssetRUNE)),
        (1.0, 'THOR.RUNE', 8, CryptoAmount(Amount.automatic(1.0, 8), AssetRUNE)),
        (555111, 'THOR.RUNE', 8, CryptoAmount(Amount(55511100000000, 8), AssetRUNE)),
        (333.5, 'ETH.USDT-0XDAC17F958D2EE523A2206206994597C13D831EC7', 6,
         CryptoAmount(Amount.automatic(333.5, 6),
                      Asset.from_string('ETH.USDT-0XDAC17F958D2EE523A2206206994597C13D831EC7'))),
        (40.0, AssetCACAO, 10, CryptoAmount(Amount.automatic(40.0, 10), AssetCACAO)),
        (Decimal("1.23456789"), 'BTC.BTC', 8, CryptoAmount(Amount(123456789, 8), AssetBTC)),
    ]
)
def test_auto_2(amount, asset, decimals, expected):
    a = CryptoAmount.automatic(amount, asset, decimals)
    assert a.amount.internal_amount == expected.base_amount == expected.amount.internal_amount
    assert a == expected
    assert a.decimals == expected.decimals
    assert a.asset == expected.asset


@pytest.mark.parametrize(
    'amount, asset, expected',
    [
        (1, 'THOR.RUNE', CryptoAmount(Amount(100000000, 8), AssetRUNE)),
        (Decimal("1.622"), 'ETH.ETH', CryptoAmount(Amount(1622000000000000000, 18), AssetETH)),
        (Decimal("1.622"), "ETH.USDC-0XA0B86991C6218B36C1D19D4A2E9EB0CE3606EB48",
         CryptoAmount(Amount(1622000, 6), Asset.from_string("ETH.USDC-0XA0B86991C6218B36C1D19D4A2E9EB0CE3606EB48"))),
    ]
)
def test_auto_guess_decimals(amount, asset, expected):
    a = CryptoAmount.automatic(amount, asset)
    assert a.amount.internal_amount == expected.base_amount == expected.amount.internal_amount
    assert a == expected
    assert a.decimals == expected.decimals
    assert a.asset == expected.asset


def test_multiply():
    amt = CryptoAmount(Amount(100, 8), AssetRUNE)
    assert amt * 2 == CryptoAmount(Amount(200, 8), AssetRUNE)
    assert amt * 0.5 == CryptoAmount(Amount(50, 8), AssetRUNE)
    assert amt * 0 == CryptoAmount.zero(AssetRUNE)

    assert amt * 3.2 == CryptoAmount(Amount(320, 8), AssetRUNE)
    assert amt * Decimal(0.5) == CryptoAmount(Amount(50, 8), AssetRUNE)


@pytest.mark.parametrize('right', [
    "foo",
    Amount(2, 8),
    AssetRUNE,
    CryptoAmount(Amount(2, 8), AssetRUNE),
])
def test_bad_multiply(right):
    amt = CryptoAmount(Amount(9999, 8), AssetRUNE)
    with pytest.raises(TypeError):
        amt * right


def test_change_amount():
    amt = CryptoAmount(Amount(100, 8), AssetRUNE)
    assert amt.changed_amount(200) == CryptoAmount(Amount(200, 8), AssetRUNE)
    assert amt.changed_amount(0) == CryptoAmount(Amount(0, 8), AssetRUNE)


# todo: repr


def test_change_decimals():
    amt = CryptoAmount(Amount.automatic(2.22, 18), Asset.from_string('ETH~ETH'))
    assert amt.decimals == amt.amount.decimals == 18
    amt2 = amt.converted_decimals(8)
    assert amt2.decimals == amt2.amount.decimals == 8

    assert amt2.amount.internal_amount == 222000000
    assert amt.amount.internal_amount == 2220000000000000195

    assert float(amt2.amount) == float(amt.amount)


def test_arithmetic():
    amt = CryptoAmount(Amount(100, 8), AssetRUNE)
    assert amt + amt == CryptoAmount(Amount(200, 8), AssetRUNE)
    assert amt - amt == CryptoAmount.zero(AssetRUNE)

    assert amt * 3 == CryptoAmount(Amount(300, 8), AssetRUNE)
    assert amt / 2 == CryptoAmount(Amount(50, 8), AssetRUNE)

    with pytest.raises(ValueError):
        bmt = CryptoAmount(Amount(100, 8), Asset.from_string(AssetBTC))
        amt + bmt

    assert amt / amt == CryptoAmount.automatic(1, Asset.dimensionless())
    assert amt // amt == CryptoAmount.automatic(1, Asset.dimensionless())
    assert amt * 5 / amt == CryptoAmount.automatic(5, Asset.dimensionless())
    # 7 // 2 == 3
    assert amt * 7 // (amt * 2) == CryptoAmount.automatic(3, Asset.dimensionless())

    amt = CryptoAmount.automatic(5, AssetRUNE)
    assert amt + 6 == CryptoAmount.automatic(11, AssetRUNE)
    assert amt - 1 == CryptoAmount.automatic(4, AssetRUNE)
    assert amt + 6.0 == CryptoAmount.automatic(11, AssetRUNE)
    assert amt - 1.0 == CryptoAmount.automatic(4, AssetRUNE)
    assert amt + "6.0" == CryptoAmount.automatic(11, AssetRUNE)
    assert amt - "1.0" == CryptoAmount.automatic(4, AssetRUNE)
    assert amt + Decimal("6.0") == CryptoAmount.automatic(11, AssetRUNE)
    assert amt - Decimal("1.0") == CryptoAmount.automatic(4, AssetRUNE)



def test_conv():
    amt = CryptoAmount(Amount(100, 8), AssetRUNE)
    assert int(amt) == 100

    amt = amt.changed_amount(0)
    assert int(amt) == 0

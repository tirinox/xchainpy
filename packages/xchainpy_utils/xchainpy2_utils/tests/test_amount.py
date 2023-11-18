import pytest

from xchainpy2_utils import *


def test_amount_general():
    assert DEFAULT_ASSET_DECIMAL == 8


def test_amount_create():
    a = Amount(1)
    assert a.internal_amount == 1
    assert a.decimals == 8
    assert a.denom == Denomination.ASSET
    assert a.format() == '0.00000001'

    a = Amount(745, 4)
    assert a.internal_amount == 745
    assert a.decimals == 4
    assert a.denom == Denomination.ASSET
    assert a.format() == '0.0745'


def test_amount_auto():
    a = Amount.automatic(8050)
    assert a.internal_amount == 8050
    assert a.decimals == 8
    assert a.denom == Denomination.BASE
    assert int(a) == 8050

    a = Amount.automatic(8050.0, 6)
    assert a.internal_amount == 8050000000
    assert a.decimals == 6
    assert a.denom == Denomination.ASSET
    assert int(a) == 8050000000

    a = Amount.automatic('8050')
    assert a.internal_amount == 805000000000
    assert a.decimals == 8
    assert a.denom == Denomination.ASSET
    assert int(a) == 805000000000

    a = Amount.automatic('1234', 6)
    assert a.internal_amount == 1234000000
    assert a.decimals == 6
    assert a.denom == Denomination.ASSET
    assert int(a) == 1234000000

    a = amount(1234)
    assert a.internal_amount == 1234
    assert a.decimals == 8
    assert a.denom == Denomination.BASE
    assert int(a) == 1234

    a = amount('100500.56')
    assert a.internal_amount == 10050056000000
    assert a.decimals == 8
    assert a.denom == Denomination.ASSET
    assert int(a) == 10050056000000


def test_amount_base():
    b = Amount.from_base(8050)
    a = Amount.to_asset(b)
    assert a.internal_amount == 8050
    assert a.decimals == 8
    assert a.denom == Denomination.ASSET
    assert int(a) == 8050
    assert a.amount == 0.0000805

    c = Amount.to_base(a)
    assert c.internal_amount == 8050
    assert c.decimals == 8
    assert c.denom == Denomination.BASE
    assert int(c) == 8050
    assert c.amount == 8050


def test_amount_sum():
    a1 = Amount(9999, 18)
    a2 = Amount(1, 6)
    a3 = a1 + a2
    assert a3.internal_amount == 10000
    assert a3.decimals == 18
    assert a3.format() == '0.00000000000001'

    a4 = Amount.automatic('6789.0', 18) + a1
    assert a4.internal_amount == 6789000000000000009999
    assert a4.decimals == 18
    assert a4.format() == '6789.000000000000009999'


def test_compare():
    assert Amount(1) == Amount(1)
    assert Amount(1) != Amount(2)
    assert Amount(1) < Amount(2)
    assert Amount(10) <= Amount(10)
    assert Amount(20) >= Amount(20)
    assert Amount(200) > Amount(100)
    assert int(Amount(11111, 6)) == int(Amount(11111, 10))
    assert Amount(11111, 6) != Amount(11111, 8)

    assert Amount(40, 4, Denomination.ASSET) > 39

    assert Amount.from_asset(40) > 39.0
    assert Amount.from_asset(40) >= 40.0
    assert Amount.from_asset(40) >= 38.0
    assert Amount.from_asset(40) < 40.1
    assert Amount.from_asset(40) <= 40.0
    assert Amount.from_asset(40) <= 40.1

    # ints are treated as base amounts
    assert Amount.from_asset(40) < 50 * 10**8
    assert Amount.from_asset(40) > 30 * 10**8


def test_change_decimals():
    a = Amount(123456789, 8, Denomination.BASE)
    d6 = a.changed_decimals(6)
    assert d6.internal_amount == 1234567
    d10 = a.changed_decimals(10)
    assert d10.internal_amount == 12345678900

    d8 = a.changed_decimals(8)
    assert d8.internal_amount == 123456789


def test_multiply():
    a = Amount(100, 8, Denomination.BASE)
    b = a * 2
    assert b.internal_amount == 200

    c = a * 2.5
    assert c.internal_amount == 250

    d = a * Decimal(0.5)
    assert d.internal_amount == 50

    e = a * Decimal(3.0)
    assert e.internal_amount == 300

    assert a * 0 == 0

    assert Amount(100500, 6, Denomination.ASSET) * 2 == Amount(201000, 6, Denomination.ASSET)


def test_divide():
    a = Amount(100, 8, Denomination.BASE)
    b = a / 2
    assert b.internal_amount == 50

    c = a / 2.5
    assert c.internal_amount == 40

    d = a / Decimal(0.5)
    assert d.internal_amount == 200

    e = a / Decimal(3.0)
    assert e.internal_amount == 33

    with pytest.raises(ZeroDivisionError):
        assert a / 0 == 0

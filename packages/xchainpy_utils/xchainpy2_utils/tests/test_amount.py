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


def test_amount_base():
    b = Amount.from_base(8050)
    a = b.as_asset
    assert a.internal_amount == 8050
    assert a.decimals == 8
    assert a.denom == Denomination.ASSET
    assert int(a) == 8050
    assert a.amount == 0.0000805

    c = a.as_base
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
    assert Amount.from_asset(40) < 50 * 10 ** 8
    assert Amount.from_asset(40) > 30 * 10 ** 8


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


def test_bool():
    assert Amount(400)
    assert Amount(-5)
    assert not Amount(0)
    assert not Amount.from_base(0, 4)
    assert not Amount.automatic(0)

    assert Amount(0).is_zero
    assert not Amount.automatic(25.3).is_zero


def test_same_denom():
    b1 = Amount(100, 6, Denomination.BASE)
    a1 = Amount(100, 6, Denomination.ASSET)
    assert a1 != b1  # different denominations
    assert b1.as_asset == a1
    assert a1.as_base == b1

    assert a1.same_denom(b1) == b1
    assert b1.same_denom(a1) == a1

    a2 = Amount(444, 6, Denomination.ASSET)
    b2 = Amount(333, 6, Denomination.BASE)
    assert a1.same_denom(b2) == a1.as_base
    assert b1.same_denom(a2) == b1.as_asset

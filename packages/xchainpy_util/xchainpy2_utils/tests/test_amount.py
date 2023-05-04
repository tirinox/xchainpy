from xchainpy2_utils import *


def test_amount_general():
    assert ASSET_DECIMAL == 8


def test_amount_create():
    a = Amount(1)
    assert a.internal_amount == 1
    assert a.decimal == 8
    assert a.denom == Denomination.ASSET
    assert a.format() == '0.00000001'

    a = Amount(745, 4)
    assert a.internal_amount == 745
    assert a.decimal == 4
    assert a.denom == Denomination.ASSET
    assert a.format() == '0.0745'


def test_amount_auto():
    a = Amount.automatic(8050)
    assert a.internal_amount == 8050
    assert a.decimal == 8
    assert a.denom == Denomination.BASE
    assert int(a) == 8050

    a = Amount.automatic(8050.0, 6)
    assert a.internal_amount == 8050000000
    assert a.decimal == 6
    assert a.denom == Denomination.ASSET
    assert int(a) == 8050000000

    a = Amount.automatic('8050')
    assert a.internal_amount == 805000000000
    assert a.decimal == 8
    assert a.denom == Denomination.ASSET
    assert int(a) == 805000000000

    a = Amount.automatic('1234', 6)
    assert a.internal_amount == 1234000000
    assert a.decimal == 6
    assert a.denom == Denomination.ASSET
    assert int(a) == 1234000000

    a = amount(1234)
    assert a.internal_amount == 1234
    assert a.decimal == 8
    assert a.denom == Denomination.BASE
    assert int(a) == 1234

    a = amount('100500.56')
    assert a.internal_amount == 10050056000000
    assert a.decimal == 8
    assert a.denom == Denomination.ASSET
    assert int(a) == 10050056000000


def test_amount_base():
    b = Amount.from_base(8050)
    a = Amount.to_asset(b)
    assert a.internal_amount == 8050
    assert a.decimal == 8
    assert a.denom == Denomination.ASSET
    assert int(a) == 8050
    assert a.amount == 0.0000805

    c = Amount.to_base(a)
    assert c.internal_amount == 8050
    assert c.decimal == 8
    assert c.denom == Denomination.BASE
    assert int(c) == 8050
    assert c.amount == 8050


def test_amount_sum():
    a1 = Amount(9999, 18)
    a2 = Amount(1, 6)
    a3 = a1 + a2
    assert a3.internal_amount == 10000
    assert a3.decimal == 18
    assert a3.format() == '0.00000000000001'

    a4 = Amount.automatic('6789.0', 18) + a1
    assert a4.internal_amount == 6789000000000000009999
    assert a4.decimal == 18
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


def test_change_decimals():
    a = Amount(123456789, 8, Denomination.BASE)
    d6 = a.changed_decimals(6)
    assert d6.internal_amount == 1234567
    d10 = a.changed_decimals(10)
    assert d10.internal_amount == 12345678900

    d8 = a.changed_decimals(8)
    assert d8.internal_amount == 123456789

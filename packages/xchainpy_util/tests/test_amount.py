from amount import Amount, Denomination, amount


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
    assert a.internal_amount == 8050
    assert a.decimal == 8
    assert a.denom == Denomination.BASE
    assert int(a) == 8050

    a = Amount.automatic('1234', 6)
    assert a.internal_amount == 1234
    assert a.decimal == 6
    assert a.denom == Denomination.BASE
    assert int(a) == 1234

    a = amount(1234)
    assert a.internal_amount == 1234
    assert a.decimal == 8
    assert a.denom == Denomination.BASE
    assert int(a) == 1234

    a = amount(100500.567)
    assert a.internal_amount == 10050056700000
    assert a.decimal == 8
    assert a.denom == Denomination.ASSET
    assert int(a) == 10050056700000
    
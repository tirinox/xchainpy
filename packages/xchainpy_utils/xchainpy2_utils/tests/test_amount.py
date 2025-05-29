import pytest

from xchainpy2_utils import *


def test_amount_general():
    assert DEFAULT_ASSET_DECIMAL == 8
    assert DC.prec == 100


def test_amount_create():
    a = Amount(1)
    assert a.internal_amount == 1
    assert a.decimals == 8

    a = Amount(745, 4)
    assert a.internal_amount == 745
    assert a.decimals == 4

    assert Amount.zero().internal_amount == 0
    assert Amount.zero().decimals == 8
    assert Amount.zero(4).internal_amount == 0
    assert Amount.zero(4).decimals == 4


@pytest.mark.parametrize('in_amt, dec, repr_str, str_str', [
    (1, 8, 'Amount(1, 8)', '0.00000001 (D:8)'),
    (12345678, 8, 'Amount(12345678, 8)', '0.12345678 (D:8)'),
    (12345678, 6, 'Amount(12345678, 6)', '12.345678 (D:6)'),
    (10 ** 18, 18, 'Amount(1000000000000000000, 18)', '1.0 (D:18)'),
    (11 * 10 ** 17, 18, 'Amount(1100000000000000000, 18)', '1.1 (D:18)'),
])
def test_amount_repr(in_amt, dec, repr_str, str_str):
    a = Amount(in_amt, dec)
    assert repr(a) == repr_str
    assert str(a) == str_str


@pytest.mark.parametrize('in_amt, in_dec, e_internal, e_decimals, e_int', [
    (1, 0, 1, 0, 1),
    (321, 0, 321, 0, 321),
    (205.0, 6, 205, 6, 205),
    (Decimal('98766'), 2, 98766, 2, 98766),
])
def test_amount_automatic_base(in_amt, in_dec, e_internal, e_decimals, e_int):
    a = Amount.automatic_base(in_amt, decimals=in_dec)
    assert a.internal_amount == e_internal
    assert a.decimals == e_decimals
    assert int(a) == e_int


@pytest.mark.parametrize('in_amt, in_dec, e_internal, e_decimals, e_int', [
    (205.0, 6, 205000000, 6, 205000000),
    (123, 0, 123, 0, 123),
    (Decimal('12345.12'), 2, 1234512, 2, 1234512),
    ("7.86", 4, 78600, 4, 78600),
    ("0", 8, 0, 8, 0),
    (0.0, 8, 0, 8, 0),
    (Decimal('0.00000001'), 8, 1, 8, 1),
    (0.00005, 8, 5000, 8, 5000),
    (0.1, 0, 0, 0, 0),
    (0.1, 1, 1, 1, 1),
    ("123456789", 8, 12345678900000000, 8, 12345678900000000),
])
def test_amount_automatic_asset(in_amt, in_dec, e_internal, e_decimals, e_int):
    a = Amount.automatic(in_amt, decimals=in_dec)
    assert a.internal_amount == e_internal
    assert a.decimals == e_decimals
    assert int(a) == e_int


@pytest.mark.parametrize(
    "input_value, decimals, expected_internal, expected_float",
    [
        (8050, 8, 8050, 0.0000805),
        (15.5, 4, 15, 0.0015),  # Assuming truncation, not rounding
        ("123.456", 3, 123, 0.123),
        (Decimal("0.00000001"), 8, 0, 0),
        (Decimal("1.5"), 2, 1, 0.01),
        ("1000", 6, 1000, 0.001),
        (0.0001, 6, 0, 0),
    ]
)
def test_amount_automatic_base(input_value, decimals, expected_internal, expected_float):
    a = Amount.automatic_base(input_value, decimals)
    assert a.internal_amount == expected_internal, f"Internal amount mismatch for {input_value}"
    assert a.decimals == decimals
    assert int(a) == expected_internal
    assert float(a) == pytest.approx(expected_float, rel=1e-9)


@pytest.mark.parametrize(
    "a1, a2, expected_internal, expected_decimals, expected_format",
    [
        # Amount + Amount
        (Amount(9999, 2), Amount(1, 2), 10000, 2, '100.0'),
        (Amount(100, 8), Amount(250, 8), 350, 8, '0.0000035'),

        # Amount + int
        (Amount(100000000, 8), 2, 300000000, 8, '3.0'),
        (Amount(100000000, 8), 0, 100000000, 8, '1.0'),
        (Amount(100000000, 8), -2, -100000000, 8, '-1.0'),

        # Amount + float (converted to asset amount)
        (Amount(100000000, 8), 0, 100000000, 8, '1.0'),
        (Amount(150000000, 8), 0.25, 175000000, 8, '1.75'),
        (Amount(150000000, 8), -0.25, 125000000, 8, '1.25'),

        # Amount + Decimal
        (Amount(500, 6), Decimal("0.0002"), 700, 6, '0.0007'),
        (Amount(100000, 6), Decimal("0.0001"), 100100, 6, '0.1001'),

        # Amount + str
        (Amount(500, 6), "0.0003", 800, 6, '0.0008'),
        (Amount(500, 6), "0", 500, 6, '0.0005'),
        (Amount(500, 6), "1", 1000500, 6, '1.0005'),
        (Amount(500, 2), "3", 800, 2, '8.0'),
    ]
)
def test_amount_sum(a1, a2, expected_internal, expected_decimals, expected_format):
    result = a1 + a2
    assert result.internal_amount == expected_internal
    assert result.decimals == expected_decimals
    assert result.format() == expected_format


@pytest.mark.parametrize(
    "a1, a2, expected_internal, expected_decimals, expected_format",
    [
        # Amount - Amount
        (Amount(9999, 2), Amount(1, 2), 9998, 2, '99.98'),
        (Amount(1000, 4), Amount(250, 4), 750, 4, '0.075'),

        # Amount - int
        (Amount(300000000, 8), 2, 100000000, 8, '1.0'),
        (Amount(100000000, 8), 0, 100000000, 8, '1.0'),
        (Amount(100000000, 8), -2, 300000000, 8, '3.0'),

        # Amount - float
        (Amount(100000000, 8), 0, 100000000, 8, '1.0'),
        (Amount(150000000, 8), 0.25, 125000000, 8, '1.25'),
        (Amount(150000000, 8), -0.25, 175000000, 8, '1.75'),

        # Amount - Decimal
        (Amount(700, 6), Decimal("0.0002"), 500, 6, '0.0005'),
        (Amount(100100, 6), Decimal("0.0001"), 100000, 6, '0.1'),

        # Amount - str
        (Amount(800, 6), "0.0003", 500, 6, '0.0005'),
        (Amount(500, 6), "0", 500, 6, '0.0005'),
        (Amount(1000500, 6), "1", 500, 6, '0.0005'),
        (Amount(800, 2), "3", 500, 2, '5.0'),
    ]
)
def test_amount_sub(a1, a2, expected_internal, expected_decimals, expected_format):
    result = a1 - a2
    assert result.internal_amount == expected_internal
    assert result.decimals == expected_decimals
    assert result.format() == expected_format


def test_amount_sum_raise_decimal_mismatch():
    a1 = Amount(100, 8)
    a2 = Amount(200, 6)  # Different decimals
    with pytest.raises(ValueError):
        _ = a1 + a2

    a3 = Amount(300, 4)
    with pytest.raises(ValueError):
        _ = a1 + a3  # Different decimals


def test_amount_subtract_raise_decimal_mismatch():
    a1 = Amount(100, 8)
    a2 = Amount(200, 6)  # Different decimals
    with pytest.raises(ValueError):
        _ = a1 - a2

    a3 = Amount(300, 4)
    with pytest.raises(ValueError):
        _ = a1 - a3  # Different decimals


def test_compare():
    assert Amount(1) == Amount(1)
    assert Amount(1) != Amount(2)
    assert Amount(1) < Amount(2)
    assert Amount(10) <= Amount(10)
    assert Amount(20) >= Amount(20)
    assert Amount(200) > Amount(100)
    assert int(Amount(11111, 6)) == int(Amount(11111, 10))
    assert Amount(11111, 6) != Amount(11111, 8)

    # no automatic conversion of decimals when comparing Amount and Amount
    assert Amount(11, 2) != Amount(1100, 4)
    assert Amount(11, 3) != Amount(1100, 4)
    assert Amount(123, 0) != Amount(123000000, 6)
    assert Amount(123, 0) != Amount(12300000, 6)

    assert Amount(400000, 4) >= 39  # , but
    assert Amount(40, 4) < 39

    assert Amount.automatic(40) > 39.0
    assert Amount.automatic(40) >= 40.0
    assert Amount.automatic(40) >= 38.0
    assert Amount.automatic(40) < 40.1
    assert Amount.automatic(40) <= 40.0
    assert Amount.automatic(40) <= 40.1


def test_change_decimals():
    a = Amount(123456789, 8)
    d6 = a.converted_decimals(6)
    assert d6.internal_amount == 1234567
    d10 = a.converted_decimals(10)
    assert d10.internal_amount == 12345678900

    d8 = a.converted_decimals(8)
    assert d8.internal_amount == 123456789


def test_multiply():
    a = Amount(100, 8)
    b = a * 2
    assert b.internal_amount == 200

    c = a * 2.5
    assert c.internal_amount == 250

    d = a * Decimal(0.5)
    assert d.internal_amount == 50

    e = a * Decimal(3.0)
    assert e.internal_amount == 300

    assert a * 0 == 0

    assert Amount(100500, 6) * 2 == Amount(201000, 6)


def test_divide():
    a = Amount(100, 8)
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


def test_divide_amount_and_amount():
    a1 = Amount(100, 8)
    assert a1 / a1 == 1.0
    assert a1 // a1 == 1

    a2 = Amount(20, 8)
    assert a2 / a2 == 1.0
    assert a2 // a2 == 1

    assert a2 / a1 == Decimal('0.2')
    assert a1 / a2 == Decimal('5.0')
    assert a2 // a1 == 0

    a3 = Amount(300, 18)
    with pytest.raises(ZeroDivisionError):
        _ = a3 / Amount(0, 18)

    # different decimals
    assert Amount(480, 2) / Amount(1200, 3) == 4.0
    assert Amount(480, 2) // Amount(1200, 3) == 4

def test_bool():
    assert Amount(400)
    assert Amount(-5)
    assert not Amount(0)
    assert not Amount.automatic_base(0, 4)
    assert not Amount.automatic(0)

    assert Amount(0).is_zero
    assert not Amount.automatic(25.3).is_zero


@pytest.mark.parametrize('internal_amount, decimals, shifter, expected_internal, expected_decimals', [
    (100000000, 8, 2, 1000000, 6),  # Shift left by 2
    (1000000, 6, -2, 100000000, 8),  # Shift right by -2
    (123456789, 8, 0, 123456789, 8),  # No shift
    (1, 8, 8, 0, 0),  # Shift left by all decimals
])
def test_left_shift_correctly_shifts_decimals(internal_amount, decimals, shifter, expected_internal, expected_decimals):
    a = Amount(internal_amount, decimals)
    shifted = a << shifter
    assert shifted.internal_amount == expected_internal
    assert shifted.decimals == expected_decimals


@pytest.mark.parametrize('internal_amount, decimals, shifter', [
    (100000000, 8, '2'),  # Non-integer shifter
    (100000000, 8, None),  # None as shifter
    (100000000, 8, 1.5),  # Float as shifter
])
def test_left_shift_raises_type_error_for_invalid_shifter(internal_amount, decimals, shifter):
    a = Amount(internal_amount, decimals)
    with pytest.raises(TypeError):
        # noinspection PyTypeChecker
        a << shifter


@pytest.mark.parametrize('internal_amount, decimals, shifter, expected_internal, expected_decimals', [
    (100000000, 8, -2, 1000000, 6),  # Shift right by 2
    (1000000, 6, 2, 100000000, 8),  # Shift left by -2
    (123456789, 8, 0, 123456789, 8),  # No shift
    (1, 8, -8, 0, 0),  # Shift right by all decimals
])
def test_right_shift_correctly_shifts_decimals(internal_amount, decimals, shifter, expected_internal,
                                               expected_decimals):
    a = Amount(internal_amount, decimals)
    shifted = a >> shifter
    assert shifted.internal_amount == expected_internal
    assert shifted.decimals == expected_decimals


@pytest.mark.parametrize('internal_amount, decimals, shifter', [
    (100000000, 8, '2'),  # Non-integer shifter
    (100000000, 8, None),  # None as shifter
    (100000000, 8, 1.5),  # Float as shifter
])
def test_right_shift_raises_type_error_for_invalid_shifter(internal_amount, decimals, shifter):
    a = Amount(internal_amount, decimals)
    with pytest.raises(TypeError):
        # noinspection PyTypeChecker
        a >> shifter

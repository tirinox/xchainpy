import math

from .consts import RAIDO_GLYPH, DOLLAR_SIGN


def number_commas(x):
    """
    Display an integer with commas as thousands separators.
    For example, 1234567 -> '1,234,567'.
    :param x: An integer.
    :return: A string with commas.
    """
    if not isinstance(x, int):
        raise TypeError("Parameter must be an integer.")
    if x < 0:
        return '-' + number_commas(-x)
    result = ''
    while x >= 1000:
        x, r = divmod(x, 1000)
        result = f",{r:03d}{result}"
    return f"{x:d}{result}"


def round_to_dig(x, e=2):
    """
    Round a number to a certain number of significant digits.
    :param x: A number to round.
    :param e: The number of significant digits.
    :return: The rounded number.
    """
    return round(x, -int(math.floor(math.log10(abs(x)))) + e - 1)


def pretty_dollar(x, signed=False, postfix=''):
    """
    Pretty-print a number as a dollar amount.
    For example, 1234.567 -> '$1,234.57'.
    :param x: The number to print.
    :param signed: Whether to include a '+' sign for positive numbers.
    :param postfix: A string to append to the number.
    :return: A pretty-printed string.
    """
    return pretty_money(x, prefix=DOLLAR_SIGN, postfix=postfix, signed=signed)


def pretty_rune(x, signed=False, prefix=''):
    """
    Pretty-print a number as a RUNE amount.
    For example, 1234.567 -> 'ᚱ1,234.57'.
    :param x: The number to print.
    :param signed: Whether to include a '+' sign for positive numbers.
    :param prefix: A string to prepend to the number.
    :return: A pretty-printed string.
    """
    return pretty_money(x, postfix=RAIDO_GLYPH, signed=signed, prefix=prefix)


def pretty_money(x, prefix='', signed=False, postfix=''):
    """
    Pretty-print a number as a money amount.
    For example, 1234.567 -> '$1,234.57'.
    :param x: The number to print.
    :param prefix: A string to prepend to the number.
    :param signed: Whether to include a '+' sign for positive numbers.
    :param postfix: A string to append to the number.
    :return: A pretty-printed string.
    """
    if math.isnan(x) or math.isinf(x):
        return str(x)
    if x < 0:
        return f"-{prefix}{pretty_money(-x)}{postfix}"
    elif x == 0:
        r = "0.0"
    else:
        if x < 1e-4:
            r = f'{x:.4f}'
        elif x < 100:
            r = str(round_to_dig(x, 3))
        elif x < 1000:
            r = str(round_to_dig(x, 4))
        else:
            x = int(round(x))
            r = number_commas(x)
    prefix = f'+{prefix}' if signed else prefix
    return f'{prefix}{r}{postfix}'


def too_big(x, limit_abs=1e24):
    """
    Check if a number is too big to be displayed.
    :param x: A number.
    :param limit_abs: The absolute value limit.
    :return: True if the number is too big, False otherwise.
    """
    return math.isinf(x) or math.isnan(x) or abs(x) > limit_abs


def detect_decimal_digits(x):
    """
    Detect the number of decimal digits in a number.
    :param x: A number.
    :return: The number of decimal digits.
    """
    x = abs(x)
    if x > 1.0:
        return 0
    return -int(math.floor(math.log10(x)))


def round_half_up(n, decimals=0):
    """
    Round a number to a certain number of decimal places.
    :param n: A number to round.
    :param decimals: The number of decimal places.
    :return: The rounded number.
    """
    multiplier = 10 ** decimals
    return math.floor(n * multiplier + 0.5) / multiplier


def short_money(x, prefix='', postfix='', localization=None, signed=False, integer=False):
    """
    Shorten a money amount.
    For example, 1234.567 -> '$1.23K' and -123444344.0 -> '-$123.44M'.
    :param x: The number to shorten.
    :param prefix: A string to prepend to the number.
    :param postfix: A string to append to the number.
    :param localization: A dictionary mapping short names to long names. Keys are K, M, B, T
    :param signed: Whether to include a '+' sign for positive numbers.
    :param integer: Whether to round the number to an integer.
    :return: A shortened string.
    """
    if math.isnan(x):
        return str(x)

    if x == 0:
        zero = '0' if integer else '0.0'
        return f'{prefix}{zero}{postfix}'

    if x < 0:
        sign = '-'
        x = -x
    else:
        sign = '+' if signed and x >= 0 else ''

    orig_x = x

    if x < 1_000:
        key = ''
    elif x < 1_000_000:
        x /= 1_000
        key = 'K'
    elif x < 1_000_000_000:
        x /= 1_000_000
        key = 'M'
    elif x < 1_000_000_000_000:
        x /= 1_000_000_000
        key = 'B'
    else:
        x /= 1_000_000_000_000
        key = 'T'

    letter = localization.get(key, key) if localization else key

    if orig_x < 1:
        digits = detect_decimal_digits(orig_x) + 2
        x = f"{x:.{digits}f}".rstrip('0')
    else:
        if integer:
            x = int(x)
        else:
            x = round_half_up(x, 1)

    result = f'{x}{letter}'
    return f'{sign}{prefix}{result}{postfix}'


def short_dollar(x, localization=None, signed=False):
    """
    Shorten a dollar amount. For example, 1234.567 -> '$1.23K' and -123444344.0 -> '-$123.44M'.
    :param x: The number to shorten.
    :param localization: A dictionary mapping short names to long names. Keys are K, M, B, T
    :param signed: Whether to include a '+' sign for positive numbers.
    :return: A shortened string.
    """
    return short_money(x, prefix=DOLLAR_SIGN, localization=localization, signed=signed)


MULT_NOTATION = {
    'k': 10 ** 3,
    'm': 10 ** 6,
    'b': 10 ** 9,
    'q': 10 ** 12
}


def parse_short_number(n: str):
    """
    Parse a short number with a multiplier notation.
    For example, '1.23k' -> 1230.0.
    :param n: A string with a short number.
    :return: A float number.
    """
    n = str(n).strip().lower()
    if not n:
        return 0.0
    mult = MULT_NOTATION.get(n[-1], 1)
    if mult > 1:
        n = n[:-1]
    return float(n) * mult

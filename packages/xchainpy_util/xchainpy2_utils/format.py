import math

from .consts import RAIDO_GLYPH, DOLLAR_SIGN


def number_commas(x):
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
    return round(x, -int(math.floor(math.log10(abs(x)))) + e - 1)


def pretty_dollar(x, signed=False, postfix=''):
    return pretty_money(x, prefix=DOLLAR_SIGN, postfix=postfix, signed=signed)


def pretty_rune(x, signed=False, prefix=''):
    return pretty_money(x, postfix=RAIDO_GLYPH, signed=signed, prefix=prefix)


def pretty_money(x, prefix='', signed=False, postfix=''):
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
    return math.isinf(x) or math.isnan(x) or abs(x) > limit_abs


def detect_decimal_digits(x):
    x = abs(x)
    if x > 1.0:
        return 0
    return -int(math.floor(math.log10(x)))


def round_half_up(n, decimals=0):
    multiplier = 10 ** decimals
    return math.floor(n * multiplier + 0.5) / multiplier


def short_money(x, prefix='', postfix='', localization=None, signed=False, integer=False):
    if math.isnan(x):
        return str(x)

    if x == 0:
        zero = '0' if integer else '0.0'
        return f'{prefix}{zero}{postfix}'

    if hasattr(localization, 'SHORT_MONEY_LOC'):
        localization = localization.SHORT_MONEY_LOC
    localization = localization or {}

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

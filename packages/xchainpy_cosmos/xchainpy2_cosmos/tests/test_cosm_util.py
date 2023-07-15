import pytest

from xchainpy2_cosmos.utils import parse_cosmos_amount


def test_parse_amount():
    assert parse_cosmos_amount('0rune') == (0, 'rune')
    assert parse_cosmos_amount('1025rune') == (1025, 'rune')
    assert parse_cosmos_amount('777555444333uatom') == (777555444333, 'uatom')
    assert parse_cosmos_amount('8g') == (8, 'g')

    with pytest.raises(ValueError):
        assert parse_cosmos_amount('')

    with pytest.raises(ValueError):
        assert parse_cosmos_amount('kfehkh')

    with pytest.raises(ValueError):
        assert parse_cosmos_amount('3483')

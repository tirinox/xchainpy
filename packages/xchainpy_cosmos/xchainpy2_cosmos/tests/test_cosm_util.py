import pytest

from xchainpy2_cosmos.utils import parse_cosmos_amount, parse_cosmos_amounts


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

    assert parse_cosmos_amounts('1rune,5bnb') == [(1, 'rune'), (5, 'bnb')]
    assert parse_cosmos_amounts('210ibc/0025F8A87464A471E66B234C4F93AEC5B4DA3D42D7986451A059273426290DD5,'
                                '667ibc/054892D6BB43AF8B93AAC28AA5FD7019D2C59A15DAFD6F45C1FA2BF9BDA22454,'
                                '18ibc/5CAE744C89BC70AE7B38019A1EDF83199B7E10F00F160E7F4F12BCA7A32A7EE5') == [
               (210, 'ibc/0025F8A87464A471E66B234C4F93AEC5B4DA3D42D7986451A059273426290DD5'),
               (667, 'ibc/054892D6BB43AF8B93AAC28AA5FD7019D2C59A15DAFD6F45C1FA2BF9BDA22454'),
               (18, 'ibc/5CAE744C89BC70AE7B38019A1EDF83199B7E10F00F160E7F4F12BCA7A32A7EE5'),
           ]

    # 1 amount
    assert parse_cosmos_amount('1025304930rune') == (1025304930, 'rune')

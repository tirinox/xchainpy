from xchainpy2_thorchain_amm import THORChainAMM


def test_thor_name():
    validate = THORChainAMM.validate_thorname
    assert not validate('')
    assert not validate('.')
    assert not validate('something.wrong!')
    assert not validate('🆕')

    assert not validate('12345678901234567890123456789012')

    for name in (
            't', 'a',
            '1', '_x_', 'foo', 'orion',
            'me+you',
    ):
        assert validate(name)

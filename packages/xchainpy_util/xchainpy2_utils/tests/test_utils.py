from xchainpy2_utils import remove_0x_prefix


def test_cut_0x():
    assert remove_0x_prefix('0x1234') == '1234'
    assert remove_0x_prefix('1234') == '1234'
    assert remove_0x_prefix('0x') == ''
    assert remove_0x_prefix('') == ''
    assert remove_0x_prefix('0X4344343434343') == '4344343434343'

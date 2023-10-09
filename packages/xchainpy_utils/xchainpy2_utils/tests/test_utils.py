from operator import itemgetter

import pytest

from xchainpy2_utils import remove_0x_prefix, key_attr_getter, unique_by_key


def test_cut_0x():
    assert remove_0x_prefix('0x1234') == '1234'
    assert remove_0x_prefix('1234') == '1234'
    assert remove_0x_prefix('0x') == ''
    assert remove_0x_prefix('') == ''
    assert remove_0x_prefix('0X4344343434343') == '4344343434343'


class Dummy:
    def __init__(self):
        self.attr = 1
        self.foo = 20


def test_key_attr_getter():
    assert key_attr_getter(Dummy(), 'attr') == 1
    assert key_attr_getter(Dummy(), 'foo') == 20

    assert key_attr_getter({
        'foo': 'abc'
    }, 'foo') == 'abc'

    assert key_attr_getter({
        'attr': 10
    }, 'attr') == 10

    with pytest.raises(LookupError):
        assert key_attr_getter({}, 'foo')

    with pytest.raises(LookupError):
        assert key_attr_getter(Dummy(), 'baz')


def test_unique_by_key():
    assert unique_by_key([
        'abc', 'dd', 'boz', 'foo', 'foobar'
    ], len) == ['abc', 'dd', 'foobar']

    assert unique_by_key([], lambda foo: foo.bar) == []

    r = unique_by_key([
        {"hash": "123"},
        {"hash": "cccdd"},
        {"hash": "123"},
        {"hash": "cc77"},
        {"hash": "90ba"},
        {"hash": "13232"},
        {"hash": "90ba"},
    ], itemgetter('hash'))
    assert len(r) == 5
    assert r[0]['hash'] == '123'
    assert r[1]['hash'] == 'cccdd'

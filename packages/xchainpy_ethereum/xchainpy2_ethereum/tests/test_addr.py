import pytest

from xchainpy2_crypto import generate_mnemonic
from xchainpy2_ethereum import EthereumClient
from xchainpy2_ethereum.utils import is_valid_eth_address


@pytest.mark.parametrize('address, valid', [
    ('0xdAC17F958D2', False),
    ('', False),
    (None, False),
    (str, False),
    ('33232323203230238228', False),
    ('fooTest', False),
    ('0xdAC17F958D2ee523a2206206994597C13D831ec7', True),
    ('0xdAC17F958D2ee523a2206206994597C13D831ec8', False),
    ('0xdAC17F958D2ee523a2206206994597C13D831eС7', False),
    ('0x2455e611e7D5bfD829274FfF0A7a5eC9F8CE78cD', True),
])
def test_address_validation(address, valid):
    assert is_valid_eth_address(address) == valid


PHRASE = 'law auto near drink try push consider similar blur chief distance message'


@pytest.mark.parametrize('index, address', [
    (0, '0x764Ec8AD43D2D628f8DC017B69b1bDA0769bBf9e'),
    (1, '0xE3b1AbD0B06aD39A289137f010Bf97878C56D346'),
    (2, '0x235BEC87ba12Bf7F77BA2fc1F69436dE9a497247'),
    (3, '0x4BB4BF43f6f72E7AB43115BE64919fc0e4834f19'),
])
def test_address_derivation(index, address):
    client = EthereumClient(phrase=PHRASE, wallet_index=index)
    address = client.get_address()
    assert is_valid_eth_address(address)
    assert client.get_address() == address

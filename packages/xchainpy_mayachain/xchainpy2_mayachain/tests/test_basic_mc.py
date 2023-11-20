import pytest

from xchainpy2_crypto import generate_mnemonic
from xchainpy2_mayachain import MayaChainClient
from xchainpy2_utils import NetworkType


@pytest.fixture
def client():
    return MayaChainClient(phrase=generate_mnemonic())


@pytest.fixture
def stagenet_client():
    return MayaChainClient(phrase=generate_mnemonic(), network=NetworkType.STAGENET)


# noinspection PyTypeChecker
def test_validate_address(client, stagenet_client):
    assert client.validate_address('thor1qd4my7934h2sn5ag5eaqsde39va4ex2asz3yv5')
    assert client.validate_address('thor1505gp5h48zd24uexrfgka70fg8ccedafsnj0e3')
    assert client.validate_address('thor1505gp5h48zd24uexrfgka70fg8ccedafsnj0e3'.upper())

    assert not client.validate_address('')
    assert not client.validate_address('5230')
    assert not client.validate_address(None)
    assert not client.validate_address(0x34434)
    assert not client.validate_address('thor1qd4my7934h2sn5ag5eaqsde39va4ex2asz3yv51')
    assert not client.validate_address('thor1qd4my7934h2sn5ag5eaqsde39va4ex2asz3yv6')
    assert not client.validate_address('sthor1qd4my7934h2sn5ag5eaqsde39va4ex2asz3yv5')
    assert not client.validate_address('tthor1qd4my7934h2sn5ag5eaqsde39va4ex2asz3yv5')
    assert not client.validate_address('cosmos1qd4my7934h2sn5ag5eaqsde39va4ex2asz3yv5')

    assert not stagenet_client.validate_address('thor1qd4my7934h2sn5ag5eaqsde39va4ex2asz3yv5')
    assert stagenet_client.validate_address('sthor16zj3wfurvc6j6sny8s6gt2s3st9yjypqfjegy2')
    assert stagenet_client.validate_address('sthor1g6pnmnyeg48yc3lg796plt0uw50qpp7humfggz')
    assert stagenet_client.validate_address('sthor1g6pnmnyeg48yc3lg796plt0uw50qpp7humfggz'.upper())


def test_address(client, stagenet_client):
    address = client.get_address()
    assert client.validate_address(address)

    assert len(client.get_private_key()) == 64
    assert len(client.get_public_key().public_key_bytes) == 33

    s_addr = stagenet_client.get_address()
    assert s_addr.removeprefix(address)

    assert len(stagenet_client.get_private_key()) == 64

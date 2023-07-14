import pytest

from xchainpy2_crypto import generate_mnemonic
from xchainpy2_thorchain import THORChainClient
from xchainpy2_utils import NetworkType


@pytest.fixture
def client():
    return THORChainClient(phrase=generate_mnemonic())


@pytest.fixture
def stagenet_client():
    return THORChainClient(phrase=generate_mnemonic(), network=NetworkType.STAGENET)


def test_validate_address(client, stagenet_client):
    assert client.validate_address('thor1qd4my7934h2sn5ag5eaqsde39va4ex2asz3yv5')
    assert client.validate_address('thor1505gp5h48zd24uexrfgka70fg8ccedafsnj0e3')
    assert client.validate_address('thor1505gp5h48zd24uexrfgka70fg8ccedafsnj0e3'.upper())

    assert not client.validate_address('')
    assert not client.validate_address('thor1qd4my7934h2sn5ag5eaqsde39va4ex2asz3yv51')
    assert not client.validate_address('thor1qd4my7934h2sn5ag5eaqsde39va4ex2asz3yv6')
    assert not client.validate_address('sthor1qd4my7934h2sn5ag5eaqsde39va4ex2asz3yv5')
    assert not client.validate_address('tthor1qd4my7934h2sn5ag5eaqsde39va4ex2asz3yv5')
    assert not client.validate_address('cosmos1qd4my7934h2sn5ag5eaqsde39va4ex2asz3yv5')

import pytest

from xchainpy2_crypto import generate_mnemonic
from xchainpy2_mayachain import MayaChainClient
from xchainpy2_utils import NetworkType, CryptoAmount, AssetCACAO


@pytest.fixture
def client():
    return MayaChainClient(phrase=generate_mnemonic())


@pytest.fixture
def stagenet_client():
    return MayaChainClient(phrase=generate_mnemonic(), network=NetworkType.STAGENET)


def test_init(client):
    assert client.network == NetworkType.MAINNET
    assert client._decimal == 10
    assert client._gas_asset == AssetCACAO


def test_wallet_index(client):
    for i in range(1, 5):
        client2 = MayaChainClient(phrase=client.phrase, wallet_index=i)
        assert client.validate_address(client2.get_address())
        assert client2.get_address() != client.get_address()
        assert client2.get_private_key() != client.get_private_key()
        assert client2.get_public_key() != client.get_public_key()

        assert len(client.get_private_key()) == 64


# noinspection PyTypeChecker
def test_validate_address(client):
    assert client.validate_address('maya1qefmyzkgkvu2kz57yv5x5r6k9tvr65v3u2dgvh')
    assert client.validate_address('maya1xdmj4ly3t9afy0fqvxqyar7c2agw9gqjjmxpku')
    assert client.validate_address('maya1xdmj4ly3t9afy0fqvxqyar7c2agw9gqjjmxpku'.upper())

    assert not client.validate_address('')
    assert not client.validate_address('5230')
    assert not client.validate_address(None)
    assert not client.validate_address(0x34434)
    assert not client.validate_address('thor1qd4my7934h2sn5ag5eaqsde39va4ex2asz3yv51')
    assert not client.validate_address('thor1qd4my7934h2sn5ag5eaqsde39va4ex2asz3yv6')
    assert not client.validate_address('sthor1qd4my7934h2sn5ag5eaqsde39va4ex2asz3yv5')
    assert not client.validate_address('tthor1qd4my7934h2sn5ag5eaqsde39va4ex2asz3yv5')
    assert not client.validate_address('cosmos1qd4my7934h2sn5ag5eaqsde39va4ex2asz3yv5')


def test_address(client, stagenet_client):
    address = client.get_address()
    assert client.validate_address(address)

    assert len(client.get_private_key()) == 64
    assert len(client.get_public_key().public_key_bytes) == 33

    s_addr = stagenet_client.get_address()
    assert s_addr.removeprefix(address)

    assert len(stagenet_client.get_private_key()) == 64


@pytest.mark.asyncio
async def test_no_keys():
    client = MayaChainClient()
    amt = CryptoAmount.zero(AssetCACAO)

    with pytest.raises(Exception):
        # deposit without PK or phrase
        await client.deposit(amt, 'foo')

    with pytest.raises(Exception):
        await client.transfer(amt, client.get_address())

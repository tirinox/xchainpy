import pytest

from xchainpy2_bitcoin import BitcoinClient
from xchainpy2_client import KeyException
from xchainpy2_utils import NetworkType

# caution! don't ever send any funds to any address derived from test seed phrase!
DEMO_MNEMONIC = 'deliver wink index glue basket vivid garbage load sister junk river day'


# noinspection PyTypeChecker
def test_valid_address():
    btc = BitcoinClient()
    assert btc.validate_address('bc1qlejn5eh6kf6wm7mxv2drnt0mk66uthvxzcemvc')
    assert btc.validate_address('bc1qauhugdhcvxglgdgcckr7nujy4etkn3z0c5m0wm')
    assert not btc.validate_address('bc1qlejn5eh6kf6wm7mxv2drnt0mk66uthvxzcemv1')
    assert not btc.validate_address('Bc1qlejn5eh6kf6wm7mxv2drnt0mk66uthvxzcemvc')

    assert btc.validate_address('tb1q2x98jkszhtkmpm57wcvl430puwtt0e4gnezn3n')
    assert btc.validate_address('tb1q0zhvv455z0fkpu87r2xe76cxtlwef7ld4wuufe')
    assert not btc.validate_address('tb1q2x98jkszhtkmpm57wcvl450puwtt0e4gnezn3n')
    assert not btc.validate_address('tb2q2x98jkszhtkmpm57wcvl430puwtt0e4gnezn3n')

    assert not btc.validate_address('')
    assert not btc.validate_address(None)
    assert not btc.validate_address(4242)


@pytest.mark.asyncio
async def test_keys_1():
    btc = BitcoinClient(phrase=DEMO_MNEMONIC)
    assert btc.get_address() == 'bc1qlejn5eh6kf6wm7mxv2drnt0mk66uthvxzcemvc'

    btc = BitcoinClient(phrase=DEMO_MNEMONIC, network=NetworkType.TESTNET)
    assert btc.get_address() == 'tb1q2x98jkszhtkmpm57wcvl430puwtt0e4gnezn3n'

    btc = BitcoinClient(phrase=DEMO_MNEMONIC, wallet_index=1)
    assert btc.get_address() == 'bc1qauhugdhcvxglgdgcckr7nujy4etkn3z0c5m0wm'

    btc = BitcoinClient(phrase=DEMO_MNEMONIC, wallet_index=1, network=NetworkType.TESTNET)
    assert btc.get_address() == 'tb1q0zhvv455z0fkpu87r2xe76cxtlwef7ld4wuufe'


@pytest.mark.parametrize("network", [NetworkType.MAINNET, NetworkType.TESTNET, NetworkType.STAGENET])
def test_empty_keys(network):
    client = BitcoinClient(network)
    with pytest.raises(KeyException):
        client.get_address()

    with pytest.raises(KeyException):
        client.get_private_key()

    with pytest.raises(KeyException):
        client.get_public_key()

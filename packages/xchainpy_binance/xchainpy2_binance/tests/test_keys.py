import pytest

from xchainpy2_binance import BinanceChainClient
from xchainpy2_crypto import generate_mnemonic

# caution! don't ever send any funds to any address derived from test seed phrase!
DEMO_MNEMONIC = 'elbow issue leisure umbrella resist diamond river exclude cousin sail siren mom'


@pytest.mark.asyncio
async def test_keys_1():
    bnb = BinanceChainClient(phrase=DEMO_MNEMONIC)
    assert bnb.get_address() == 'bnb1ka9eqcwnfqzqsfy0pdzmq9ju2xpyue2fqecsas'

    bnb = BinanceChainClient(phrase=DEMO_MNEMONIC, wallet_index=1)
    assert bnb.get_address() == 'bnb1hkfvhkfdszdmmkjdvml02wxcyqzs8pkhy57323'

import pytest

from xchainpy2_bitcoin import BitcoinClient, AssetTestBTC
from xchainpy2_utils import NetworkType, AssetBTC


@pytest.mark.parametrize("network", [NetworkType.MAINNET, NetworkType.TESTNET, NetworkType.STAGENET])
def test_client(network):
    client = BitcoinClient(network=network)
    assert client
    assert client.network == network
    assert client.decimal == 8

    if network in (NetworkType.MAINNET, NetworkType.STAGENET):
        assert client._gas_asset == AssetBTC
    else:
        assert client._gas_asset == AssetTestBTC


def test_explorers():
    client = BitcoinClient()
    assert client.get_explorer_url() == 'https://blockstream.info/'
    assert (client.get_explorer_address_url('bc1qlejn5eh6kf6wm7mxv2drnt0mk66uthvxzcemvc')
            == 'https://blockstream.info/address/bc1qlejn5eh6kf6wm7mxv2drnt0mk66uthvxzcemvc')
    assert (client.get_explorer_tx_url('tx_id') == 'https://blockstream.info/tx/tx_id')
    assert (client.get_explorer_tx_url('0b0bc3c25bb8cf15102927fbeb294df91816877e9a9692f70bbaf4f9cd187721')
            == 'https://blockstream.info/tx/0b0bc3c25bb8cf15102927fbeb294df91816877e9a9692f70bbaf4f9cd187721')

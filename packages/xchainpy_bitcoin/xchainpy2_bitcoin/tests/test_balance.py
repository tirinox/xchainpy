import pytest
import requests_mock

from xchainpy2_bitcoin import BitcoinClient
from xchainpy2_bitcoin.tests.common import load_json
from xchainpy2_utils import AssetBTC


@pytest.mark.asyncio
async def test_balance():
    with requests_mock.Mocker() as m:
        m.get('https://blockstream.info/api/address/bc1pjt9a2j85q8yn6p0g7q07c38nev9wct9fquj9fda7283y94khmc0s3fwp4j',
              json=load_json('block_stream_address_4j'))
        m.get('https://mempool.space/api/address/bc1pjt9a2j85q8yn6p0g7q07c38nev9wct9fquj9fda7283y94khmc0s3fwp4j',
              json=load_json('block_stream_address_4j'))

        btc = BitcoinClient()
        balances = await btc.get_balance('bc1pjt9a2j85q8yn6p0g7q07c38nev9wct9fquj9fda7283y94khmc0s3fwp4j')
        assert balances
        assert balances[0].asset == AssetBTC
        assert balances[0].amount.as_base.internal_amount == 5589017

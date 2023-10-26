import asyncio

import pytest
import pytest_asyncio

from xchainpy2_utils import Chain, AssetBTC
from .. import HaskoinProvider

@pytest.fixture(scope='module')
async def haskoin_btc():
    provider = HaskoinProvider.default_bitcoin()
    yield provider
    await provider.session.close()



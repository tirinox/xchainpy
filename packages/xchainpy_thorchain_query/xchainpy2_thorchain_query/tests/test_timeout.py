import pytest
import requests_mock

from .common import *
from xchainpy2_thorchain_query import THORChainCache


@pytest.mark.asyncio
async def test_timeout_thornode(thornode_instance):
    with requests_mock.Mocker() as m:
        m.get(f'{URLs.THORNode.MAINNET}/thorchain/inbound_addresses', json=load_json('inbound_addresses'))

        # Client timeout is 0.01 seconds (very small)

        thornode_instance.configuration.timeout = 0.01

        cache = THORChainCache(None, thornode_instance)

        # This should fail with a timeout error
        with pytest.raises(Exception) as e:
            await cache.get_inbound_details()
        assert 'All backup hosts failed' in str(e.value)
        assert e.value.__cause__.__class__.__name__ == 'TimeoutError'

        thornode_instance.configuration.timeout = 99

        d = await cache.get_inbound_details()
        assert len(d) > 0

        await cache.close()


@pytest.mark.asyncio
async def test_timeout_midgard(thornode_instance, midgard_instance):
    with requests_mock.Mocker() as m:
        m.get(f'{URLs.Midgard.MAINNET}/v2/thorchain/pools', json=load_json('midgard_pools'))
        m.get(f'{URLs.THORNode.MAINNET}/thorchain/inbound_addresses', json=load_json('inbound_addresses'))

        # Client timeout is 0.01 seconds (very small)

        midgard_instance.configuration.timeout = 0.01
        thornode_instance.configuration.timeout = 0.01

        cache = THORChainCache(midgard_instance, thornode_instance)

        # This should fail with a timeout error
        with pytest.raises(Exception) as e:
            await cache.get_pools()
        assert 'All backup hosts failed' in str(e.value)
        assert e.value.__cause__.__class__.__name__ == 'TimeoutError'

        midgard_instance.configuration.timeout = 99
        thornode_instance.configuration.timeout = 99

        d = await cache.get_pools()
        assert len(d) > 0

        await cache.close()

import time

import pytest
from aioresponses import aioresponses

from xchainpy2_thorchain_query import THORChainQuery
from xchainpy2_thorchain_query.tests.common import load_json


@pytest.mark.asyncio
async def test_thor_name_cached():
    with aioresponses() as m:
        m.get('https://midgard.ninerealms.com/v2/thorname/lookup/t',
              status=200,
              payload=load_json('midgard_t_name.json'))
        m.get('https://thornode.ninerealms.com/thorchain/lastblock', status=200, payload=load_json('lastblock.json'))

        query = THORChainQuery()
        name = await query.cache.get_name_details('t')

        assert name
        assert next(
            n for n in name.entries if n.chain == 'THOR').address == 'thor160yye65pf9rzwrgqmtgav69n6zlsyfpgm9a7xk'
        assert int(name.expire) == 60787996

        t0 = time.monotonic()
        await query.cache.get_name_details('t')
        t1 = time.monotonic()
        assert t1 - t0 < 0.01  # cached

        await query.close()


@pytest.mark.asyncio
async def test_thor_name_not_found():
    with aioresponses() as m:
        m.get('https://midgard.ninerealms.com/v2/thorname/lookup/tffeefffefeeefefe',
              status=404, body='not found')
        m.get('https://thornode.ninerealms.com/thorchain/lastblock', status=200, payload=load_json('lastblock.json'))

        query = THORChainQuery()
        name = await query.cache.get_name_details('tffeefffefeeefefe')
        assert not name

        await query.close()

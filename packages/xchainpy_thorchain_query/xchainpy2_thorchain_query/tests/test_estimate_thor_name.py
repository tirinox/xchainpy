import datetime

import pytest
import requests_mock

from xchainpy2_thorchain_query import THORChainQuery


@pytest.mark.asyncio
async def test_estimate_thor_name():
    with requests_mock.Mocker() as m:
        # m.get(f'{URLs.THORNode.MAINNET}/thorchain/inbound_addresses', json=load_json('inbound_addresses'))

        query = THORChainQuery()

        r = await query.estimate_thor_name(False, 'fefefwfebfghh')
        assert r.can_register
        # 10 rune once + 1 rune / year
        assert 11 < float(r.cost.amount) < 12

        r = await query.estimate_thor_name(False, 'fefefwfebfghh',
                                           expiry=datetime.datetime.now() + datetime.timedelta(days=365 * 3))
        assert r.can_register
        # 10 rune once + 1 rune / year => 13
        assert 13 < float(r.cost.amount) < 13.5

        r = await query.estimate_thor_name(True, 'fefefwfebfghh')
        assert not r.can_register

        # already registered, cannot register again

        r = await query.estimate_thor_name(False, 't')
        assert not r.can_register

        await query.close()

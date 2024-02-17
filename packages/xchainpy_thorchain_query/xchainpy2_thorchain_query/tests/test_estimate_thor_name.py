import datetime

import pytest
import requests_mock

from xchainpy2_thorchain_query import THORChainQuery, THORNameException


@pytest.mark.asyncio
async def test_estimate_thor_name():
    with requests_mock.Mocker() as m:
        # m.get(f'{URLs.THORNode.MAINNET}/thorchain/inbound_addresses', json=load_json('inbound_addresses'))

        query = THORChainQuery()

        r = await query.estimate_thor_name(False, 'fefefwfebfghh')
        # 10 rune once + 1 rune / year
        assert 11 < float(r.cost.amount) < 12

        r = await query.estimate_thor_name(False, 'fefefwfebfghh',
                                           expiry=datetime.datetime.now() + datetime.timedelta(days=365 * 3))
        # 10 rune once + 1 rune / year => 13
        assert 13 < float(r.cost.amount) < 13.5

        with pytest.raises(THORNameException):
            # not registered, cannot update
            await query.estimate_thor_name(True, 'fefefwfebfghh')

        with pytest.raises(THORNameException):
            # already registered, cannot register again
            await query.estimate_thor_name(False, 't')

        await query.close()

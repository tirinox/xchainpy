import json

import pytest
from aioresponses import aioresponses

from xchainpy2_client import FeeType, FeeOption
from xchainpy2_thorchain import THORChainClient
from xchainpy2_utils import RUNE_DECIMAL, Amount



def load_json(file_name):
    if not file_name.endswith('.json'):
        file_name = f'{file_name}.json'
    with open(f'./mock/{file_name}') as f:
        return json.load(f)


@pytest.mark.asyncio
async def test_fees_thornode():
    with aioresponses() as m:
        client = THORChainClient()

        m.get(f'https://thornode.ninerealms.com/thorchain/network', payload=load_json('network'))

        fees = await client.get_fees()
        assert fees.type == FeeType.FLAT_FEE
        assert fees.fees[FeeOption.AVERAGE] == fees.fees[FeeOption.FAST] == fees.fees[FeeOption.FASTEST] == \
            Amount.from_base(3120509, RUNE_DECIMAL)

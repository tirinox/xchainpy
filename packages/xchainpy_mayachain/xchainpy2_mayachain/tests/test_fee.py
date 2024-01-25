import json

import pytest
from aioresponses import aioresponses

from xchainpy2_client import FeeType, FeeOption
from xchainpy2_mayachain import DEFAULT_CLIENT_URLS, MayaChainClient
from xchainpy2_utils import Amount, CACAO_DECIMAL, NetworkType


def load_json(file_name):
    if not file_name.endswith('.json'):
        file_name = f'{file_name}.json'
    with open(f'./mock/{file_name}') as f:
        return json.load(f)


@pytest.mark.asyncio
async def test_fee_mayanode():
    with aioresponses() as m:
        client = MayaChainClient()

        base_url = DEFAULT_CLIENT_URLS[NetworkType.MAINNET].node
        m.get(f'{base_url}/mayachain/mimir', payload=load_json('mimir'))

        fees = await client.get_fees()
        assert fees.type == FeeType.FLAT_FEE
        assert fees.fees[FeeOption.AVERAGE] == fees.fees[FeeOption.FAST] == fees.fees[FeeOption.FASTEST] == \
            Amount.from_base(43435934, CACAO_DECIMAL)

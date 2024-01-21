import json

import pytest_asyncio

from xchainpy2_thorchain_query import ConfigurationEx, MidgardAPIClient, URLs
from xchainpy2_thorchain_query.thornode import THORNodeAPIClient


def load_json(file_name):
    if not file_name.endswith('.json'):
        file_name = f'{file_name}.json'
    with open(f'./mock_data/{file_name}') as f:
        return json.load(f)


@pytest_asyncio.fixture
async def midgard_instance():
    midgard = MidgardAPIClient(ConfigurationEx.new(host=URLs.Midgard.MAINNET))
    yield midgard
    await midgard.close()


@pytest_asyncio.fixture
async def thornode_instance():
    thornode = THORNodeAPIClient(ConfigurationEx.new(host=URLs.THORNode.MAINNET))
    yield thornode
    await thornode.close()

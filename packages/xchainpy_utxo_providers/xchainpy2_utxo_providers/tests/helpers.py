import asyncio

import aiohttp
import pytest
import pytest_asyncio

from xchainpy2_utils import Amount


@pytest.fixture(scope="session")
def event_loop():
    return asyncio.get_event_loop()


@pytest_asyncio.fixture
async def client_session():
    session = aiohttp.ClientSession()
    yield session
    await session.close()


@pytest_asyncio.fixture
async def provider_getter(client_session):
    def parametric_func(constructor):
        return constructor(client_session)

    return parametric_func


def amt(x):
    return Amount.from_asset(x, 8).as_base

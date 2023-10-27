import asyncio

import aiohttp
import pytest
import pytest_asyncio


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

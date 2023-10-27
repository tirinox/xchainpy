from .helpers import *


@pytest.mark.asyncio
async def test_foo(client_session):
    async with client_session.get('https://httpbin.org/get') as resp:
        assert resp.status == 200

import time
import warnings

import pytest

from xchainpy2_utils.async_utils import *
from xchainpy2_utils.versions import deprecated


def test_async_wrap():
    @async_wrap
    def _test_f(x):
        time.sleep(0.1)
        return 100 * x

    start_time = time.monotonic()

    assert asyncio.run(_test_f(0)) == 0
    assert asyncio.run(_test_f(1)) == 100
    assert asyncio.run(_test_f(2)) == 200

    elapsed_time = time.monotonic() - start_time

    assert 0.3 < elapsed_time < 0.35



def test_deprecate_async():
    class FooClass:
        @deprecated("Run is obsolete")
        async def run(self):
            print("I am deprecated")

        async def run2(self):
            print("I am good")

    async def call_run():
        with pytest.warns(DeprecationWarning, match="run is deprecated: Run is obsolete"):
            await FooClass().run()

        # Expect no warnings from run2()
        with warnings.catch_warnings():
            warnings.simplefilter("error", DeprecationWarning)  # Turn warnings into errors
            await FooClass().run2()  # Should pass silently

    asyncio.run(call_run())

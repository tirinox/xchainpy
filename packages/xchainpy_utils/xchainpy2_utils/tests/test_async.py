import time

from xchainpy2_utils.async_utils import *


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


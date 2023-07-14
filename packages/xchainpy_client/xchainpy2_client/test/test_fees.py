import pytest

from xchainpy2_client import FeeType, FeeOption
from xchainpy2_client.fees import single_fee, standard_fee, calc_fees, calc_fees_async
from xchainpy2_utils import Amount


def test_single_fee():
    fee = single_fee(FeeType.FLAT_FEE, Amount(10))
    assert fee.type == FeeType.FLAT_FEE
    assert fee.fees and len(fee.fees) == 3
    assert fee.fees[FeeOption.FASTEST] == fee.fees[FeeOption.AVERAGE] == fee.fees[FeeOption.FASTEST] == Amount(10)


def test_std_fee():
    fee = standard_fee(FeeType.PER_BYTE, Amount(10))
    assert fee.type == FeeType.PER_BYTE
    assert fee.fees and len(fee.fees) == 3
    assert fee.fees[FeeOption.AVERAGE] == Amount(5)
    assert fee.fees[FeeOption.FAST] == Amount(10)
    assert fee.fees[FeeOption.FASTEST] == Amount(50)


@pytest.mark.asyncio
async def test_calc_fees():
    def transform(k: FeeOption, v: Amount, a, b):
        c = a * v + b if k != FeeOption.FASTEST else 100
        return Amount.automatic(int(c))

    rates = {
        FeeOption.AVERAGE: 10,
        FeeOption.FAST: 12,
        FeeOption.FASTEST: 16
    }

    r = calc_fees(rates, transform, 2, 3)

    def test_result():
        assert r.type == FeeType.PER_BYTE
        assert r.fees[FeeOption.AVERAGE] == Amount.from_base(23)
        assert r.fees[FeeOption.FAST] == Amount.from_base(27)
        assert r.fees[FeeOption.FASTEST] == Amount.from_base(100)

    test_result()

    async def a_transform(*args):
        return transform(*args)

    r = await calc_fees_async(rates, a_transform, 2, 3)
    test_result()

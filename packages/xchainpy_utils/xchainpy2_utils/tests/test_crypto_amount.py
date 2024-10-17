from decimal import Decimal

import pytest

from xchainpy2_utils import CryptoAmount, Amount, Asset, AssetRUNE, AssetCACAO, Denomination


def test_zero():
    assert CryptoAmount.zero(AssetRUNE) == CryptoAmount(Amount.zero(8), AssetRUNE)
    assert CryptoAmount.zero(AssetCACAO) == CryptoAmount(Amount.zero(8), AssetCACAO)


def test_pick():
    balances = [
        CryptoAmount(Amount(100, 8), Asset.from_string('BNB.BNB')),
        CryptoAmount(Amount(42, 8), AssetRUNE),
    ]
    assert CryptoAmount.pick(balances, AssetRUNE) == CryptoAmount(Amount(42, 8), AssetRUNE)
    assert CryptoAmount.pick(balances, AssetCACAO) == CryptoAmount.zero(AssetCACAO)

    assert CryptoAmount.pick(balances, AssetRUNE).amount.denom == Denomination.ASSET
    assert CryptoAmount.pick(balances, AssetCACAO).amount.denom == Denomination.ASSET


def test_fee_subtract():
    amt = CryptoAmount(Amount(100, 8), AssetRUNE)
    fee = CryptoAmount(Amount(1, 8), AssetRUNE)
    assert amt - fee == CryptoAmount(Amount(99, 8), AssetRUNE)


def test_auto():
    assert CryptoAmount.automatic(1, 'THOR.RUNE') == CryptoAmount(Amount(1, 8), AssetRUNE).as_base
    assert CryptoAmount.automatic(1.0, 'THOR.RUNE') == CryptoAmount(Amount.automatic(1.0, 8), AssetRUNE)

    assert (
            CryptoAmount.automatic(333.5, 'ETH.USDT-0XDAC17F958D2EE523A2206206994597C13D831EC7')
            == CryptoAmount(Amount.automatic(333.5, 6),
                            Asset.from_string('ETH.USDT-0XDAC17F958D2EE523A2206206994597C13D831EC7'))
    )

    assert (CryptoAmount.automatic(40.0, AssetCACAO) == CryptoAmount(Amount.automatic(40.0, 10), AssetCACAO))


def test_multiply():
    amt = CryptoAmount(Amount(100, 8), AssetRUNE)
    assert amt * 2 == CryptoAmount(Amount(200, 8), AssetRUNE)
    assert amt * 0.5 == CryptoAmount(Amount(50, 8), AssetRUNE)
    assert amt * 0 == CryptoAmount.zero(AssetRUNE)

    assert amt * 3.2 == CryptoAmount(Amount(320, 8), AssetRUNE)
    assert amt * Decimal(0.5) == CryptoAmount(Amount(50, 8), AssetRUNE)


@pytest.mark.parametrize('right', [
    "foo",
    Amount(2, 8),
    AssetRUNE,
    CryptoAmount(Amount(2, 8), AssetRUNE),
])
def test_bad_multiply(right):
    amt = CryptoAmount(Amount(9999, 8), AssetRUNE)
    with pytest.raises(TypeError):
        amt * right


def test_change_amount():
    amt = CryptoAmount(Amount(100, 8), AssetRUNE)
    assert amt.change_amount(200) == CryptoAmount(Amount(200, 8), AssetRUNE)
    assert amt.change_amount(0) == CryptoAmount(Amount(0, 8), AssetRUNE)


def test_change_decimals():
    amt = CryptoAmount(Amount.automatic(2.22, 18), Asset.from_string('ETH~ETH'))
    assert amt.decimals == amt.amount.decimals == 18
    amt2 = amt.changed_decimals(8)
    assert amt2.decimals == amt2.amount.decimals == 8

    assert amt2.amount.internal_amount == 222000000
    assert amt.amount.internal_amount == 2220000000000000195

    assert float(amt2.amount) == float(amt.amount)


def test_arithmetic():
    amt = CryptoAmount(Amount(100, 8), AssetRUNE)
    assert amt + amt == CryptoAmount(Amount(200, 8), AssetRUNE)
    assert amt - amt == CryptoAmount.zero(AssetRUNE)

    assert amt * 3 == CryptoAmount(Amount(300, 8), AssetRUNE)
    assert amt / 2 == CryptoAmount(Amount(50, 8), AssetRUNE)

    bmt = CryptoAmount(Amount(100, 8), Asset.from_string('BNB.BNB'))

    with pytest.raises(ValueError):
        amt + bmt


def test_conv():
    amt = CryptoAmount(Amount(100, 8), AssetRUNE)
    assert int(amt) == 100

    amt = amt.change_amount(0)
    assert int(amt) == 0

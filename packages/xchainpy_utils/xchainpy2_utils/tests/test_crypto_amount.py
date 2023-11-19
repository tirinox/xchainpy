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

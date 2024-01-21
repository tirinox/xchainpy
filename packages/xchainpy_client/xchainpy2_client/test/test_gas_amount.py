from decimal import Decimal

import pytest

from xchainpy2_client.test.mocks import MockChainClient
from xchainpy2_utils import AssetRUNE, CryptoAmount, Amount


def test_gas_amount():
    client = MockChainClient()

    assert client.zero_gas_amount.amount == 0
    assert client.zero_gas_amount.asset == AssetRUNE
    assert client.zero_gas_amount.amount.decimals == 7

    assert client.gas_base_amount(3333) == CryptoAmount(Amount.from_base(3333, 7), AssetRUNE)

    with pytest.raises(AssertionError):
        # noinspection PyTypeChecker
        client.gas_base_amount(3333.0)  # only int allowed

    with pytest.raises(AssertionError):
        # noinspection PyTypeChecker
        client.gas_base_amount("3333")

    assert client.gas_asset_amount(0.0000001) == CryptoAmount(Amount.from_asset(0.0000001, 7), AssetRUNE)
    assert client.gas_asset_amount(4433434.5535) == CryptoAmount(Amount.from_asset(4433434.5535, 7), AssetRUNE)
    assert client.gas_asset_amount("4433434.5535") == CryptoAmount(Amount.from_asset(4433434.5535, 7), AssetRUNE)
    assert client.gas_asset_amount(Decimal("4433434.5535")) == CryptoAmount(Amount.from_asset(4433434.5535, 7),
                                                                            AssetRUNE)

    assert client.gas_base_amount(0) == client.zero_gas_amount
    assert client.gas_base_amount(1001) == CryptoAmount(Amount.from_base(1001, 7), AssetRUNE)

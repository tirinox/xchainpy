from datetime import timezone

import pytest

from xchainpy2_utils import (
    Amount,
    AssetBTC,
    AssetRUNE,
    Chain,
    CryptoAmount,
    DEFAULT_CHAIN_ATTRS,
    DAY,
    YEAR,
    batched,
    calculate_days_from_blocks,
    calculate_time_from_blocks,
    clamp,
    flatten,
    number_commas,
    parse_iso_date,
    too_big,
)
from xchainpy2_utils.versions import deprecated


def test_chain_flags_and_currency_symbols():
    assert Chain.Bitcoin.is_utxo
    assert Chain.Arbitrum.is_evm
    assert not Chain.Arbitrum.is_utxo
    assert Chain.THORChain.currency_symbol == "ᚱ"
    assert Chain.Arbitrum.currency_symbol == ""


def test_default_chain_attrs_use_cryptoamount_for_dust():
    btc_dust = DEFAULT_CHAIN_ATTRS[Chain.Bitcoin].dust

    assert isinstance(btc_dust.asset, CryptoAmount)
    assert btc_dust.asset == CryptoAmount(Amount(10_000, 8), AssetBTC)
    assert btc_dust.rune == CryptoAmount.zero(AssetRUNE)


def test_block_time_helpers():
    assert calculate_time_from_blocks(10, Chain.THORChain) == 60
    assert calculate_days_from_blocks(DAY // 6, Chain.THORChain) == 1
    assert YEAR == 365 * DAY


def test_parse_iso_date_handles_z_suffix():
    dt = parse_iso_date("2024-01-02T03:04:05Z")

    assert dt.year == 2024
    assert dt.month == 1
    assert dt.day == 2
    assert dt.tzinfo == timezone.utc


def test_sequence_and_math_helpers():
    assert list(batched(range(5), 2)) == [[0, 1], [2, 3], [4]]
    assert flatten([[1, 2], [], [3]]) == [1, 2, 3]
    assert clamp(-5, 0, 10) == 0
    assert clamp(15, 0, 10) == 10


@pytest.mark.parametrize(
    "value, expected",
    [
        (0, "0"),
        (1_234_567, "1,234,567"),
        (-1_234_567, "-1,234,567"),
    ],
)
def test_number_commas(value, expected):
    assert number_commas(value) == expected


def test_number_commas_rejects_non_ints():
    with pytest.raises(TypeError):
        number_commas(1.5)


def test_too_big_detects_non_finite_and_large_values():
    assert too_big(float("inf"))
    assert too_big(float("nan"))
    assert too_big(1e25)
    assert not too_big(1e6)


def test_deprecated_sync_function_warns_once_per_call():
    @deprecated("use new_function instead")
    def old_function(x):
        return x * 2

    with pytest.warns(DeprecationWarning, match="old_function is deprecated: use new_function instead"):
        assert old_function(3) == 6


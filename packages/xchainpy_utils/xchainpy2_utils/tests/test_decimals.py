import pytest

from xchainpy2_utils import guess_decimals, AssetRUNE, AssetATOM, AssetBSC


@pytest.mark.parametrize("a, dec", [
    ('THOR.RUNE', 8),
    ('ETH.ETH', 18),
    ('BSC.BNB', 18),
    (AssetRUNE, 8),
    (AssetATOM, 6),
    ('ETH.WSTETH-0X7F39C581F595B53C5CB19BD0B3F8DA6C935E2CA0', 18),
    ('ETH.USDC-0XA0B86991C6218B36C1D19D4A2E9EB0CE3606EB48', 6),
    ('ETH.USDT-0XDAC17F958D2EE523A2206206994597C13D831EC7', 6),
    ('ETH.UOS-0XD13C7342E1EF687C5AD21B27C2B65D772CAB5C8C', 4),
    ('AVAX.USDC-0XB97EF9EF8734C71904D8002F8B6BC66DD9C48A6E', 6),
    ('ETH.GUSD-0X056FD409E1D7A124BD7017459DFEA2F387B6D5CD', 2),
    ('KUJI.KUJI', 6),
    ('THOR.RUNE', 8),
    ('GAIA.ATOM', 6),
    ('BNB.BNB', 8),
    ('BCH.BCH', 8),
    ('LTC.LTC', 8),
    ('DOGE.DOGE', 8),
    ('AVAX.AVAX', 18),
    (AssetBSC, 18),
])
def test_decimals(a, dec):
    assert guess_decimals(a) == dec


def test_invalid_chain():
    with pytest.raises(ValueError):
        guess_decimals('INVALID.ASSET-0x12')

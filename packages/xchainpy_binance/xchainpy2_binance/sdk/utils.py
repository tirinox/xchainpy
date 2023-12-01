from decimal import Decimal
from typing import Union

import array
from bech32 import convertbits
from bip_utils import Bech32Decoder
from bip_utils.bech32.bech32 import Bech32Const


def encode_number(num: Union[float, Decimal]) -> int:
    """Encode number multiply by 1e8 (10^8) and round to int

    :param num: number to encode

    """
    if type(num) == Decimal:
        return int(num * (Decimal(10) ** 8))
    else:
        return int(round(num * 1e8))


def varint_encode(num):
    """Convert number into varint bytes

    :param num: number to encode

    """
    buf = b''
    while True:
        towrite = num & 0x7f
        num >>= 7
        if num:
            buf += bytes(((towrite | 0x80),))
        else:
            buf += bytes((towrite,))
            break
    return buf


def decode_address(address):
    # noinspection PyProtectedMember
    hrp, data = Bech32Decoder._DecodeBech32(address, Bech32Const.SEPARATOR, Bech32Const.CHECKSUM_STR_LEN)
    if hrp is None:
        return None

    bits = convertbits(data, 5, 8, False)
    return array.array('B', bits).tobytes()


    # return bytes(data)
    # bits = convertbits(data, 5, 8, False)
    # return array.array('B', bits).tobytes()

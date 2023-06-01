import os
import random
import string

import pytest
from bip_utils import Bech32ChecksumError

from xchainpy2_crypto import encode_address, decode_address


def randomize_characters(s, n):
    # Create a string of valid characters to choose from
    valid_characters = string.ascii_letters + string.digits

    # Convert the string to a list of characters
    chars = list(s)

    # Randomize n characters in the list
    for _ in range(n):
        index = random.randint(0, len(chars) - 1)
        random_char = random.choice(valid_characters)
        chars[index] = random_char

    # Convert the list back to a string
    randomized_string = ''.join(chars)

    return randomized_string


def test_address_encode_decode():
    prefixes = ('thor', 'tthor', 'thorpub', 'tthorpub', 'maya', 'cacao', 'btc')
    for i in range(100):
        pub_key = os.urandom(32)
        prefix = prefixes[i % len(prefixes)]
        address = encode_address(pub_key, prefix)

        assert address.startswith(prefix)
        decoded = decode_address(address, prefix)
        assert decoded == pub_key

        other_pub_key = os.urandom(32)
        assert decode_address(address, prefix) != other_pub_key

        # noinspection PyTypeChecker
        with pytest.raises((ValueError, Bech32ChecksumError)):
            spoiled_address = randomize_characters(address, random.randint(2, 10))
            decode_address(spoiled_address, prefix)

        with pytest.raises(ValueError):
            decode_address(address, randomize_characters(prefix, random.randint(5, 10)))

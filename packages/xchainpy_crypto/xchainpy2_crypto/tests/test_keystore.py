import os
import random

import pytest

from xchainpy2_crypto import generate_mnemonic, KeyStore, InvalidPasswordException


def test_keystore_encrypt_decrypt():
    for i in range(10):
        mnemonic = generate_mnemonic()
        password = os.urandom(random.randint(1, 16)).hex()
        ks = KeyStore.encrypt_to_keystore(mnemonic, password)

        mnemonic_out = ks.decrypt_from_keystore(password)
        assert mnemonic == mnemonic_out


def test_invalid_password():
    mnemonic = generate_mnemonic()
    password = 'good_password123'
    ks = KeyStore.encrypt_to_keystore(mnemonic, password)

    with pytest.raises(InvalidPasswordException):
        ks.decrypt_from_keystore('wrong_password')

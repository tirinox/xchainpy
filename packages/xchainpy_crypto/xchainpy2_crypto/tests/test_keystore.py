import os
import random
import tempfile

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



def test_save_load():
    mnemonic = generate_mnemonic()
    password = 'good_password123'

    ks = KeyStore.encrypt_to_keystore(mnemonic, password)

    # save to temp file
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        ks.save(temp_file.name)
        assert os.path.exists(temp_file.name)

        ks2 = KeyStore.from_file(temp_file.name)
        assert ks.to_dict == ks2.to_dict
        assert ks.meta == ks2.meta and bool(ks.meta)
        assert ks.id == ks2.id and bool(ks.id)
        assert ks.ciphertext == ks2.ciphertext and bool(ks.ciphertext)
        assert ks.cipher == ks2.cipher and bool(ks.cipher)
        assert ks.cipherparams_iv == ks2.cipherparams_iv and bool(ks.cipherparams_iv)
        assert ks.kdf == ks2.kdf and bool(ks.kdf)
        assert ks.kdfparams_prf == ks2.kdfparams_prf and bool(ks.kdfparams_prf)

        assert ks.decrypt_from_keystore(password) == ks2.decrypt_from_keystore(password) == mnemonic

    with pytest.raises(FileNotFoundError):
        KeyStore.from_file('_some_non_existent.txt')

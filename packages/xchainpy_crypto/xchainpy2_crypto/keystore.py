import hashlib
import json
import uuid
from os import urandom
from typing import NamedTuple

from Crypto.Cipher import AES
from Crypto.Hash import BLAKE2b
from Crypto.Util import Counter

from .utils import validate_mnemonic, generate_mnemonic

CIPHER = 'aes-128-ctr'
NBITS = 128
KDF = 'pbkdf2'
PRF = 'hmac-sha256'
DKLEN = 32
C = 262144
HASH_FUNCTION = 'sha256'
META = 'xchain-keystore'
VERSION = 1
ENCODING = 'utf-8'


class InvalidPasswordException(Exception):
    pass


class KeyStore(NamedTuple):
    cipher: str
    ciphertext: str
    cipherparams_iv: str
    kdf: str
    kdfparams_prf: str
    kdfparams_dklen: int
    kdfparams_salt: str
    kdfparams_c: int
    mac: str
    id: str
    version: int
    meta: str

    @property
    def to_dict(self):
        return {
            'crypto': {
                'cipher': self.cipher,
                'ciphertext': self.ciphertext,
                'cipherparams': {
                    'iv': self.cipherparams_iv
                },
                'kdf': self.kdf,
                'kdfparams': {
                    'prf': self.kdfparams_prf,
                    'dklen': self.kdfparams_dklen,
                    'salt': self.kdfparams_salt,
                    'c': self.kdfparams_c
                },
                'mac': self.mac,
            },
            'id': self.id,
            'version': self.version,
            'meta': self.meta
        }

    @property
    def to_json(self):
        return json.dumps(self.to_dict)

    @classmethod
    def from_dict(cls, j):
        crypto = j.get('crypto')
        return cls(
            cipher=crypto['cipher'],
            ciphertext=crypto['ciphertext'],
            cipherparams_iv=crypto['cipherparams']['iv'],
            kdf=crypto['kdf'],
            kdfparams_prf=crypto['kdfparams']['prf'],
            kdfparams_dklen=int(crypto['kdfparams']['dklen']),
            kdfparams_salt=crypto['kdfparams']['salt'],
            kdfparams_c=crypto['kdfparams']['c'],
            mac=crypto['mac'],
            id=j['id'],
            version=j['version'],
            meta=j['meta']
        )

    @classmethod
    def from_file(cls, path):
        with open(path) as f:
            data = json.load(f)
            return cls.from_dict(data)

    def save(self, path: str, indent=4):
        with open(path, 'w') as f:
            json.dump(self.to_dict, f, indent=indent)

    @classmethod
    def encrypt_to_keystore(cls, mnemonic: str, password: str):
        """
        Encrypts a mnemonic to a keystore with a password
        :param str mnemonic: BIP39 mnemonic
        :param str password: Password
        :return: KeyStore
        """
        if not validate_mnemonic(mnemonic):
            raise Exception("Invalid BIP39 Phrase")

        ID = str(uuid.uuid4())
        salt = urandom(32)
        iv = urandom(16).hex()

        derived_key = hashlib.pbkdf2_hmac(
            HASH_FUNCTION,
            password.encode(ENCODING),
            salt,
            C,
            DKLEN
        )

        ctr = Counter.new(NBITS, initial_value=int(iv, 16))
        aes_cipher = AES.new(derived_key[0:16], AES.MODE_CTR, counter=ctr)
        cipher_bytes = aes_cipher.encrypt(mnemonic.encode("utf8"))

        blake256 = BLAKE2b.new(digest_bits=256)
        blake256.update((derived_key[16:32] + cipher_bytes))
        mac = blake256.hexdigest()

        return cls(
            cipher=CIPHER,
            ciphertext=cipher_bytes.hex(),
            cipherparams_iv=iv,
            kdf=KDF,
            kdfparams_prf=PRF,
            kdfparams_dklen=DKLEN,
            kdfparams_salt=salt.hex(),
            kdfparams_c=C,
            mac=mac,
            id=ID,
            version=VERSION,
            meta=META
        )

    def decrypt_from_keystore(self, password: str):
        """
        Derives a mnemonic from a keystore with a password
        :param str password: password
        :return: str Mnemonic phrase
        """
        derived_key = hashlib.pbkdf2_hmac(
            HASH_FUNCTION,
            password.encode(ENCODING),
            bytes.fromhex(self.kdfparams_salt),
            self.kdfparams_c,
            self.kdfparams_dklen
        )

        cipher_bytes = bytes.fromhex(self.ciphertext)

        blake256 = BLAKE2b.new(digest_bits=256)
        blake256.update((derived_key[16:32] + cipher_bytes))
        mac = blake256.hexdigest()
        if mac != self.mac:
            raise InvalidPasswordException("Invalid password")

        ctr = Counter.new(NBITS, initial_value=int(self.cipherparams_iv, 16))
        aes_cipher = AES.new(derived_key[0:16], AES.MODE_CTR, counter=ctr)
        phrase = aes_cipher.decrypt(cipher_bytes)
        return phrase.decode("utf8")

    @classmethod
    def generate_and_encrypt(cls, password: str, *args, **kwargs):
        mnemonic = generate_mnemonic(*args, **kwargs)
        return cls.encrypt_to_keystore(mnemonic, password)

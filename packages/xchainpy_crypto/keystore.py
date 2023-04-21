import hashlib
import json
import uuid
from os import urandom
from typing import NamedTuple

from Crypto.Cipher import AES
from Crypto.Hash import BLAKE2b
from Crypto.Util import Counter

from utils import validate_mnemonic

CIPHER = 'aes-128-ctr'
NBITS = 128
KDF = 'pbkdf2'
PRF = 'hmac-sha256'
DKLEN = 32
C = 262144
HASH_FUNCTION = 'sha256'
META = 'xchain-keystore'
VERSION = 1


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
            'id': self.id,
            'version': self.version,
            'meta': self.meta
        }

    @property
    def to_json(self):
        return json.dumps(self.to_dict)

    @classmethod
    def from_dict(cls, j):
        return cls(
            cipher=j['cipher'],
            ciphertext=j['ciphertext'],
            cipherparams_iv=j['cipherparams']['iv'],
            kdf=j['kdf'],
            kdfparams_prf=j['kdfparams']['prf'],
            kdfparams_dklen=int(j['kdfparams']['dklen']),
            kdfparams_salt=j['kdfparams']['salt'],
            kdfparams_c=j['kdfparams']['c'],
            mac=j['mac'],
            id=j['id'],
            version=j['version'],
            meta=j['meta']
        )

    @classmethod
    def from_file(cls, path):
        with open(path, 'r') as f:
            return cls.from_dict(json.load(f))

    def save(self, path: str, indent=4):
        with open(path, 'w') as f:
            json.dump(self.to_dict, f, indent=indent)

    @classmethod
    def from_mnemonic_and_password(cls, mnemonic: str, password: str):
        if not validate_mnemonic(mnemonic):
            raise Exception("Invalid BIP39 Phrase")

        ID = str(uuid.uuid4())
        salt = urandom(32)
        iv = urandom(16).hex()

        derived_key = hashlib.pbkdf2_hmac(
            HASH_FUNCTION,
            password.encode('utf-8'),
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

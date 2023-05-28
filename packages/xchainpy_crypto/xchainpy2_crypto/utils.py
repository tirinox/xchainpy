from typing import Union

from Crypto.Hash import RIPEMD160, SHA256
from bip_utils import Bip39MnemonicGenerator, Bip39WordsNum, Bip39Languages, Bip39MnemonicValidator, \
    Bip39SeedGenerator, Bech32Encoder, Bip32Secp256k1


def generate_mnemonic(words_number=Bip39WordsNum.WORDS_NUM_12, lang=Bip39Languages.ENGLISH):
    """
    Generate a mnemonic phrase
    :param words_number: Words number 12/24, default: 12
    :param lang: Language, default: English
    :return: str: Mnemonic phrase
    """
    mnemonic = Bip39MnemonicGenerator(lang=lang).FromWordsNumber(words_number)
    return str(mnemonic)


def _normalize_mnemonic_type(mnemonic: str) -> str:
    if isinstance(mnemonic, (list, tuple)):
        mnemonic = ' '.join(mnemonic)
    return mnemonic


def validate_mnemonic(mnemonic: str, lang: str = None) -> bool:
    """
    :param mnemonic: Mnemonic phrase or list of words
    :param lang: Bip39Languages or None
    :return: bool: True if valid, False otherwise
    """
    if not mnemonic:
        return False
    mnemonic = _normalize_mnemonic_type(mnemonic)
    return Bip39MnemonicValidator(lang).IsValid(mnemonic)


def get_seed(mnemonic, lang: str = None) -> bytes:
    """
    :param mnemonic: Mnemonic phrase or list of words
    :param lang: Bip39Languages or None
    :return: bytes: Seed
    """
    mnemonic = _normalize_mnemonic_type(mnemonic)
    return Bip39SeedGenerator(mnemonic, lang).Generate()


def sha256ripemd160(hex_str: str) -> str:
    """
    Calculate `ripemd160(sha256(hex))` from the hex string
    :param str hex_str: Input hex string
    :return: str: Output hex string
    """
    data = bytes.fromhex(hex_str)
    return RIPEMD160.RIPEMD160Hash(
        SHA256.SHA256Hash(data).digest()
    ).hexdigest()


def encode_address(value: Union[str, bytes], prefix='thor') -> str:
    """
    Encode address from the string or bytes
    :param str value: Input
    :param str prefix: Address prefix 'thor' by default
    :return: str: Address
    """
    if isinstance(value, str):
        value = bytes.fromhex(value)
    return Bech32Encoder.Encode(prefix, value)


def create_address(public_key: bytes, prefix='thor') -> str:
    """
    Create address from public key
    :param bytes public_key: Public key
    :param str prefix: Address prefix
    :return: str: Address
    """
    hexed = public_key.hex()
    hash_hex = sha256ripemd160(hexed)
    return encode_address(hash_hex, prefix)


def get_bip32(seed: bytes, derivation_path: str) -> Bip32Secp256k1:
    return Bip32Secp256k1.FromSeed(seed).DerivePath(derivation_path)

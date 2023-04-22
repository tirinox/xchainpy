from bip_utils import Bip39MnemonicGenerator, Bip39WordsNum, Bip39Languages, Bip39MnemonicValidator, Bip39SeedGenerator


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


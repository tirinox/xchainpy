from bip_utils import Bip39MnemonicGenerator, Bip39WordsNum, Bip39Languages, Bip39MnemonicValidator


def generate_mnemonic(words_number=Bip39WordsNum.WORDS_NUM_12, lang=Bip39Languages.ENGLISH):
    """
    Generate a mnemonic phrase
    :param words_number: Words number 12/24, default: 12
    :param lang: Language, default: English
    :return: str: Mnemonic phrase
    """
    mnemonic = Bip39MnemonicGenerator(lang=lang).FromWordsNumber(words_number)
    return str(mnemonic)


def validate_mnemonic(mnemonic: str, lang: str = None) -> bool:
    """
    :param mnemonic: Mnemonic phrase or list of words
    :param lang: Bip39Languages or None
    :return: bool: True if valid, False otherwise
    """
    if isinstance(mnemonic, (list, tuple)):
        mnemonic = ' '.join(mnemonic)
    return Bip39MnemonicValidator(lang).IsValid(mnemonic)

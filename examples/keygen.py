
from xchainpy2_crypto import generate_mnemonic, validate_mnemonic, KeyStore, get_seed
from bip_utils import Bip39Languages


def demo_generate_mnemonics():
    PARAMS = [
        (12, Bip39Languages.ENGLISH),
        (12, Bip39Languages.FRENCH),
        (15, Bip39Languages.ENGLISH),
        (24, Bip39Languages.ENGLISH),
        (24, Bip39Languages.CHINESE_TRADITIONAL),
    ]

    for n, lang in PARAMS:
        mnemonic = generate_mnemonic(n, lang)
        valid = validate_mnemonic(mnemonic)
        print(f"{n = }, {lang = :<40}, {mnemonic!s}\n{valid = }")

    assert not validate_mnemonic('abandon abandon abandon 33')


def demo_keystore():
    mnemonic = generate_mnemonic()
    password = 'password123'
    print(f"{mnemonic = }")
    ks = KeyStore.encrypt_to_keystore(mnemonic, password)
    print(ks)
    ks.save('data/example_keystore.json')

    mnemonic_out = ks.decrypt_from_keystore(password)
    print(mnemonic_out)

    seed = get_seed(mnemonic)
    print(seed.hex())


if __name__ == '__main__':
    demo_generate_mnemonics()
    demo_keystore()

from xchainpy2_crypto import *

def test_create_mnemonic():
    mnemonic = generate_mnemonic()
    assert len(mnemonic.split()) == 12
    assert validate_mnemonic(mnemonic)

    mnemonic = generate_mnemonic(15)
    assert len(mnemonic.split()) == 15
    assert validate_mnemonic(mnemonic)

    mnemonic = generate_mnemonic(24)
    assert len(mnemonic.split()) == 24
    assert validate_mnemonic(mnemonic)

    assert not validate_mnemonic('')
    assert not validate_mnemonic(None)

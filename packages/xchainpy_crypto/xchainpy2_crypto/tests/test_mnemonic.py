import pytest

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


@pytest.mark.parametrize('wallet_index, key, address', [
    (0, '437a3090352a646872f9ddc9c172e7d74d3e0472bc67ca5eccef0a64b94d791d',
     'thor14nhwuxr8e00m2qtfgpqtwafnw25x8vmtka8c5a'),
    (1, 'aea64d24898d02b080b6231ee0778e3f4c0b31cf756b565d586b8e7f390feafe',
     'thor14p9fz9f8hw6f7jeh9msxg6v7xw65r52r7xnjka'),
    (2, '55935cd344247aa0cb2dca2c13780f7ed9a571efd709cae9e82204ef57ec62ef',
     'thor1xs3tksyfhyxe2xlwr9rtlcjm0pzthdsuavx39c')
])
def test_wallet_private_key_index(wallet_index, key, address):
    # totally random, no worries
    mnemonic = 'grain dizzy better fossil taste install tobacco bless source science category van'

    derivation_path = f"44'/931'/0'/0/{wallet_index}"

    seed = get_seed(mnemonic)
    assert len(seed) == 64
    gen_key = get_bip32(seed, derivation_path)

    priv_key = get_private_key(gen_key)
    pub_key = get_public_key(gen_key)

    assert priv_key.hex() == key, 'Generated key does not match expected key'
    assert create_address(pub_key, 'thor') == address, 'Generated address does not match expected address'

    assert derive_private_key(mnemonic, derivation_path).hex() == key, 'Generated key does not match expected key'
    assert derive_address(mnemonic, derivation_path, 'thor') == address, \
        'Generated address does not match expected address'

from typing import Optional

import binascii

# from .utils.segwit_addr import address_from_public_key, decode_address
from .environment import BinanceEnvironment
# from .http_cli import HttpApiClient


class BaseWallet:
    HD_PATH = "44'/714'/0'/0/{id}"

    def __init__(self, env: Optional[BinanceEnvironment] = None, hd_path: str = HD_PATH):
        self._env = env or BinanceEnvironment.get_production_env()
        self._public_key = None
        self._address = None
        self._account_number = None
        self._sequence = None
        self._chain_id = None
        self._http_client = None
        self._hd_path = hd_path

    def initialise_wallet(self):
        if self._account_number:
            return
        account = self._get_http_client().get_account(self._address)

        self._account_number = account['account_number']
        self._sequence = account['sequence']

        node_info = self._get_http_client().get_node_info()
        self._chain_id = node_info['node_info']['network']

    def increment_account_sequence(self):
        if self._sequence:
            self._sequence += 1

    def decrement_account_sequence(self):
        if self._sequence:
            self._sequence -= 1

    def reload_account_sequence(self):
        sequence_res = self._get_http_client().get_account_sequence(self._address)
        self._sequence = sequence_res['sequence']

    def generate_order_id(self):
        return f"{binascii.hexlify(self.address_decoded).decode().upper()}-{(self._sequence + 1)}"

    def _get_http_client(self):
        # if not self._http_client:
        #     self._http_client = HttpApiClient(self._env)
        return self._http_client

    @property
    def env(self):
        return self._env

    @property
    def address(self):
        return self._address

    @property
    def address_decoded(self):
        # return decode_address(self._address)
        raise NotImplementedError  # todo

    @property
    def public_key(self):
        return self._public_key

    @property
    def public_key_hex(self):
        return binascii.hexlify(self._public_key)

    @property
    def account_number(self):
        return self._account_number

    @property
    def sequence(self):
        return self._sequence

    @property
    def chain_id(self):
        return self._chain_id

    def sign_message(self, msg_bytes):
        raise NotImplementedError


class Wallet(BaseWallet):
    """
    Usage example:

    m = Wallet.create_random_mnemonic() # 12 words
    p = 'my secret passphrase' # bip39 passphrase

    # Store <m> and <p> somewhere safe

    wallet1 = Wallet.create_wallet_from_mnemonic(m, passphrase=p, child=0, env=testnet_env)
    wallet2 = Wallet.create_wallet_from_mnemonic(m, passphrase=p, child=1, env=testnet_env)
    ...

    """

    def __init__(self, private_key, env: Optional[BinanceEnvironment] = None, hd_path: str = BaseWallet.HD_PATH):
        super().__init__(env, hd_path=hd_path)
        self._private_key = private_key
        # self._pk = PrivateKey(bytes(bytearray.fromhex(self._private_key)))
        # self._public_key = self._pk.pubkey.serialize(compressed=True)
        # self._address = address_from_public_key(self._public_key, self._env.hrp)

    @property
    def private_key(self):
        return self._private_key

    def sign_message(self, msg_bytes: bytes) -> bytes:
        # check if ledger wallet
        raise NotImplementedError  # todo
        # sig = self._pk.ecdsa_sign(msg_bytes)
        # return self._pk.ecdsa_serialize_compact(sig)

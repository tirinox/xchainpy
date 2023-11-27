from typing import NamedTuple

import binascii


class Account(NamedTuple):
    account_number: int
    sequence: int
    address: str
    address_bytes: bytes
    chain_id: str
    balances: list
    public_key: bytes
    private_key: bytes

    def generate_order_id(self):
        return f"{binascii.hexlify(self.address).decode().upper()}-{(self.sequence + 1)}"

    def with_private_key(self, pk: bytes):
        return self._replace(private_key=pk)


class BaseWallet:
    def __init__(self, public_key=None, address=None, account_number=None, sequence=None, chain_id=None):
        self.public_key = public_key
        self.address = address
        self.account_number = account_number
        self.sequence = sequence
        self.chain_id = chain_id

    def increment_account_sequence(self):
        if self.sequence:
            self.sequence += 1

    def decrement_account_sequence(self):
        if self.sequence:
            self.sequence -= 1

    def generate_order_id(self):
        return f"{binascii.hexlify(self.address_decoded).decode().upper()}-{(self.sequence + 1)}"

    @property
    def address_decoded(self):
        # return decode_address(self._address)
        raise NotImplementedError  # todo

    @property
    def public_key_hex(self):
        return binascii.hexlify(self.public_key)

    def sign_message(self, msg_bytes):
        raise NotImplementedError

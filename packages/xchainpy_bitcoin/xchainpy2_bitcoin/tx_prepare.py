import binascii
import math
from typing import List, Optional

from bitcoinlib.transactions import Output, Transaction

from xchainpy2_bitcoin.accumulative import accumulative
from xchainpy2_bitcoin.utils import UTXOException
from xchainpy2_client import UTXO
from xchainpy2_utils import Amount

OP_RETURN = 106
OP_RETURN_HEX = '6a'


def try_get_memo_from_output(out: Output) -> Optional[str]:
    """
    Try to get the memo string from the output script.

    :param out: Output to get the memo from
    :return: Memo string if found, None otherwise
    """
    if len(out.script.commands) >= 2 and out.script.commands[0] == OP_RETURN:
        return out.script.commands[1].decode('utf-8')


def compile_memo(memo: str) -> bytes:
    """Compile a memo string to a script for OP_RETURN output.
    https://dev.thorchain.org/concepts/sending-transactions.html#utxo-chains

    :param memo: The memo to be compiled
    :type memo: str
    :returns: The compiled memo: bytes
    """
    metadata = bytes(memo, 'utf-8')
    metadata_len = len(metadata)

    if metadata_len <= 75:
        # length byte + data (https://en.bitcoin.it/wiki/Script)
        payload = bytearray((metadata_len,)) + metadata
    elif metadata_len <= 256:
        # OP_PUSHDATA1 format
        payload = b"\x4c" + bytearray((metadata_len,)) + metadata
    else:
        # OP_PUSHDATA2 format
        chunks = metadata_len // 256
        rest = metadata_len % 256
        payload = b"\x4d" + bytearray((rest,)) + bytearray((chunks,)) + metadata

    compiled_memo = binascii.b2a_hex(payload).decode()
    compiled_memo = OP_RETURN_HEX + compiled_memo
    compiled_memo = binascii.unhexlify(compiled_memo)
    return compiled_memo


class UTXOPrepare:
    """
    UTXOPrepare is a class to prepare transactions in UTXO networks.
    It computes the inputs and outputs of a transaction based on the available UTXOs and the desired outputs.
    """

    def __init__(self, utxos: List[UTXO], service_network, fee_per_byte=1, min_confirmations=1):
        self.service_network = service_network
        self.utxos = utxos
        self.fee_per_byte = fee_per_byte
        self.min_confirmations = min_confirmations
        self.witness_type = 'segwit'

    @staticmethod
    def make_output_with_memo(memo: str):
        """
        Create an output with a memo which is OP_RETURN.

        :param memo: Memo to be added to the output
        :return: Output description
        """
        return {
            'value': 0,
            'script': compile_memo(memo),
        }

    def available_utxos(self):
        """
        Get the available UTXOs based on the minimum confirmations.

        :return: List of available UTXOs
        """
        return [utxo for utxo in self.utxos if utxo.confirmations >= self.min_confirmations]

    @property
    def fee_rate_whole(self):
        """
        Get the fee rate in whole number.

        :return: Fee rate in whole number
        """
        return int(math.ceil(self.fee_per_byte))

    def build(self, sender: str, recipient: str, amount: Amount, memo: Optional[str] = None) -> Transaction:
        """
        Build a transaction based on the sender, recipient, amount and memo.

        :param sender: Sender address
        :param recipient: Address of the recipient
        :param amount: Amount of gas asset to be transferred
        :param memo: Optional memo to be added to the transaction
        :return: Transaction object of bitcoinlib
        """
        # return Output(0, recipient, lock_script=compile_memo(memo), network=self.service_network)
        outputs = [
            # this output is the actual transfer
            {
                'value': int(amount.as_base),
                'address': recipient,
            }
        ]

        if memo:
            if len(memo) > 80:
                raise UTXOException('Memo too long, must not be longer than 80 chars.')
            # this output is the memo
            outputs.append(self.make_output_with_memo(memo))

        available_utxos = self.available_utxos()
        if len(available_utxos) == 0:
            raise UTXOException('No available utxos. Have you waited for confirmations?')

        raw_available_utxos = [
            {
                'value': utxo.value,
                'hash': utxo.hash,
                'index': utxo.index,
                'witness_utxo': {
                    'value': utxo.value,
                    'script': '',
                }
            } for utxo in available_utxos
        ]

        acc_result = accumulative(raw_available_utxos, outputs, self.fee_rate_whole)
        if not acc_result.inputs or not acc_result.outputs:
            raise UTXOException('Insufficient balance for transaction')

        for output in acc_result.outputs:
            if not output.get('address') and output.get('value') > 0:
                # an empty address means this is the change address
                output['address'] = sender

        t = Transaction(network=self.service_network, witness_type=self.witness_type, version=2)

        for the_input in acc_result.inputs:
            txid = the_input.get('hash')
            index = the_input.get('index')
            t.add_input(
                prev_txid=txid,
                output_n=index,
                witness_type=self.witness_type,
                value=the_input.get('value')
            )

        for output in acc_result.outputs:
            if output.get('address'):
                t.add_output(value=output.get('value'), address=output.get('address'))
            elif output.get('script'):
                t.add_output(value=output.get('value'), lock_script=output.get('script'))

        return t

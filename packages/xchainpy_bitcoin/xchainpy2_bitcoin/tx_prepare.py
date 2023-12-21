import binascii
import math
from typing import List, Optional

from bitcoinlib.transactions import Output, Transaction, Input

from xchainpy2_bitcoin.utils import UTXOException
from xchainpy2_bitcoin.accumulative import accumulative
from xchainpy2_client import UTXO
from xchainpy2_utils import Amount

OP_RETURN = 106
OP_RETURN_HEX = '6a'


def try_get_memo_from_output(out: Output) -> Optional[str]:
    if len(out.script.commands) >= 2 and out.script.commands[0] == OP_RETURN:
        return out.script.commands[1].decode('utf-8')


def compile_memo(memo: str) -> bytes:
    """Compile memo

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

    compiled_memo = binascii.b2a_hex(payload).decode('utf-8')
    compiled_memo = OP_RETURN_HEX + compiled_memo
    compiled_memo = binascii.unhexlify(compiled_memo)
    return compiled_memo


class UTXOPrepare:
    def __init__(self, utxos: List[UTXO], service_network, fee_per_byte=1, min_confirmations=1):
        self.service_network = service_network
        self.utxos = utxos
        self.fee_per_byte = fee_per_byte
        self.min_confirmations = min_confirmations

    def make_output_with_memo(self, recipient: str, memo: str):
        return Output(0, recipient, lock_script=compile_memo(memo), network=self.service_network)

    def available_utxos(self):
        return [utxo for utxo in self.utxos if utxo.confirmations >= self.min_confirmations]

    @property
    def fee_rate_whole(self):
        return int(math.ceil(self.fee_per_byte))

    def build(self, sender: str, recipient: str, amount: Amount, memo: Optional[str] = None) -> Transaction:
        outputs = [
            Output(
                int(amount.as_base),
                recipient,
                network=self.service_network
            )
        ]

        if memo:
            if len(memo) > 80:
                raise UTXOException('Memo too long, must not be longer than 80 chars.')
            outputs.append(self.make_output_with_memo(recipient, memo))

        available_utxos = self.available_utxos()
        if len(available_utxos) == 0:
            raise UTXOException('No available utxos. Have you waited for confirmations?')

        raw_outputs = [
            {
                'script': output.script.raw,
                'value': output.value,
            } for output in outputs
        ]
        raw_available_utxos = [
            {
                'value': utxo.value,
                'script': utxo.witness_utxo.script,
            } for utxo in available_utxos
        ]

        acc_result = accumulative(raw_available_utxos, raw_outputs, self.fee_rate_whole)
        if not acc_result.inputs or not acc_result.outputs:
            raise UTXOException('Insufficient balance for transaction')

        for output in acc_result.outputs:
            if not output['address']:
                # an empty address means this is the change address
                output['address'] = sender

        inputs = [
            Input()
        ]

        t = Transaction(inputs, outputs)
        return t

        # r = [
        #     {'address': 'blt1q74y0083lzwmhsdf336hl5ptwxlqqwthdsdws84',
        #      'txid': 'fe2acca01e507c4815984418ab6a5ab703b31a49daff6b3db17ea2f91a3de61c', 'confirmations': 10,
        #      'output_n': 0, 'index': 0, 'value': 100000000, 'script': ''},
        #     {'address': 'blt1q74y0083lzwmhsdf336hl5ptwxlqqwthdsdws84',
        #      'txid': '01ff110796c32a4ff9c7c3895a1809172630f5629e6b49e606ad483f0afd1c67', 'confirmations': 10,
        #      'output_n': 0, 'index': 0, 'value': 100000000, 'script': ''}
        # ]


"""

    const targetOutputs = []

    //1. add output amount and recipient to targets
    targetOutputs.push({
      address: recipient,
      value: amount.amount().toNumber(),
    })
    //2. add output memo to targets (optional)
    if (compiledMemo) {
      targetOutputs.push({ script: compiledMemo, value: 0 })
    }
    const { inputs, outputs } = accumulative(utxos, targetOutputs, feeRateWhole)

    // .inputs and .outputs will be undefined if no solution was found
    if (!inputs || !outputs) throw new Error('Insufficient Balance for transaction')

    const psbt = new Bitcoin.Psbt({ network: Utils.btcNetwork(this.network) }) // Network-specific

    // psbt add input from accumulative inputs
    inputs.forEach((utxo: UTXO) =>
      psbt.addInput({
        hash: utxo.hash,
        index: utxo.index,
        witnessUtxo: utxo.witnessUtxo,
      }),
    )

    // psbt add outputs from accumulative outputs
    outputs.forEach((output: Bitcoin.PsbtTxOutput) => {
      if (!output.address) {
        //an empty address means this is the  change ddress
        output.address = sender
      }
      if (!output.script) {
        psbt.addOutput(output)
      } else {
        //we need to add the compiled memo this way to
        //avoid dust error tx when accumulating memo output with 0 value
        if (compiledMemo) {
          psbt.addOutput({ script: compiledMemo, value: 0 })
        }
      }
    })

    return { psbt, utxos, inputs }
  }
"""

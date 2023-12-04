import binascii

from xchainpy2_utils import NetworkType


def get_btc_address_prefix(network: NetworkType) -> str:
    """
    Get address prefix based on the network.
    :param network:
    :return: string address prefix
    """
    if network == NetworkType.TESTNET:
        return 'tb1'
    elif network == NetworkType.STAGENET:
        return 'bc1'
    elif network == NetworkType.MAINNET:
        return 'bc1'
    else:
        raise ValueError('Invalid network')


def compile_memo(memo: str) -> bytes:
    """Compile memo

    :param memo: The memo to be compiled
    :type memo: str
    :returns: The compiled memo: bytes
    """
    metadata = bytes(memo, 'utf-8')
    metadata_len = len(metadata)
    op_return = '6a'

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
    compiled_memo = op_return + compiled_memo
    compiled_memo = binascii.unhexlify(compiled_memo)
    return compiled_memo

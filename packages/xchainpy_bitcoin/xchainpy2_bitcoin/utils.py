from xchainpy2_utils import NetworkType


class UTXOException(Exception):
    """
    Exception raised when there is an issue with UTXO Client operations.
    """
    ...


def get_btc_address_prefix(network: NetworkType) -> str:
    """
    Get address prefix based on the network.

    :param network: Network type
    :return: string address prefix
    """
    if network == NetworkType.TESTNET:
        return 'tb1'
    elif network == NetworkType.DEVNET:
        return 'blt'
    elif network == NetworkType.STAGENET:
        return 'bc1'
    elif network == NetworkType.MAINNET:
        return 'bc1'
    else:
        raise ValueError('Invalid network')

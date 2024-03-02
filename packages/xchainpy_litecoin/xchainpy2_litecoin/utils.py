from xchainpy2_utils import NetworkType


def get_ltc_address_prefix(network: NetworkType) -> str:
    """
    Get address prefix based on the network.
    :param network:
    :return: string address prefix
    """
    if network == NetworkType.TESTNET:
        return 'tltc1'
    elif network == NetworkType.DEVNET:
        return 'tltc1'
    elif network == NetworkType.STAGENET:
        return 'ltc1'
    elif network == NetworkType.MAINNET:
        return 'ltc1'
    else:
        raise ValueError('Invalid network')

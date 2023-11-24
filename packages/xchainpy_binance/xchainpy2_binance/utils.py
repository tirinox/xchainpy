from xchainpy2_utils import NetworkType


def get_bnb_address_prefix(network: NetworkType) -> str:
    """
    Get address prefix based on the network.
    :param network:
    :return: string address prefix
    """
    if network == NetworkType.TESTNET:
        return 'tbnb'
    elif network == NetworkType.STAGENET:
        return 'bnb'
    elif network == NetworkType.MAINNET:
        return 'bnb'
    else:
        raise ValueError('Invalid network')

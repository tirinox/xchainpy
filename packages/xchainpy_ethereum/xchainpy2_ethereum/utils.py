import json
import logging
import os
import re

import web3

from xchainpy2_utils import NetworkType

SELF_DIR = os.path.dirname(os.path.abspath(__file__))

MAX_APPROVAL = 2 ** 256 - 1


def get_erc20_abi():
    with open(f'{SELF_DIR}/abi/erc20.json', 'r') as f:
        return json.load(f)


def get_router_abi():
    with open(f'{SELF_DIR}/abi/router.json', 'r') as f:
        return json.load(f)


def is_valid_eth_address(address):
    if not isinstance(address, str):
        return False

    if not re.match(r'^0x[a-fA-F0-9]{40}$', address):
        return False

    # Checksum validation
    if address != web3.Web3.to_checksum_address(address):
        return False

    return True


def select_random_free_provider(network: NetworkType, source):
    import random
    provider_url = random.choice(source[network])
    logging.warning(f"Auto selected free RPC provider: {provider_url}. "
                    f"Please consider using your own provider for better performance and security.")

    if provider_url.startswith("ws"):
        provider = web3.providers.WebsocketProvider(provider_url)
    else:
        provider = web3.providers.HTTPProvider(provider_url)

    return provider


class EVMCallError(Exception):
    pass


def validated_checksum_address(web3, address: str) -> str:
    """
    This function validates and returns a checksum address.
    In case the address is in uppercase, that means it probably came from THORChain or other similar AMM.
    it converts it to checksum address.
    Otherwise, it validates the address and returns it.
    :param web3:
    :param address:
    :return:
    """
    if not address:
        raise ValueError("Address is required")
    if address.isupper():  # if it is in uppercase, that means it probably came from THORChain or other similar AMM
        address = web3.to_checksum_address(address)
    if not is_valid_eth_address(address):
        raise ValueError(f'Invalid address: {address}')
    return address

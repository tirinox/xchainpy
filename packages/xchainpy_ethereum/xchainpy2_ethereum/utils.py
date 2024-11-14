import json
import logging
import re

import web3
from web3.main import BaseWeb3

from xchainpy2_utils import NetworkType
from .const import ROUTER_ABI_FILE, ERC20_ABI_FILE


def get_erc20_abi():
    """
    Loads and returns standard ERC20 token ABI as a Python dictionary
    See: https://eips.ethereum.org/EIPS/eip-20

    :return: dict
    """
    with open(ERC20_ABI_FILE, 'r') as f:
        return json.load(f)


def get_router_abi():
    """
    Loads and returns ABI of the THORChain router v4 as a Python dictionary
    See: https://dev.thorchain.org/protocol-development/chain-clients/evm-chains.html?highlight=router#router

    :return: dict
    """
    with open(ROUTER_ABI_FILE, 'r') as f:
        return json.load(f)


def is_valid_eth_address(address):
    """
    Validates Ethereum address, including checksum validation

    :param address: Ethereum address to be validated
    :return: bool
    """
    if not isinstance(address, str):
        return False

    if not re.match(r'^0x[a-fA-F0-9]{40}$', address):
        return False

    # Checksum validation
    if address != web3.Web3.to_checksum_address(address):
        return False

    return True


def select_random_free_provider(network: NetworkType, source: dict) -> web3.providers.BaseProvider:
    """
    Selects a random free RPC provider from the source list

    :param network: Type of network
    :type network: NetworkType
    :param source: Dictionary of free RPC providers grouped by network
    :return: Web3 provider instance
    :rtype web3.providers.BaseProvider
    """
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
    """
    This kind of exception is raised when there are issues with Web3 provider communication
    """
    pass


def validated_checksum_address(web3_pr: BaseWeb3, address: str) -> str:
    """
    This function validates and returns a checksum address.
    In case the address is in uppercase, that means it probably came from THORChain or other similar AMM.
    it converts it to checksum address.
    Otherwise, it validates the address and returns it.

    :param web3_pr: Web3 instance
    :type web3_pr: BaseWeb3
    :param address: EVM Address to be validated
    :return: Validated checksum address
    :rtype: str
    """
    if not address:
        raise ValueError("Address is required")
    if address.isupper():  # if it is in uppercase, that means it probably came from THORChain or other similar AMM
        address = web3_pr.to_checksum_address(address)
    if not is_valid_eth_address(address):
        raise ValueError(f'Invalid address: {address}')
    return address

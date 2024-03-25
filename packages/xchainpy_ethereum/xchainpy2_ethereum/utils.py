import json
import re

import web3


def get_erc20_abi():
    with open('abi/erc20.json', 'r') as f:
        return json.load(f)


def get_router_abi():
    with open('abi/router.json', 'r') as f:
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

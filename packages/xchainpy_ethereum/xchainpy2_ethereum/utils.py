import json
import logging
import os
import re
from functools import reduce
from operator import attrgetter, itemgetter

import web3

from xchainpy2_client import Fees, FeeType, FeeOption
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

def mean_fee(items):
    return wei_to_gwei(round(reduce(lambda a, v: a + v, items) / len(items)))


def wei_to_gwei(wei):
    return web3.Web3.from_wei(wei, 'gwei')


# noinspection PyProtectedMember
def estimate_fees(w3: web3.Web3, percentiles=(20, 50, 80), block_count=20):
    fee_history = w3.eth.fee_history(block_count, 'pending', list(percentiles))
    reward_history = fee_history['reward']

    lo, mi, hi = [
        list(map(itemgetter(i), reward_history)) for i in range(3)
    ]

    # noinspection PyUnresolvedReferences
    base_fee = w3.eth.get_block('pending').baseFeePerGas
    max_priority_fee = w3.eth.max_priority_fee + base_fee

    hi, mi, lo = mean_fee(hi), mean_fee(mi), mean_fee(lo)

    return Fees(
        FeeType.PER_BYTE,
        fees={
            FeeOption._ETH_MAX_FEE: max_priority_fee,
            FeeOption._ETH_BASE_FEE: base_fee,
            FeeOption.FASTEST: hi + base_fee,
            FeeOption.FAST: mi + base_fee,
            FeeOption.AVERAGE: lo + base_fee
        }
    )


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

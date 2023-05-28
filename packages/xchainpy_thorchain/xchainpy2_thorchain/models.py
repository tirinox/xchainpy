from typing import NamedTuple, Dict

from xchainpy2_utils import NetworkType


class NodeURL(NamedTuple):
    node: str
    rpc: str



from typing import NamedTuple, Dict

from xchainpy2_client import ExplorerProvider
from xchainpy2_utils import NetworkType


class NodeURL(NamedTuple):
    node: str
    rpc: str


ExplorerProviders = Dict[NetworkType, ExplorerProvider]

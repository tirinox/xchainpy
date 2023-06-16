from typing import NamedTuple, Dict, Callable, Optional

from xchainpy2_client import ExplorerProvider
from xchainpy2_utils import NetworkType


class NodeURL(NamedTuple):
    node: str
    rpc: str


ExplorerProviders = Dict[NetworkType, ExplorerProvider]


class RPCTxResultInner(NamedTuple):
    code: int
    data: str
    log: str
    info: str
    gas_wanted: str
    gas_used: str
    events: list
    codespace: str


class RPCTxResult(NamedTuple):
    hash: str
    height: int
    index: int
    tx_results: RPCTxResultInner
    tx: str


ThorTxFilterFunc = Optional[Callable[[RPCTxResult], bool]]

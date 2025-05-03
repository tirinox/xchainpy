from typing import NamedTuple, Dict

from xchainpy2_client import ExplorerProvider
from xchainpy2_utils import NetworkType


class NodeURL(NamedTuple):
    node: str
    rpc: str = ''

    @classmethod
    def from_ip_address(cls, ip_address: str, thornode_port: int, rpc_port: int, protocol='http'):
        return cls(
            f'{protocol}://{ip_address}:{thornode_port}',
            f'{protocol}://{ip_address}:{rpc_port}',
        )


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

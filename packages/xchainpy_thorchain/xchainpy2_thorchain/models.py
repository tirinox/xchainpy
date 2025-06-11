from typing import NamedTuple


class NodeURL(NamedTuple):
    node: str
    rpc: str = ''

    @classmethod
    def from_ip_address(cls, ip_address: str, thornode_port: int, rpc_port: int, protocol='http'):
        return cls(
            f'{protocol}://{ip_address}:{thornode_port}',
            f'{protocol}://{ip_address}:{rpc_port}',
        )

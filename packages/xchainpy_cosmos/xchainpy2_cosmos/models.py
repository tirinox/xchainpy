from collections import defaultdict
from typing import NamedTuple, Optional, List


def load_logs(j_logs):
    return [TxLog.from_rpc_json(log) for log in j_logs]


class TxResponse(NamedTuple):
    height: int
    txhash: str
    data: str
    raw_log: str
    logs: list
    gas_wanted: str
    gas_used: str
    tx: Optional[dict]
    timestamp: str

    @classmethod
    def from_rpc_json(cls, j):
        return cls(
            int(j['height']),
            j['txhash'],
            j['data'],
            j['raw_log'],
            load_logs(j['logs']),
            j['gas_wanted'],
            j['gas_used'],
            j['tx'],
            j['timestamp']
        )


class TxHistoryResponse(NamedTuple):
    page_number: int
    page_total: int
    limit: int
    total: int
    tx_responses: List[TxResponse]
    txs: List[dict]

    @classmethod
    def from_rpc_json(cls, j):
        total = int(j['pagination']['total'])
        return cls(
            total=total,
            tx_responses=[TxResponse.from_rpc_json(tx) for tx in j['tx_responses']],
            txs=j['txs'],
            page_number=1,
            page_total=1,
            limit=total
        )


class TxEventAttribute(NamedTuple):
    key: str
    value: str

    @classmethod
    def from_rpc_json(cls, j):
        return cls(
            j['key'],
            j['value']
        )


class TxEvent(NamedTuple):
    type: str
    attributes: List[TxEventAttribute]

    @classmethod
    def from_rpc_json(cls, j):
        return cls(
            j['type'],
            [TxEventAttribute.from_rpc_json(attr) for attr in j['attributes']]
        )

    def find_attributes(self, key):
        return (a for a in self.attributes if a.key == key)

    def find_attr_value_first(self, key, default=None) -> Optional[str]:
        attr = next(self.find_attributes(key), None)
        return attr.value if attr else default

    @property
    def as_dict_of_list(self):
        groups = defaultdict(list)
        for attr in self.attributes:
            groups[attr.key].append(attr.value)
        return groups

    @property
    def as_dict(self):
        return {attr.key: attr.value for attr in self.attributes}


class TxLog(NamedTuple):
    msg_index: int
    log: str
    events: List[TxEvent]

    @classmethod
    def from_rpc_json(cls, j):
        return cls(
            j['msg_index'],
            j['log'],
            [TxEvent.from_rpc_json(event) for event in j['events']]
        )

    def find_events(self, event_name) -> List[TxEvent]:
        return [e for e in self.events if e.type == event_name]

    def find_event(self, event_name):
        return next((e for e in self.events if e.type == event_name), None)


class RPCResponse(NamedTuple):
    jsonrpc: str
    id: int
    result: dict

    @classmethod
    def from_rpc_json(cls, j):
        return cls(
            j['jsonrpc'],
            j['id'],
            j['result']
        )


class TxLoadException(Exception):
    pass


class TxInternalException(Exception):
    pass

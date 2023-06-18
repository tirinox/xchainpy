from typing import NamedTuple, Optional, List


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
            j['height'],
            j['txhash'],
            j['data'],
            j['raw_log'],
            [TxLog.from_rpc_json(log) for log in j['logs']],
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

from typing import NamedTuple, Optional, List


class TxResponse(NamedTuple):
    height: int
    txhash: int
    data: str
    raw_log: str
    logs: list
    gas_wanted: str
    gas_used: str
    tx: Optional[dict]
    timestamp: str


class TxHistoryResponse(NamedTuple):
    page_number: int
    page_total: int
    limit: int
    pagination: dict
    tx_responses: List[TxResponse]


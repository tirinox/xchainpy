import datetime
import json

from xchainpy2_client import TxType
from xchainpy2_cosmos import RPCResponse, TxResponse
from xchainpy2_cosmos.utils import parse_tx_response
from xchainpy2_thorchain import DENOM_RUNE_NATIVE
from xchainpy2_utils import AssetRUNE, RUNE_DECIMAL, Amount


def test_rpc_response():
    r = RPCResponse.from_rpc_json({
        "jsonrpc": "foo",
        "id": 100,
        "result": "good"
    })
    assert r.result == "good"
    assert r.id == 100
    assert r.jsonrpc == "foo"


def test_parse_tx_response():
    txhash = '40BD2FCF41252AD7EAEE313989DC9CB10A120CD384804DD0E9D87F1B388243BB'
    with open(f'./samples/{txhash}.json') as f:
        raw_json = json.load(f)

    xctx = parse_tx_response(
        TxResponse.from_rpc_json(raw_json['tx_response']),
        AssetRUNE,
        DENOM_RUNE_NATIVE,
        RUNE_DECIMAL
    )
    assert xctx.asset == AssetRUNE
    assert xctx.hash == txhash
    assert xctx.height == 11646005
    assert xctx.type == TxType.TRANSFER
    assert xctx.date == datetime.datetime(2023, 7, 10, 15, 49, 56)
    assert len(xctx.from_txs) == 1
    assert len(xctx.to_txs) == 1

    from0, to0 = xctx.from_txs[0], xctx.to_txs[0]

    assert from0.from_address == 'thor1uz4fpyd5f5d6p9pzk8lxyj4qxnwq6f9utg0e7k'
    assert from0.amount == Amount.from_base(978173200000, RUNE_DECIMAL)

    assert to0.address == 'thor1t60f02r8jvzjrhtnjgfj4ne6rs5wjnejwmj7fh'
    assert to0.amount == Amount.from_base(978173200000, RUNE_DECIMAL)
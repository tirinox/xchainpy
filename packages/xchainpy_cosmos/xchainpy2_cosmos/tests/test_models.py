from xchainpy2_cosmos import RPCResponse
from xchainpy2_utils.testing_utils import load_example_json


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
    tx_hash = '40BD2FCF41252AD7EAEE313989DC9CB10A120CD384804DD0E9D87F1B388243BB'
    raw_json = load_example_json(__file__, f'samples/{tx_hash}.json')

    # assert xctx.asset == AssetRUNE
    # assert xctx.hash == tx_hash
    # assert xctx.height == 11646005
    # assert xctx.type == TxType.TRANSFER
    # assert xctx.date == datetime.datetime(2023, 7, 10, 15, 49, 56)
    #
    # todo
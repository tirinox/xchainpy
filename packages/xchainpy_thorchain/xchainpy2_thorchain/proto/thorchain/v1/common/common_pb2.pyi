from gogoproto import gogo_pb2 as _gogo_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Asset(_message.Message):
    __slots__ = ("chain", "symbol", "ticker", "synth", "trade")
    CHAIN_FIELD_NUMBER: _ClassVar[int]
    SYMBOL_FIELD_NUMBER: _ClassVar[int]
    TICKER_FIELD_NUMBER: _ClassVar[int]
    SYNTH_FIELD_NUMBER: _ClassVar[int]
    TRADE_FIELD_NUMBER: _ClassVar[int]
    chain: str
    symbol: str
    ticker: str
    synth: bool
    trade: bool
    def __init__(self, chain: _Optional[str] = ..., symbol: _Optional[str] = ..., ticker: _Optional[str] = ..., synth: bool = ..., trade: bool = ...) -> None: ...

class Coin(_message.Message):
    __slots__ = ("asset", "amount", "decimals")
    ASSET_FIELD_NUMBER: _ClassVar[int]
    AMOUNT_FIELD_NUMBER: _ClassVar[int]
    DECIMALS_FIELD_NUMBER: _ClassVar[int]
    asset: Asset
    amount: str
    decimals: int
    def __init__(self, asset: _Optional[_Union[Asset, _Mapping]] = ..., amount: _Optional[str] = ..., decimals: _Optional[int] = ...) -> None: ...

class PubKeySet(_message.Message):
    __slots__ = ("secp256k1", "ed25519")
    SECP256K1_FIELD_NUMBER: _ClassVar[int]
    ED25519_FIELD_NUMBER: _ClassVar[int]
    secp256k1: str
    ed25519: str
    def __init__(self, secp256k1: _Optional[str] = ..., ed25519: _Optional[str] = ...) -> None: ...

class Tx(_message.Message):
    __slots__ = ("id", "chain", "from_address", "to_address", "coins", "gas", "memo")
    ID_FIELD_NUMBER: _ClassVar[int]
    CHAIN_FIELD_NUMBER: _ClassVar[int]
    FROM_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    TO_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    COINS_FIELD_NUMBER: _ClassVar[int]
    GAS_FIELD_NUMBER: _ClassVar[int]
    MEMO_FIELD_NUMBER: _ClassVar[int]
    id: str
    chain: str
    from_address: str
    to_address: str
    coins: _containers.RepeatedCompositeFieldContainer[Coin]
    gas: _containers.RepeatedCompositeFieldContainer[Coin]
    memo: str
    def __init__(self, id: _Optional[str] = ..., chain: _Optional[str] = ..., from_address: _Optional[str] = ..., to_address: _Optional[str] = ..., coins: _Optional[_Iterable[_Union[Coin, _Mapping]]] = ..., gas: _Optional[_Iterable[_Union[Coin, _Mapping]]] = ..., memo: _Optional[str] = ...) -> None: ...

class Fee(_message.Message):
    __slots__ = ("coins", "pool_deduct")
    COINS_FIELD_NUMBER: _ClassVar[int]
    POOL_DEDUCT_FIELD_NUMBER: _ClassVar[int]
    coins: _containers.RepeatedCompositeFieldContainer[Coin]
    pool_deduct: str
    def __init__(self, coins: _Optional[_Iterable[_Union[Coin, _Mapping]]] = ..., pool_deduct: _Optional[str] = ...) -> None: ...

class ProtoUint(_message.Message):
    __slots__ = ("value",)
    VALUE_FIELD_NUMBER: _ClassVar[int]
    value: str
    def __init__(self, value: _Optional[str] = ...) -> None: ...

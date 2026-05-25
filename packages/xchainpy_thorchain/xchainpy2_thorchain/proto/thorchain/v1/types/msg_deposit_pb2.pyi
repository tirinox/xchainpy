from common import common_pb2 as _common_pb2
from gogoproto import gogo_pb2 as _gogo_pb2
from amino import amino_pb2 as _amino_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class MsgDeposit(_message.Message):
    __slots__ = ("coins", "memo", "signer", "salt")
    COINS_FIELD_NUMBER: _ClassVar[int]
    MEMO_FIELD_NUMBER: _ClassVar[int]
    SIGNER_FIELD_NUMBER: _ClassVar[int]
    SALT_FIELD_NUMBER: _ClassVar[int]
    coins: _containers.RepeatedCompositeFieldContainer[_common_pb2.Coin]
    memo: str
    signer: bytes
    salt: bytes
    def __init__(self, coins: _Optional[_Iterable[_Union[_common_pb2.Coin, _Mapping]]] = ..., memo: _Optional[str] = ..., signer: _Optional[bytes] = ..., salt: _Optional[bytes] = ...) -> None: ...

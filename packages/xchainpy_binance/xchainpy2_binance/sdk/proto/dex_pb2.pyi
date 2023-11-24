from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class StdTx(_message.Message):
    __slots__ = ["msgs", "signatures", "memo", "source", "data"]
    MSGS_FIELD_NUMBER: _ClassVar[int]
    SIGNATURES_FIELD_NUMBER: _ClassVar[int]
    MEMO_FIELD_NUMBER: _ClassVar[int]
    SOURCE_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    msgs: _containers.RepeatedScalarFieldContainer[bytes]
    signatures: _containers.RepeatedScalarFieldContainer[bytes]
    memo: str
    source: int
    data: bytes
    def __init__(self, msgs: _Optional[_Iterable[bytes]] = ..., signatures: _Optional[_Iterable[bytes]] = ..., memo: _Optional[str] = ..., source: _Optional[int] = ..., data: _Optional[bytes] = ...) -> None: ...

class StdSignature(_message.Message):
    __slots__ = ["pub_key", "signature", "account_number", "sequence"]
    class PubKey(_message.Message):
        __slots__ = []
        def __init__(self) -> None: ...
    PUB_KEY_FIELD_NUMBER: _ClassVar[int]
    SIGNATURE_FIELD_NUMBER: _ClassVar[int]
    ACCOUNT_NUMBER_FIELD_NUMBER: _ClassVar[int]
    SEQUENCE_FIELD_NUMBER: _ClassVar[int]
    pub_key: bytes
    signature: bytes
    account_number: int
    sequence: int
    def __init__(self, pub_key: _Optional[bytes] = ..., signature: _Optional[bytes] = ..., account_number: _Optional[int] = ..., sequence: _Optional[int] = ...) -> None: ...

class NewOrder(_message.Message):
    __slots__ = ["sender", "id", "symbol", "ordertype", "side", "price", "quantity", "timeinforce"]
    SENDER_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    SYMBOL_FIELD_NUMBER: _ClassVar[int]
    ORDERTYPE_FIELD_NUMBER: _ClassVar[int]
    SIDE_FIELD_NUMBER: _ClassVar[int]
    PRICE_FIELD_NUMBER: _ClassVar[int]
    QUANTITY_FIELD_NUMBER: _ClassVar[int]
    TIMEINFORCE_FIELD_NUMBER: _ClassVar[int]
    sender: bytes
    id: str
    symbol: str
    ordertype: int
    side: int
    price: int
    quantity: int
    timeinforce: int
    def __init__(self, sender: _Optional[bytes] = ..., id: _Optional[str] = ..., symbol: _Optional[str] = ..., ordertype: _Optional[int] = ..., side: _Optional[int] = ..., price: _Optional[int] = ..., quantity: _Optional[int] = ..., timeinforce: _Optional[int] = ...) -> None: ...

class CancelOrder(_message.Message):
    __slots__ = ["sender", "symbol", "refid"]
    SENDER_FIELD_NUMBER: _ClassVar[int]
    SYMBOL_FIELD_NUMBER: _ClassVar[int]
    REFID_FIELD_NUMBER: _ClassVar[int]
    sender: bytes
    symbol: str
    refid: str
    def __init__(self, sender: _Optional[bytes] = ..., symbol: _Optional[str] = ..., refid: _Optional[str] = ...) -> None: ...

class TokenFreeze(_message.Message):
    __slots__ = ["symbol", "amount"]
    FROM_FIELD_NUMBER: _ClassVar[int]
    SYMBOL_FIELD_NUMBER: _ClassVar[int]
    AMOUNT_FIELD_NUMBER: _ClassVar[int]
    symbol: str
    amount: int
    def __init__(self, symbol: _Optional[str] = ..., amount: _Optional[int] = ..., **kwargs) -> None: ...

class TokenUnfreeze(_message.Message):
    __slots__ = ["symbol", "amount"]
    FROM_FIELD_NUMBER: _ClassVar[int]
    SYMBOL_FIELD_NUMBER: _ClassVar[int]
    AMOUNT_FIELD_NUMBER: _ClassVar[int]
    symbol: str
    amount: int
    def __init__(self, symbol: _Optional[str] = ..., amount: _Optional[int] = ..., **kwargs) -> None: ...

class Send(_message.Message):
    __slots__ = ["inputs", "outputs"]
    class Token(_message.Message):
        __slots__ = ["denom", "amount"]
        DENOM_FIELD_NUMBER: _ClassVar[int]
        AMOUNT_FIELD_NUMBER: _ClassVar[int]
        denom: str
        amount: int
        def __init__(self, denom: _Optional[str] = ..., amount: _Optional[int] = ...) -> None: ...
    class Input(_message.Message):
        __slots__ = ["address", "coins"]
        ADDRESS_FIELD_NUMBER: _ClassVar[int]
        COINS_FIELD_NUMBER: _ClassVar[int]
        address: bytes
        coins: _containers.RepeatedCompositeFieldContainer[Send.Token]
        def __init__(self, address: _Optional[bytes] = ..., coins: _Optional[_Iterable[_Union[Send.Token, _Mapping]]] = ...) -> None: ...
    class Output(_message.Message):
        __slots__ = ["address", "coins"]
        ADDRESS_FIELD_NUMBER: _ClassVar[int]
        COINS_FIELD_NUMBER: _ClassVar[int]
        address: bytes
        coins: _containers.RepeatedCompositeFieldContainer[Send.Token]
        def __init__(self, address: _Optional[bytes] = ..., coins: _Optional[_Iterable[_Union[Send.Token, _Mapping]]] = ...) -> None: ...
    INPUTS_FIELD_NUMBER: _ClassVar[int]
    OUTPUTS_FIELD_NUMBER: _ClassVar[int]
    inputs: _containers.RepeatedCompositeFieldContainer[Send.Input]
    outputs: _containers.RepeatedCompositeFieldContainer[Send.Output]
    def __init__(self, inputs: _Optional[_Iterable[_Union[Send.Input, _Mapping]]] = ..., outputs: _Optional[_Iterable[_Union[Send.Output, _Mapping]]] = ...) -> None: ...

class Vote(_message.Message):
    __slots__ = ["proposal_id", "voter", "option"]
    PROPOSAL_ID_FIELD_NUMBER: _ClassVar[int]
    VOTER_FIELD_NUMBER: _ClassVar[int]
    OPTION_FIELD_NUMBER: _ClassVar[int]
    proposal_id: int
    voter: bytes
    option: int
    def __init__(self, proposal_id: _Optional[int] = ..., voter: _Optional[bytes] = ..., option: _Optional[int] = ...) -> None: ...

class SideVote(_message.Message):
    __slots__ = ["proposal_id", "voter", "option", "side_chain_id"]
    PROPOSAL_ID_FIELD_NUMBER: _ClassVar[int]
    VOTER_FIELD_NUMBER: _ClassVar[int]
    OPTION_FIELD_NUMBER: _ClassVar[int]
    SIDE_CHAIN_ID_FIELD_NUMBER: _ClassVar[int]
    proposal_id: int
    voter: bytes
    option: int
    side_chain_id: str
    def __init__(self, proposal_id: _Optional[int] = ..., voter: _Optional[bytes] = ..., option: _Optional[int] = ..., side_chain_id: _Optional[str] = ...) -> None: ...

class Token(_message.Message):
    __slots__ = ["denom", "amount"]
    DENOM_FIELD_NUMBER: _ClassVar[int]
    AMOUNT_FIELD_NUMBER: _ClassVar[int]
    denom: str
    amount: int
    def __init__(self, denom: _Optional[str] = ..., amount: _Optional[int] = ...) -> None: ...

class AppAccount(_message.Message):
    __slots__ = ["base", "name", "frozen", "locked"]
    class baseAccount(_message.Message):
        __slots__ = ["address", "coins", "public_key", "account_number", "sequence"]
        ADDRESS_FIELD_NUMBER: _ClassVar[int]
        COINS_FIELD_NUMBER: _ClassVar[int]
        PUBLIC_KEY_FIELD_NUMBER: _ClassVar[int]
        ACCOUNT_NUMBER_FIELD_NUMBER: _ClassVar[int]
        SEQUENCE_FIELD_NUMBER: _ClassVar[int]
        address: bytes
        coins: _containers.RepeatedCompositeFieldContainer[Token]
        public_key: bytes
        account_number: int
        sequence: int
        def __init__(self, address: _Optional[bytes] = ..., coins: _Optional[_Iterable[_Union[Token, _Mapping]]] = ..., public_key: _Optional[bytes] = ..., account_number: _Optional[int] = ..., sequence: _Optional[int] = ...) -> None: ...
    BASE_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    FROZEN_FIELD_NUMBER: _ClassVar[int]
    LOCKED_FIELD_NUMBER: _ClassVar[int]
    base: AppAccount.baseAccount
    name: str
    frozen: _containers.RepeatedCompositeFieldContainer[Token]
    locked: _containers.RepeatedCompositeFieldContainer[Token]
    def __init__(self, base: _Optional[_Union[AppAccount.baseAccount, _Mapping]] = ..., name: _Optional[str] = ..., frozen: _Optional[_Iterable[_Union[Token, _Mapping]]] = ..., locked: _Optional[_Iterable[_Union[Token, _Mapping]]] = ...) -> None: ...

class AtomicSwapInfo(_message.Message):
    __slots__ = ["to", "out_amount", "in_amount", "expected_income", "recipient_other_chain", "random_number_hash", "random_number", "timestamp", "cross_chain", "expire_height", "index", "closed_time", "status"]
    FROM_FIELD_NUMBER: _ClassVar[int]
    TO_FIELD_NUMBER: _ClassVar[int]
    OUT_AMOUNT_FIELD_NUMBER: _ClassVar[int]
    IN_AMOUNT_FIELD_NUMBER: _ClassVar[int]
    EXPECTED_INCOME_FIELD_NUMBER: _ClassVar[int]
    RECIPIENT_OTHER_CHAIN_FIELD_NUMBER: _ClassVar[int]
    RANDOM_NUMBER_HASH_FIELD_NUMBER: _ClassVar[int]
    RANDOM_NUMBER_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    CROSS_CHAIN_FIELD_NUMBER: _ClassVar[int]
    EXPIRE_HEIGHT_FIELD_NUMBER: _ClassVar[int]
    INDEX_FIELD_NUMBER: _ClassVar[int]
    CLOSED_TIME_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    to: bytes
    out_amount: _containers.RepeatedCompositeFieldContainer[Token]
    in_amount: _containers.RepeatedCompositeFieldContainer[Token]
    expected_income: str
    recipient_other_chain: bytes
    random_number_hash: bytes
    random_number: bytes
    timestamp: int
    cross_chain: bool
    expire_height: int
    index: int
    closed_time: int
    status: int
    def __init__(self, to: _Optional[bytes] = ..., out_amount: _Optional[_Iterable[_Union[Token, _Mapping]]] = ..., in_amount: _Optional[_Iterable[_Union[Token, _Mapping]]] = ..., expected_income: _Optional[str] = ..., recipient_other_chain: _Optional[bytes] = ..., random_number_hash: _Optional[bytes] = ..., random_number: _Optional[bytes] = ..., timestamp: _Optional[int] = ..., cross_chain: bool = ..., expire_height: _Optional[int] = ..., index: _Optional[int] = ..., closed_time: _Optional[int] = ..., status: _Optional[int] = ..., **kwargs) -> None: ...

class TokenInfo(_message.Message):
    __slots__ = ["name", "symbol", "original_symbol", "total_supply", "owner", "mintable"]
    NAME_FIELD_NUMBER: _ClassVar[int]
    SYMBOL_FIELD_NUMBER: _ClassVar[int]
    ORIGINAL_SYMBOL_FIELD_NUMBER: _ClassVar[int]
    TOTAL_SUPPLY_FIELD_NUMBER: _ClassVar[int]
    OWNER_FIELD_NUMBER: _ClassVar[int]
    MINTABLE_FIELD_NUMBER: _ClassVar[int]
    name: str
    symbol: str
    original_symbol: str
    total_supply: int
    owner: bytes
    mintable: bool
    def __init__(self, name: _Optional[str] = ..., symbol: _Optional[str] = ..., original_symbol: _Optional[str] = ..., total_supply: _Optional[int] = ..., owner: _Optional[bytes] = ..., mintable: bool = ...) -> None: ...

class MiniTokenInfo(_message.Message):
    __slots__ = ["name", "symbol", "original_symbol", "total_supply", "owner", "mintable", "token_type", "token_uri"]
    NAME_FIELD_NUMBER: _ClassVar[int]
    SYMBOL_FIELD_NUMBER: _ClassVar[int]
    ORIGINAL_SYMBOL_FIELD_NUMBER: _ClassVar[int]
    TOTAL_SUPPLY_FIELD_NUMBER: _ClassVar[int]
    OWNER_FIELD_NUMBER: _ClassVar[int]
    MINTABLE_FIELD_NUMBER: _ClassVar[int]
    TOKEN_TYPE_FIELD_NUMBER: _ClassVar[int]
    TOKEN_URI_FIELD_NUMBER: _ClassVar[int]
    name: str
    symbol: str
    original_symbol: str
    total_supply: int
    owner: bytes
    mintable: bool
    token_type: int
    token_uri: str
    def __init__(self, name: _Optional[str] = ..., symbol: _Optional[str] = ..., original_symbol: _Optional[str] = ..., total_supply: _Optional[int] = ..., owner: _Optional[bytes] = ..., mintable: bool = ..., token_type: _Optional[int] = ..., token_uri: _Optional[str] = ...) -> None: ...

class DexFeeParam(_message.Message):
    __slots__ = ["dex_fee_fields"]
    class DexFeeField(_message.Message):
        __slots__ = ["fee_name", "fee_value"]
        FEE_NAME_FIELD_NUMBER: _ClassVar[int]
        FEE_VALUE_FIELD_NUMBER: _ClassVar[int]
        fee_name: str
        fee_value: int
        def __init__(self, fee_name: _Optional[str] = ..., fee_value: _Optional[int] = ...) -> None: ...
    DEX_FEE_FIELDS_FIELD_NUMBER: _ClassVar[int]
    dex_fee_fields: _containers.RepeatedCompositeFieldContainer[DexFeeParam.DexFeeField]
    def __init__(self, dex_fee_fields: _Optional[_Iterable[_Union[DexFeeParam.DexFeeField, _Mapping]]] = ...) -> None: ...

class FixedFeeParams(_message.Message):
    __slots__ = ["msg_type", "fee", "fee_for"]
    MSG_TYPE_FIELD_NUMBER: _ClassVar[int]
    FEE_FIELD_NUMBER: _ClassVar[int]
    FEE_FOR_FIELD_NUMBER: _ClassVar[int]
    msg_type: str
    fee: int
    fee_for: int
    def __init__(self, msg_type: _Optional[str] = ..., fee: _Optional[int] = ..., fee_for: _Optional[int] = ...) -> None: ...

class TransferFeeParam(_message.Message):
    __slots__ = ["fixed_fee_params", "multi_transfer_fee", "lower_limit_as_multi"]
    FIXED_FEE_PARAMS_FIELD_NUMBER: _ClassVar[int]
    MULTI_TRANSFER_FEE_FIELD_NUMBER: _ClassVar[int]
    LOWER_LIMIT_AS_MULTI_FIELD_NUMBER: _ClassVar[int]
    fixed_fee_params: FixedFeeParams
    multi_transfer_fee: int
    lower_limit_as_multi: int
    def __init__(self, fixed_fee_params: _Optional[_Union[FixedFeeParams, _Mapping]] = ..., multi_transfer_fee: _Optional[int] = ..., lower_limit_as_multi: _Optional[int] = ...) -> None: ...

class ResultBroadcastTx(_message.Message):
    __slots__ = ["code", "data", "log", "hash"]
    CODE_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    LOG_FIELD_NUMBER: _ClassVar[int]
    HASH_FIELD_NUMBER: _ClassVar[int]
    code: int
    data: bytes
    log: str
    hash: bytes
    def __init__(self, code: _Optional[int] = ..., data: _Optional[bytes] = ..., log: _Optional[str] = ..., hash: _Optional[bytes] = ...) -> None: ...

class Issue(_message.Message):
    __slots__ = ["name", "symbol", "total_supply", "mintable"]
    FROM_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    SYMBOL_FIELD_NUMBER: _ClassVar[int]
    TOTAL_SUPPLY_FIELD_NUMBER: _ClassVar[int]
    MINTABLE_FIELD_NUMBER: _ClassVar[int]
    name: str
    symbol: str
    total_supply: int
    mintable: bool
    def __init__(self, name: _Optional[str] = ..., symbol: _Optional[str] = ..., total_supply: _Optional[int] = ..., mintable: bool = ..., **kwargs) -> None: ...

class Burn(_message.Message):
    __slots__ = ["symbol", "amount"]
    FROM_FIELD_NUMBER: _ClassVar[int]
    SYMBOL_FIELD_NUMBER: _ClassVar[int]
    AMOUNT_FIELD_NUMBER: _ClassVar[int]
    symbol: str
    amount: int
    def __init__(self, symbol: _Optional[str] = ..., amount: _Optional[int] = ..., **kwargs) -> None: ...

class Mint(_message.Message):
    __slots__ = ["symbol", "amount"]
    FROM_FIELD_NUMBER: _ClassVar[int]
    SYMBOL_FIELD_NUMBER: _ClassVar[int]
    AMOUNT_FIELD_NUMBER: _ClassVar[int]
    symbol: str
    amount: int
    def __init__(self, symbol: _Optional[str] = ..., amount: _Optional[int] = ..., **kwargs) -> None: ...

class SubmitProposal(_message.Message):
    __slots__ = ["title", "description", "proposal_type", "proposer", "initial_deposit", "voting_period"]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    PROPOSAL_TYPE_FIELD_NUMBER: _ClassVar[int]
    PROPOSER_FIELD_NUMBER: _ClassVar[int]
    INITIAL_DEPOSIT_FIELD_NUMBER: _ClassVar[int]
    VOTING_PERIOD_FIELD_NUMBER: _ClassVar[int]
    title: str
    description: str
    proposal_type: int
    proposer: bytes
    initial_deposit: _containers.RepeatedCompositeFieldContainer[Token]
    voting_period: int
    def __init__(self, title: _Optional[str] = ..., description: _Optional[str] = ..., proposal_type: _Optional[int] = ..., proposer: _Optional[bytes] = ..., initial_deposit: _Optional[_Iterable[_Union[Token, _Mapping]]] = ..., voting_period: _Optional[int] = ...) -> None: ...

class SideSubmitProposal(_message.Message):
    __slots__ = ["title", "description", "proposal_type", "proposer", "initial_deposit", "voting_period", "side_chain_id"]
    TITLE_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    PROPOSAL_TYPE_FIELD_NUMBER: _ClassVar[int]
    PROPOSER_FIELD_NUMBER: _ClassVar[int]
    INITIAL_DEPOSIT_FIELD_NUMBER: _ClassVar[int]
    VOTING_PERIOD_FIELD_NUMBER: _ClassVar[int]
    SIDE_CHAIN_ID_FIELD_NUMBER: _ClassVar[int]
    title: str
    description: str
    proposal_type: int
    proposer: bytes
    initial_deposit: _containers.RepeatedCompositeFieldContainer[Token]
    voting_period: int
    side_chain_id: str
    def __init__(self, title: _Optional[str] = ..., description: _Optional[str] = ..., proposal_type: _Optional[int] = ..., proposer: _Optional[bytes] = ..., initial_deposit: _Optional[_Iterable[_Union[Token, _Mapping]]] = ..., voting_period: _Optional[int] = ..., side_chain_id: _Optional[str] = ...) -> None: ...

class Deposit(_message.Message):
    __slots__ = ["proposal_id", "depositer", "amount"]
    PROPOSAL_ID_FIELD_NUMBER: _ClassVar[int]
    DEPOSITER_FIELD_NUMBER: _ClassVar[int]
    AMOUNT_FIELD_NUMBER: _ClassVar[int]
    proposal_id: int
    depositer: bytes
    amount: _containers.RepeatedCompositeFieldContainer[Token]
    def __init__(self, proposal_id: _Optional[int] = ..., depositer: _Optional[bytes] = ..., amount: _Optional[_Iterable[_Union[Token, _Mapping]]] = ...) -> None: ...

class SideDeposit(_message.Message):
    __slots__ = ["proposal_id", "depositer", "amount", "side_chain_id"]
    PROPOSAL_ID_FIELD_NUMBER: _ClassVar[int]
    DEPOSITER_FIELD_NUMBER: _ClassVar[int]
    AMOUNT_FIELD_NUMBER: _ClassVar[int]
    SIDE_CHAIN_ID_FIELD_NUMBER: _ClassVar[int]
    proposal_id: int
    depositer: bytes
    amount: _containers.RepeatedCompositeFieldContainer[Token]
    side_chain_id: str
    def __init__(self, proposal_id: _Optional[int] = ..., depositer: _Optional[bytes] = ..., amount: _Optional[_Iterable[_Union[Token, _Mapping]]] = ..., side_chain_id: _Optional[str] = ...) -> None: ...

class Description(_message.Message):
    __slots__ = ["moniker", "identity", "website", "details"]
    MONIKER_FIELD_NUMBER: _ClassVar[int]
    IDENTITY_FIELD_NUMBER: _ClassVar[int]
    WEBSITE_FIELD_NUMBER: _ClassVar[int]
    DETAILS_FIELD_NUMBER: _ClassVar[int]
    moniker: str
    identity: str
    website: str
    details: str
    def __init__(self, moniker: _Optional[str] = ..., identity: _Optional[str] = ..., website: _Optional[str] = ..., details: _Optional[str] = ...) -> None: ...

class Commission(_message.Message):
    __slots__ = ["rate", "max_rate", "max_change_rate"]
    RATE_FIELD_NUMBER: _ClassVar[int]
    MAX_RATE_FIELD_NUMBER: _ClassVar[int]
    MAX_CHANGE_RATE_FIELD_NUMBER: _ClassVar[int]
    rate: int
    max_rate: int
    max_change_rate: int
    def __init__(self, rate: _Optional[int] = ..., max_rate: _Optional[int] = ..., max_change_rate: _Optional[int] = ...) -> None: ...

class CreateValidator(_message.Message):
    __slots__ = ["description", "commission", "delegator_address", "validator_address", "pubkey", "delegation"]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    COMMISSION_FIELD_NUMBER: _ClassVar[int]
    DELEGATOR_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    VALIDATOR_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    PUBKEY_FIELD_NUMBER: _ClassVar[int]
    DELEGATION_FIELD_NUMBER: _ClassVar[int]
    description: Description
    commission: Commission
    delegator_address: bytes
    validator_address: bytes
    pubkey: bytes
    delegation: Token
    def __init__(self, description: _Optional[_Union[Description, _Mapping]] = ..., commission: _Optional[_Union[Commission, _Mapping]] = ..., delegator_address: _Optional[bytes] = ..., validator_address: _Optional[bytes] = ..., pubkey: _Optional[bytes] = ..., delegation: _Optional[_Union[Token, _Mapping]] = ...) -> None: ...

class RealCreateValidator(_message.Message):
    __slots__ = ["createValidator", "proposal_id"]
    CREATEVALIDATOR_FIELD_NUMBER: _ClassVar[int]
    PROPOSAL_ID_FIELD_NUMBER: _ClassVar[int]
    createValidator: CreateValidator
    proposal_id: int
    def __init__(self, createValidator: _Optional[_Union[CreateValidator, _Mapping]] = ..., proposal_id: _Optional[int] = ...) -> None: ...

class RemoveValidator(_message.Message):
    __slots__ = ["launcher_addr", "val_addr", "val_cons_addr", "proposal_id"]
    LAUNCHER_ADDR_FIELD_NUMBER: _ClassVar[int]
    VAL_ADDR_FIELD_NUMBER: _ClassVar[int]
    VAL_CONS_ADDR_FIELD_NUMBER: _ClassVar[int]
    PROPOSAL_ID_FIELD_NUMBER: _ClassVar[int]
    launcher_addr: bytes
    val_addr: bytes
    val_cons_addr: bytes
    proposal_id: int
    def __init__(self, launcher_addr: _Optional[bytes] = ..., val_addr: _Optional[bytes] = ..., val_cons_addr: _Optional[bytes] = ..., proposal_id: _Optional[int] = ...) -> None: ...

class List(_message.Message):
    __slots__ = ["proposal_id", "base_asset_symbol", "quote_asset_symbol", "init_price"]
    FROM_FIELD_NUMBER: _ClassVar[int]
    PROPOSAL_ID_FIELD_NUMBER: _ClassVar[int]
    BASE_ASSET_SYMBOL_FIELD_NUMBER: _ClassVar[int]
    QUOTE_ASSET_SYMBOL_FIELD_NUMBER: _ClassVar[int]
    INIT_PRICE_FIELD_NUMBER: _ClassVar[int]
    proposal_id: int
    base_asset_symbol: str
    quote_asset_symbol: str
    init_price: int
    def __init__(self, proposal_id: _Optional[int] = ..., base_asset_symbol: _Optional[str] = ..., quote_asset_symbol: _Optional[str] = ..., init_price: _Optional[int] = ..., **kwargs) -> None: ...

class TimeLock(_message.Message):
    __slots__ = ["description", "amount", "lock_time"]
    class Token(_message.Message):
        __slots__ = ["denom", "amount"]
        DENOM_FIELD_NUMBER: _ClassVar[int]
        AMOUNT_FIELD_NUMBER: _ClassVar[int]
        denom: str
        amount: int
        def __init__(self, denom: _Optional[str] = ..., amount: _Optional[int] = ...) -> None: ...
    FROM_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    AMOUNT_FIELD_NUMBER: _ClassVar[int]
    LOCK_TIME_FIELD_NUMBER: _ClassVar[int]
    description: str
    amount: _containers.RepeatedCompositeFieldContainer[TimeLock.Token]
    lock_time: int
    def __init__(self, description: _Optional[str] = ..., amount: _Optional[_Iterable[_Union[TimeLock.Token, _Mapping]]] = ..., lock_time: _Optional[int] = ..., **kwargs) -> None: ...

class TimeUnlock(_message.Message):
    __slots__ = ["time_lock_id"]
    FROM_FIELD_NUMBER: _ClassVar[int]
    TIME_LOCK_ID_FIELD_NUMBER: _ClassVar[int]
    time_lock_id: int
    def __init__(self, time_lock_id: _Optional[int] = ..., **kwargs) -> None: ...

class TimeRelock(_message.Message):
    __slots__ = ["time_lock_id", "description", "amount", "lock_time"]
    class Token(_message.Message):
        __slots__ = ["denom", "amount"]
        DENOM_FIELD_NUMBER: _ClassVar[int]
        AMOUNT_FIELD_NUMBER: _ClassVar[int]
        denom: str
        amount: int
        def __init__(self, denom: _Optional[str] = ..., amount: _Optional[int] = ...) -> None: ...
    FROM_FIELD_NUMBER: _ClassVar[int]
    TIME_LOCK_ID_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    AMOUNT_FIELD_NUMBER: _ClassVar[int]
    LOCK_TIME_FIELD_NUMBER: _ClassVar[int]
    time_lock_id: int
    description: str
    amount: _containers.RepeatedCompositeFieldContainer[TimeRelock.Token]
    lock_time: int
    def __init__(self, time_lock_id: _Optional[int] = ..., description: _Optional[str] = ..., amount: _Optional[_Iterable[_Union[TimeRelock.Token, _Mapping]]] = ..., lock_time: _Optional[int] = ..., **kwargs) -> None: ...

class SetAccountFlag(_message.Message):
    __slots__ = ["flags"]
    FROM_FIELD_NUMBER: _ClassVar[int]
    FLAGS_FIELD_NUMBER: _ClassVar[int]
    flags: int
    def __init__(self, flags: _Optional[int] = ..., **kwargs) -> None: ...

class HashTimerLockTransferMsg(_message.Message):
    __slots__ = ["to", "recipient_other_chain", "sender_other_chain", "random_number_hash", "timestamp", "amount", "expected_income", "height_span", "cross_chain"]
    FROM_FIELD_NUMBER: _ClassVar[int]
    TO_FIELD_NUMBER: _ClassVar[int]
    RECIPIENT_OTHER_CHAIN_FIELD_NUMBER: _ClassVar[int]
    SENDER_OTHER_CHAIN_FIELD_NUMBER: _ClassVar[int]
    RANDOM_NUMBER_HASH_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    AMOUNT_FIELD_NUMBER: _ClassVar[int]
    EXPECTED_INCOME_FIELD_NUMBER: _ClassVar[int]
    HEIGHT_SPAN_FIELD_NUMBER: _ClassVar[int]
    CROSS_CHAIN_FIELD_NUMBER: _ClassVar[int]
    to: bytes
    recipient_other_chain: str
    sender_other_chain: str
    random_number_hash: bytes
    timestamp: int
    amount: _containers.RepeatedCompositeFieldContainer[Token]
    expected_income: str
    height_span: int
    cross_chain: bool
    def __init__(self, to: _Optional[bytes] = ..., recipient_other_chain: _Optional[str] = ..., sender_other_chain: _Optional[str] = ..., random_number_hash: _Optional[bytes] = ..., timestamp: _Optional[int] = ..., amount: _Optional[_Iterable[_Union[Token, _Mapping]]] = ..., expected_income: _Optional[str] = ..., height_span: _Optional[int] = ..., cross_chain: bool = ..., **kwargs) -> None: ...

class DepositHashTimerLockMsg(_message.Message):
    __slots__ = ["amount", "swap_id"]
    FROM_FIELD_NUMBER: _ClassVar[int]
    AMOUNT_FIELD_NUMBER: _ClassVar[int]
    SWAP_ID_FIELD_NUMBER: _ClassVar[int]
    amount: _containers.RepeatedCompositeFieldContainer[Token]
    swap_id: bytes
    def __init__(self, amount: _Optional[_Iterable[_Union[Token, _Mapping]]] = ..., swap_id: _Optional[bytes] = ..., **kwargs) -> None: ...

class ClaimHashTimerLockMsg(_message.Message):
    __slots__ = ["swap_id", "random_number"]
    FROM_FIELD_NUMBER: _ClassVar[int]
    SWAP_ID_FIELD_NUMBER: _ClassVar[int]
    RANDOM_NUMBER_FIELD_NUMBER: _ClassVar[int]
    swap_id: bytes
    random_number: bytes
    def __init__(self, swap_id: _Optional[bytes] = ..., random_number: _Optional[bytes] = ..., **kwargs) -> None: ...

class SubmitEvidenceMsg(_message.Message):
    __slots__ = ["submitter", "headers"]
    SUBMITTER_FIELD_NUMBER: _ClassVar[int]
    HEADERS_FIELD_NUMBER: _ClassVar[int]
    submitter: bytes
    headers: _containers.RepeatedCompositeFieldContainer[BscHeader]
    def __init__(self, submitter: _Optional[bytes] = ..., headers: _Optional[_Iterable[_Union[BscHeader, _Mapping]]] = ...) -> None: ...

class BscHeader(_message.Message):
    __slots__ = ["parentHash", "sha3Uncles", "miner", "stateRoot", "transactionsRoot", "receiptsRoot", "logsBloom", "difficulty", "number", "gasLimit", "gasUsed", "timestamp", "extraData", "mixHash", "nonce"]
    PARENTHASH_FIELD_NUMBER: _ClassVar[int]
    SHA3UNCLES_FIELD_NUMBER: _ClassVar[int]
    MINER_FIELD_NUMBER: _ClassVar[int]
    STATEROOT_FIELD_NUMBER: _ClassVar[int]
    TRANSACTIONSROOT_FIELD_NUMBER: _ClassVar[int]
    RECEIPTSROOT_FIELD_NUMBER: _ClassVar[int]
    LOGSBLOOM_FIELD_NUMBER: _ClassVar[int]
    DIFFICULTY_FIELD_NUMBER: _ClassVar[int]
    NUMBER_FIELD_NUMBER: _ClassVar[int]
    GASLIMIT_FIELD_NUMBER: _ClassVar[int]
    GASUSED_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    EXTRADATA_FIELD_NUMBER: _ClassVar[int]
    MIXHASH_FIELD_NUMBER: _ClassVar[int]
    NONCE_FIELD_NUMBER: _ClassVar[int]
    parentHash: bytes
    sha3Uncles: bytes
    miner: bytes
    stateRoot: bytes
    transactionsRoot: bytes
    receiptsRoot: bytes
    logsBloom: bytes
    difficulty: int
    number: int
    gasLimit: int
    gasUsed: int
    timestamp: int
    extraData: bytes
    mixHash: bytes
    nonce: bytes
    def __init__(self, parentHash: _Optional[bytes] = ..., sha3Uncles: _Optional[bytes] = ..., miner: _Optional[bytes] = ..., stateRoot: _Optional[bytes] = ..., transactionsRoot: _Optional[bytes] = ..., receiptsRoot: _Optional[bytes] = ..., logsBloom: _Optional[bytes] = ..., difficulty: _Optional[int] = ..., number: _Optional[int] = ..., gasLimit: _Optional[int] = ..., gasUsed: _Optional[int] = ..., timestamp: _Optional[int] = ..., extraData: _Optional[bytes] = ..., mixHash: _Optional[bytes] = ..., nonce: _Optional[bytes] = ...) -> None: ...

class SideChainUnJailMsg(_message.Message):
    __slots__ = ["address", "side_chain_id"]
    ADDRESS_FIELD_NUMBER: _ClassVar[int]
    SIDE_CHAIN_ID_FIELD_NUMBER: _ClassVar[int]
    address: bytes
    side_chain_id: str
    def __init__(self, address: _Optional[bytes] = ..., side_chain_id: _Optional[str] = ...) -> None: ...

class RefundHashTimerLockMsg(_message.Message):
    __slots__ = ["swap_id"]
    FROM_FIELD_NUMBER: _ClassVar[int]
    SWAP_ID_FIELD_NUMBER: _ClassVar[int]
    swap_id: bytes
    def __init__(self, swap_id: _Optional[bytes] = ..., **kwargs) -> None: ...

class Status(_message.Message):
    __slots__ = ["text", "finalClaim"]
    TEXT_FIELD_NUMBER: _ClassVar[int]
    FINALCLAIM_FIELD_NUMBER: _ClassVar[int]
    text: int
    finalClaim: str
    def __init__(self, text: _Optional[int] = ..., finalClaim: _Optional[str] = ...) -> None: ...

class Prophecy(_message.Message):
    __slots__ = ["id", "status", "claimValidators", "validatorClaims"]
    class ClaimValidatorsEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: bytes
        def __init__(self, key: _Optional[str] = ..., value: _Optional[bytes] = ...) -> None: ...
    class ValidatorClaimsEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    ID_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    CLAIMVALIDATORS_FIELD_NUMBER: _ClassVar[int]
    VALIDATORCLAIMS_FIELD_NUMBER: _ClassVar[int]
    id: str
    status: Status
    claimValidators: _containers.ScalarMap[str, bytes]
    validatorClaims: _containers.ScalarMap[str, str]
    def __init__(self, id: _Optional[str] = ..., status: _Optional[_Union[Status, _Mapping]] = ..., claimValidators: _Optional[_Mapping[str, bytes]] = ..., validatorClaims: _Optional[_Mapping[str, str]] = ...) -> None: ...

class TinyTokenIssue(_message.Message):
    __slots__ = ["name", "symbol", "total_supply", "mintable", "token_uri"]
    FROM_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    SYMBOL_FIELD_NUMBER: _ClassVar[int]
    TOTAL_SUPPLY_FIELD_NUMBER: _ClassVar[int]
    MINTABLE_FIELD_NUMBER: _ClassVar[int]
    TOKEN_URI_FIELD_NUMBER: _ClassVar[int]
    name: str
    symbol: str
    total_supply: int
    mintable: bool
    token_uri: str
    def __init__(self, name: _Optional[str] = ..., symbol: _Optional[str] = ..., total_supply: _Optional[int] = ..., mintable: bool = ..., token_uri: _Optional[str] = ..., **kwargs) -> None: ...

class MiniTokenIssue(_message.Message):
    __slots__ = ["name", "symbol", "total_supply", "mintable", "token_uri"]
    FROM_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    SYMBOL_FIELD_NUMBER: _ClassVar[int]
    TOTAL_SUPPLY_FIELD_NUMBER: _ClassVar[int]
    MINTABLE_FIELD_NUMBER: _ClassVar[int]
    TOKEN_URI_FIELD_NUMBER: _ClassVar[int]
    name: str
    symbol: str
    total_supply: int
    mintable: bool
    token_uri: str
    def __init__(self, name: _Optional[str] = ..., symbol: _Optional[str] = ..., total_supply: _Optional[int] = ..., mintable: bool = ..., token_uri: _Optional[str] = ..., **kwargs) -> None: ...

class MiniTokenSetURI(_message.Message):
    __slots__ = ["symbol", "token_uri"]
    FROM_FIELD_NUMBER: _ClassVar[int]
    SYMBOL_FIELD_NUMBER: _ClassVar[int]
    TOKEN_URI_FIELD_NUMBER: _ClassVar[int]
    symbol: str
    token_uri: str
    def __init__(self, symbol: _Optional[str] = ..., token_uri: _Optional[str] = ..., **kwargs) -> None: ...

class MiniTokenList(_message.Message):
    __slots__ = ["base_asset_symbol", "quote_asset_symbol", "init_price"]
    FROM_FIELD_NUMBER: _ClassVar[int]
    BASE_ASSET_SYMBOL_FIELD_NUMBER: _ClassVar[int]
    QUOTE_ASSET_SYMBOL_FIELD_NUMBER: _ClassVar[int]
    INIT_PRICE_FIELD_NUMBER: _ClassVar[int]
    base_asset_symbol: str
    quote_asset_symbol: str
    init_price: int
    def __init__(self, base_asset_symbol: _Optional[str] = ..., quote_asset_symbol: _Optional[str] = ..., init_price: _Optional[int] = ..., **kwargs) -> None: ...

class TransferTokenOwnershipMsg(_message.Message):
    __slots__ = ["symbol", "new_owner"]
    FROM_FIELD_NUMBER: _ClassVar[int]
    SYMBOL_FIELD_NUMBER: _ClassVar[int]
    NEW_OWNER_FIELD_NUMBER: _ClassVar[int]
    symbol: str
    new_owner: bytes
    def __init__(self, symbol: _Optional[str] = ..., new_owner: _Optional[bytes] = ..., **kwargs) -> None: ...

class UnJailMsg(_message.Message):
    __slots__ = ["address"]
    ADDRESS_FIELD_NUMBER: _ClassVar[int]
    address: bytes
    def __init__(self, address: _Optional[bytes] = ...) -> None: ...

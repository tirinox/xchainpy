from amino import amino_pb2 as _amino_pb2
from gogoproto import gogo_pb2 as _gogo_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Status(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    incomplete: _ClassVar[Status]
    done: _ClassVar[Status]
    reverted: _ClassVar[Status]
incomplete: Status
done: Status
reverted: Status

class Asset(_message.Message):
    __slots__ = ("chain", "symbol", "ticker", "synth", "trade", "secured")
    CHAIN_FIELD_NUMBER: _ClassVar[int]
    SYMBOL_FIELD_NUMBER: _ClassVar[int]
    TICKER_FIELD_NUMBER: _ClassVar[int]
    SYNTH_FIELD_NUMBER: _ClassVar[int]
    TRADE_FIELD_NUMBER: _ClassVar[int]
    SECURED_FIELD_NUMBER: _ClassVar[int]
    chain: str
    symbol: str
    ticker: str
    synth: bool
    trade: bool
    secured: bool
    def __init__(self, chain: _Optional[str] = ..., symbol: _Optional[str] = ..., ticker: _Optional[str] = ..., synth: bool = ..., trade: bool = ..., secured: bool = ...) -> None: ...

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

class OutputRef(_message.Message):
    __slots__ = ("tx_hash", "output_index", "key_image", "spend_tx_hash")
    TX_HASH_FIELD_NUMBER: _ClassVar[int]
    OUTPUT_INDEX_FIELD_NUMBER: _ClassVar[int]
    KEY_IMAGE_FIELD_NUMBER: _ClassVar[int]
    SPEND_TX_HASH_FIELD_NUMBER: _ClassVar[int]
    tx_hash: str
    output_index: int
    key_image: str
    spend_tx_hash: str
    def __init__(self, tx_hash: _Optional[str] = ..., output_index: _Optional[int] = ..., key_image: _Optional[str] = ..., spend_tx_hash: _Optional[str] = ...) -> None: ...

class ObservedTx(_message.Message):
    __slots__ = ("tx", "status", "out_hashes", "block_height", "signers", "observed_pub_key", "keysign_ms", "finalise_height", "aggregator", "aggregator_target", "aggregator_target_limit", "spent_output_refs")
    TX_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    OUT_HASHES_FIELD_NUMBER: _ClassVar[int]
    BLOCK_HEIGHT_FIELD_NUMBER: _ClassVar[int]
    SIGNERS_FIELD_NUMBER: _ClassVar[int]
    OBSERVED_PUB_KEY_FIELD_NUMBER: _ClassVar[int]
    KEYSIGN_MS_FIELD_NUMBER: _ClassVar[int]
    FINALISE_HEIGHT_FIELD_NUMBER: _ClassVar[int]
    AGGREGATOR_FIELD_NUMBER: _ClassVar[int]
    AGGREGATOR_TARGET_FIELD_NUMBER: _ClassVar[int]
    AGGREGATOR_TARGET_LIMIT_FIELD_NUMBER: _ClassVar[int]
    SPENT_OUTPUT_REFS_FIELD_NUMBER: _ClassVar[int]
    tx: Tx
    status: Status
    out_hashes: _containers.RepeatedScalarFieldContainer[str]
    block_height: int
    signers: _containers.RepeatedScalarFieldContainer[str]
    observed_pub_key: str
    keysign_ms: int
    finalise_height: int
    aggregator: str
    aggregator_target: str
    aggregator_target_limit: str
    spent_output_refs: _containers.RepeatedCompositeFieldContainer[OutputRef]
    def __init__(self, tx: _Optional[_Union[Tx, _Mapping]] = ..., status: _Optional[_Union[Status, str]] = ..., out_hashes: _Optional[_Iterable[str]] = ..., block_height: _Optional[int] = ..., signers: _Optional[_Iterable[str]] = ..., observed_pub_key: _Optional[str] = ..., keysign_ms: _Optional[int] = ..., finalise_height: _Optional[int] = ..., aggregator: _Optional[str] = ..., aggregator_target: _Optional[str] = ..., aggregator_target_limit: _Optional[str] = ..., spent_output_refs: _Optional[_Iterable[_Union[OutputRef, _Mapping]]] = ...) -> None: ...

class Attestation(_message.Message):
    __slots__ = ("PubKey", "Signature")
    PUBKEY_FIELD_NUMBER: _ClassVar[int]
    SIGNATURE_FIELD_NUMBER: _ClassVar[int]
    PubKey: bytes
    Signature: bytes
    def __init__(self, PubKey: _Optional[bytes] = ..., Signature: _Optional[bytes] = ...) -> None: ...

class AttestTx(_message.Message):
    __slots__ = ("obsTx", "attestation", "inbound", "allow_future_observation")
    OBSTX_FIELD_NUMBER: _ClassVar[int]
    ATTESTATION_FIELD_NUMBER: _ClassVar[int]
    INBOUND_FIELD_NUMBER: _ClassVar[int]
    ALLOW_FUTURE_OBSERVATION_FIELD_NUMBER: _ClassVar[int]
    obsTx: ObservedTx
    attestation: Attestation
    inbound: bool
    allow_future_observation: bool
    def __init__(self, obsTx: _Optional[_Union[ObservedTx, _Mapping]] = ..., attestation: _Optional[_Union[Attestation, _Mapping]] = ..., inbound: bool = ..., allow_future_observation: bool = ...) -> None: ...

class QuorumTx(_message.Message):
    __slots__ = ("obsTx", "attestations", "inbound", "allow_future_observation")
    OBSTX_FIELD_NUMBER: _ClassVar[int]
    ATTESTATIONS_FIELD_NUMBER: _ClassVar[int]
    INBOUND_FIELD_NUMBER: _ClassVar[int]
    ALLOW_FUTURE_OBSERVATION_FIELD_NUMBER: _ClassVar[int]
    obsTx: ObservedTx
    attestations: _containers.RepeatedCompositeFieldContainer[Attestation]
    inbound: bool
    allow_future_observation: bool
    def __init__(self, obsTx: _Optional[_Union[ObservedTx, _Mapping]] = ..., attestations: _Optional[_Iterable[_Union[Attestation, _Mapping]]] = ..., inbound: bool = ..., allow_future_observation: bool = ...) -> None: ...

class QuorumState(_message.Message):
    __slots__ = ("quoTxs", "quoNetworkFees", "quoSolvencies", "quoErrataTxs", "quoPriceFeeds")
    QUOTXS_FIELD_NUMBER: _ClassVar[int]
    QUONETWORKFEES_FIELD_NUMBER: _ClassVar[int]
    QUOSOLVENCIES_FIELD_NUMBER: _ClassVar[int]
    QUOERRATATXS_FIELD_NUMBER: _ClassVar[int]
    QUOPRICEFEEDS_FIELD_NUMBER: _ClassVar[int]
    quoTxs: _containers.RepeatedCompositeFieldContainer[QuorumTx]
    quoNetworkFees: _containers.RepeatedCompositeFieldContainer[QuorumNetworkFee]
    quoSolvencies: _containers.RepeatedCompositeFieldContainer[QuorumSolvency]
    quoErrataTxs: _containers.RepeatedCompositeFieldContainer[QuorumErrataTx]
    quoPriceFeeds: _containers.RepeatedCompositeFieldContainer[QuorumPriceFeed]
    def __init__(self, quoTxs: _Optional[_Iterable[_Union[QuorumTx, _Mapping]]] = ..., quoNetworkFees: _Optional[_Iterable[_Union[QuorumNetworkFee, _Mapping]]] = ..., quoSolvencies: _Optional[_Iterable[_Union[QuorumSolvency, _Mapping]]] = ..., quoErrataTxs: _Optional[_Iterable[_Union[QuorumErrataTx, _Mapping]]] = ..., quoPriceFeeds: _Optional[_Iterable[_Union[QuorumPriceFeed, _Mapping]]] = ...) -> None: ...

class NetworkFee(_message.Message):
    __slots__ = ("height", "chain", "transaction_size", "transaction_rate")
    HEIGHT_FIELD_NUMBER: _ClassVar[int]
    CHAIN_FIELD_NUMBER: _ClassVar[int]
    TRANSACTION_SIZE_FIELD_NUMBER: _ClassVar[int]
    TRANSACTION_RATE_FIELD_NUMBER: _ClassVar[int]
    height: int
    chain: str
    transaction_size: int
    transaction_rate: int
    def __init__(self, height: _Optional[int] = ..., chain: _Optional[str] = ..., transaction_size: _Optional[int] = ..., transaction_rate: _Optional[int] = ...) -> None: ...

class AttestNetworkFee(_message.Message):
    __slots__ = ("network_fee", "attestation")
    NETWORK_FEE_FIELD_NUMBER: _ClassVar[int]
    ATTESTATION_FIELD_NUMBER: _ClassVar[int]
    network_fee: NetworkFee
    attestation: Attestation
    def __init__(self, network_fee: _Optional[_Union[NetworkFee, _Mapping]] = ..., attestation: _Optional[_Union[Attestation, _Mapping]] = ...) -> None: ...

class QuorumNetworkFee(_message.Message):
    __slots__ = ("network_fee", "attestations")
    NETWORK_FEE_FIELD_NUMBER: _ClassVar[int]
    ATTESTATIONS_FIELD_NUMBER: _ClassVar[int]
    network_fee: NetworkFee
    attestations: _containers.RepeatedCompositeFieldContainer[Attestation]
    def __init__(self, network_fee: _Optional[_Union[NetworkFee, _Mapping]] = ..., attestations: _Optional[_Iterable[_Union[Attestation, _Mapping]]] = ...) -> None: ...

class Solvency(_message.Message):
    __slots__ = ("id", "chain", "pub_key", "coins", "height")
    ID_FIELD_NUMBER: _ClassVar[int]
    CHAIN_FIELD_NUMBER: _ClassVar[int]
    PUB_KEY_FIELD_NUMBER: _ClassVar[int]
    COINS_FIELD_NUMBER: _ClassVar[int]
    HEIGHT_FIELD_NUMBER: _ClassVar[int]
    id: str
    chain: str
    pub_key: str
    coins: _containers.RepeatedCompositeFieldContainer[Coin]
    height: int
    def __init__(self, id: _Optional[str] = ..., chain: _Optional[str] = ..., pub_key: _Optional[str] = ..., coins: _Optional[_Iterable[_Union[Coin, _Mapping]]] = ..., height: _Optional[int] = ...) -> None: ...

class AttestSolvency(_message.Message):
    __slots__ = ("solvency", "attestation")
    SOLVENCY_FIELD_NUMBER: _ClassVar[int]
    ATTESTATION_FIELD_NUMBER: _ClassVar[int]
    solvency: Solvency
    attestation: Attestation
    def __init__(self, solvency: _Optional[_Union[Solvency, _Mapping]] = ..., attestation: _Optional[_Union[Attestation, _Mapping]] = ...) -> None: ...

class QuorumSolvency(_message.Message):
    __slots__ = ("solvency", "attestations")
    SOLVENCY_FIELD_NUMBER: _ClassVar[int]
    ATTESTATIONS_FIELD_NUMBER: _ClassVar[int]
    solvency: Solvency
    attestations: _containers.RepeatedCompositeFieldContainer[Attestation]
    def __init__(self, solvency: _Optional[_Union[Solvency, _Mapping]] = ..., attestations: _Optional[_Iterable[_Union[Attestation, _Mapping]]] = ...) -> None: ...

class ErrataTx(_message.Message):
    __slots__ = ("id", "chain")
    ID_FIELD_NUMBER: _ClassVar[int]
    CHAIN_FIELD_NUMBER: _ClassVar[int]
    id: str
    chain: str
    def __init__(self, id: _Optional[str] = ..., chain: _Optional[str] = ...) -> None: ...

class AttestErrataTx(_message.Message):
    __slots__ = ("errata_tx", "attestation")
    ERRATA_TX_FIELD_NUMBER: _ClassVar[int]
    ATTESTATION_FIELD_NUMBER: _ClassVar[int]
    errata_tx: ErrataTx
    attestation: Attestation
    def __init__(self, errata_tx: _Optional[_Union[ErrataTx, _Mapping]] = ..., attestation: _Optional[_Union[Attestation, _Mapping]] = ...) -> None: ...

class QuorumErrataTx(_message.Message):
    __slots__ = ("errata_tx", "attestations")
    ERRATA_TX_FIELD_NUMBER: _ClassVar[int]
    ATTESTATIONS_FIELD_NUMBER: _ClassVar[int]
    errata_tx: ErrataTx
    attestations: _containers.RepeatedCompositeFieldContainer[Attestation]
    def __init__(self, errata_tx: _Optional[_Union[ErrataTx, _Mapping]] = ..., attestations: _Optional[_Iterable[_Union[Attestation, _Mapping]]] = ...) -> None: ...

class PriceFeed(_message.Message):
    __slots__ = ("version", "time", "rates")
    VERSION_FIELD_NUMBER: _ClassVar[int]
    TIME_FIELD_NUMBER: _ClassVar[int]
    RATES_FIELD_NUMBER: _ClassVar[int]
    version: bytes
    time: int
    rates: _containers.RepeatedCompositeFieldContainer[OraclePrice]
    def __init__(self, version: _Optional[bytes] = ..., time: _Optional[int] = ..., rates: _Optional[_Iterable[_Union[OraclePrice, _Mapping]]] = ...) -> None: ...

class AttestPriceFeed(_message.Message):
    __slots__ = ("price_feed", "attestation")
    PRICE_FEED_FIELD_NUMBER: _ClassVar[int]
    ATTESTATION_FIELD_NUMBER: _ClassVar[int]
    price_feed: PriceFeed
    attestation: Attestation
    def __init__(self, price_feed: _Optional[_Union[PriceFeed, _Mapping]] = ..., attestation: _Optional[_Union[Attestation, _Mapping]] = ...) -> None: ...

class QuorumPriceFeed(_message.Message):
    __slots__ = ("price_feed", "attestations")
    PRICE_FEED_FIELD_NUMBER: _ClassVar[int]
    ATTESTATIONS_FIELD_NUMBER: _ClassVar[int]
    price_feed: PriceFeed
    attestations: _containers.RepeatedCompositeFieldContainer[Attestation]
    def __init__(self, price_feed: _Optional[_Union[PriceFeed, _Mapping]] = ..., attestations: _Optional[_Iterable[_Union[Attestation, _Mapping]]] = ...) -> None: ...

class QuorumPriceFeedBatch(_message.Message):
    __slots__ = ("quorum_price_feeds",)
    QUORUM_PRICE_FEEDS_FIELD_NUMBER: _ClassVar[int]
    quorum_price_feeds: _containers.RepeatedCompositeFieldContainer[QuorumPriceFeed]
    def __init__(self, quorum_price_feeds: _Optional[_Iterable[_Union[QuorumPriceFeed, _Mapping]]] = ...) -> None: ...

class OraclePrice(_message.Message):
    __slots__ = ("amount", "decimals")
    AMOUNT_FIELD_NUMBER: _ClassVar[int]
    DECIMALS_FIELD_NUMBER: _ClassVar[int]
    amount: int
    decimals: int
    def __init__(self, amount: _Optional[int] = ..., decimals: _Optional[int] = ...) -> None: ...

class AttestationBatch(_message.Message):
    __slots__ = ("attest_txs", "attest_network_fees", "attest_solvencies", "attest_errata_txs", "attest_price_feeds")
    ATTEST_TXS_FIELD_NUMBER: _ClassVar[int]
    ATTEST_NETWORK_FEES_FIELD_NUMBER: _ClassVar[int]
    ATTEST_SOLVENCIES_FIELD_NUMBER: _ClassVar[int]
    ATTEST_ERRATA_TXS_FIELD_NUMBER: _ClassVar[int]
    ATTEST_PRICE_FEEDS_FIELD_NUMBER: _ClassVar[int]
    attest_txs: _containers.RepeatedCompositeFieldContainer[AttestTx]
    attest_network_fees: _containers.RepeatedCompositeFieldContainer[AttestNetworkFee]
    attest_solvencies: _containers.RepeatedCompositeFieldContainer[AttestSolvency]
    attest_errata_txs: _containers.RepeatedCompositeFieldContainer[AttestErrataTx]
    attest_price_feeds: _containers.RepeatedCompositeFieldContainer[AttestPriceFeed]
    def __init__(self, attest_txs: _Optional[_Iterable[_Union[AttestTx, _Mapping]]] = ..., attest_network_fees: _Optional[_Iterable[_Union[AttestNetworkFee, _Mapping]]] = ..., attest_solvencies: _Optional[_Iterable[_Union[AttestSolvency, _Mapping]]] = ..., attest_errata_txs: _Optional[_Iterable[_Union[AttestErrataTx, _Mapping]]] = ..., attest_price_feeds: _Optional[_Iterable[_Union[AttestPriceFeed, _Mapping]]] = ...) -> None: ...

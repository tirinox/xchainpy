import asyncio
from enum import Enum
from typing import NamedTuple, Optional

from xchainpy2_midgard.rest import ApiException
from xchainpy2_thorchain import ActionType, THORMemo
from xchainpy2_thornode import TxStatusResponse, TxSignersResponse
from xchainpy2_utils import DEFAULT_CHAIN_ATTRS, remove_0x_prefix
from .cache import THORChainCache

DEFAULT_POLL_INTERVAL = 5  # sec


class TxStatus(Enum):
    UNKNOWN = 'unknown'
    OBSERVED = 'observed'
    DONE = 'done'
    REFUNDED = 'refunded'
    INCOMPLETE = 'incomplete'
    BELOW_DUST = 'dust'

    @classmethod
    def finished(cls):
        return cls.DONE, cls.REFUNDED, cls.BELOW_DUST


class TxStage(Enum):
    Unknown = 'Unknown'
    InboundObserved = 'InboundObserved'
    InboundConfirmationCounted = 'InboundConfirmationCounted'
    InboundFinalised = 'InboundFinalised'
    SwapFinalised = 'SwapFinalised'
    OutboundDelayWait = 'OutboundDelayWait'
    OutboundSigned = 'OutboundSigned'


class TxDetails(NamedTuple):
    txid: str
    action_type: ActionType
    status: TxStatus
    stage: TxStage
    signers: TxSignersResponse
    status_details: TxStatusResponse

    @property
    def successful(self):
        return self.status == TxStatus.DONE

    @property
    def failed(self):
        return self.status in (TxStatus.REFUNDED, TxStatus.BELOW_DUST)

    @property
    def pending(self):
        return not self.failed and not self.successful

    @classmethod
    def create(cls, signers: Optional[TxSignersResponse], status_details: Optional[TxStatusResponse],
               tx_hash=''):
        if not signers or not status_details:
            return cls(
                tx_hash, ActionType.UNKNOWN, TxStatus.UNKNOWN, TxStage.Unknown, signers, status_details
            )

        memo = THORMemo.parse_memo(status_details.tx.memo)

        stage = TxStage.Unknown
        status = TxStatus.UNKNOWN

        if cls.get_stage(status_details, 'inbound_observed'):
            stage = TxStage.InboundObserved
        if cls.get_stage(status_details, 'inbound_confirmation_counted'):
            stage = TxStage.InboundConfirmationCounted
            status = TxStatus.OBSERVED
        if cls.get_stage(status_details, 'inbound_finalised'):
            stage = TxStage.InboundFinalised
            status = TxStatus.OBSERVED
        if cls.get_stage(status_details, 'swap_finalised'):
            stage = TxStage.SwapFinalised
        if cls.get_stage(status_details, 'outbound_delay'):
            stage = TxStage.OutboundDelayWait
        if cls.get_stage(status_details, 'outbound_signed'):
            stage = TxStage.OutboundSigned

        if stage == TxStage.OutboundSigned:
            if memo.action in (ActionType.SWAP, ActionType.WITHDRAW, ActionType.LOAN_OPEN,
                               ActionType.UNBOND):
                status = TxStatus.DONE
        elif stage == TxStage.SwapFinalised and status_details.out_txs:
            # outbound inside THORChain blockchain
            status = TxStatus.DONE
        elif stage == TxStage.InboundFinalised:
            if memo.action in (ActionType.ADD_LIQUIDITY, ActionType.BOND, ActionType.DONATE):
                status = TxStatus.DONE
        elif stage == TxStage.InboundObserved or stage == TxStage.InboundFinalised:
            status = TxStatus.OBSERVED

        refunds = cls.find_refunds(status_details)
        if refunds:
            status = TxStatus.REFUNDED

        # todo: handle other cases and set appropriate TxStatus

        return cls(
            status_details.tx.id,
            memo.action,
            status,
            stage,
            signers, status_details
        )

    @classmethod
    def get_stage(cls, status_details, stage, key='completed', default=None):
        stages = status_details.stages.to_dict()
        stage_desc = stages.get(stage)
        if stage_desc is None:
            return

        return stage_desc.get(key, default)

    @classmethod
    def find_refunds(cls, status_details: TxStatusResponse):
        return [
            tx for tx in status_details.out_txs
            if 'REFUND' in tx.memo.upper()
        ] if status_details.out_txs else []

    @property
    def has_refunds(self):
        return bool(self.find_refunds(self.status_details))

    @property
    def has_out_txs(self):
        return bool(self.status_details.out_txs)


class TransactionTracker:
    def __init__(self, cache: THORChainCache, chain_attributes=DEFAULT_CHAIN_ATTRS):
        self.cache = cache
        self.chain_attributes = chain_attributes

    async def check_tx_progress(self, inbound_tx_hash: str) -> TxDetails:
        if len(inbound_tx_hash) <= 10:
            raise ValueError('inbound_tx_hash is too short')
        try:
            tx_details: TxSignersResponse = await self.cache.tx_api.tx_signers(inbound_tx_hash)
        except ApiException as e:
            if e.status == 404:
                return TxDetails.create(None, None, inbound_tx_hash)
            raise

        try:
            tx_status: TxStatusResponse = await self.cache.tx_api.tx_status(inbound_tx_hash)
        except ApiException as e:
            if e.status == 404:
                return TxDetails.create(tx_details, None)
            raise

        return TxDetails.create(tx_details, tx_status)

    def poll(self, txid: str, interval=DEFAULT_POLL_INTERVAL, stage=True, status=True):
        """
        Poll TX status
        Usages:

        async for details in tracker.poll(txid):
            if not details.pending:
                print(f'Finished: {details}')
                break
            else:
                print('Still pending...')

        :param txid: inbound TX hash
        :param interval: Interval between requests in seconds
        :return: async generator
        """
        return TransactionTrackerAsyncGenerator(self, interval, txid, stage, status)


class TransactionTrackerAsyncGenerator:
    def __init__(self, tracker: TransactionTracker, interval, tx_hash, stage=True, status=True):
        self.tracker = tracker
        self.interval = interval
        self.tx_hash = remove_0x_prefix(tx_hash)
        self.stage = stage
        self.status = status
        if not self.stage and not self.status:
            raise ValueError('At least one of stage or status should be True')

        self._previous_status = TxStatus.UNKNOWN
        self._previous_stage = TxStage.Unknown
        self._finished = False

    def __aiter__(self):
        return self

    async def __anext__(self) -> TxDetails:
        if self._finished:
            raise StopAsyncIteration

        while True:
            details = await self.tracker.check_tx_progress(self.tx_hash)

            something_changed = False
            if self.stage and details.stage != self._previous_stage:
                self._previous_stage = details.stage
                something_changed = True
            if self.status and details.status != self._previous_status:
                self._previous_status = details.status
                something_changed = True

            if not details.pending:
                self._finished = True
                return details

            if not something_changed:
                await asyncio.sleep(self.interval)
            else:
                return details

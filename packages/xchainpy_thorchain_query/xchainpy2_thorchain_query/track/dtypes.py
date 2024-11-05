from enum import Enum
from typing import NamedTuple, Optional

from xchainpy2_thorchain import ActionType, THORMemo
from xchainpy2_thornode import TxStatusResponse, TxSignersResponse


class TxStatus(Enum):
    """
    Transaction status enum.
    If it is pending, it means that transaction is not finished yet. But you can check its stage. See TxStage enum.
    If transaction is done, it means that it is finished successfully.
    Incomplete means that you need to submit another transaction to complete this one (usually add liquidity for
    other side).
    """

    UNKNOWN = 'unknown'
    PENDING = 'pending'
    DONE = 'done'
    REFUNDED = 'refunded'
    INCOMPLETE = 'incomplete'
    BELOW_DUST = 'dust'

    Unknown = UNKNOWN
    Pending = PENDING
    Done = DONE
    Refunded = REFUNDED
    Incomplete = INCOMPLETE
    BelowDust = BELOW_DUST

    @classmethod
    def finished(cls):
        """
        Return list of statuses that are considered finished (successful or failed)
        :return:
        """
        return cls.DONE, cls.REFUNDED, cls.BELOW_DUST

    @property
    def is_successful(self):
        return self == self.DONE

    @property
    def is_pending(self):
        return self == self.PENDING

    @property
    def is_finished(self):
        return self in self.finished()


class TxStage(Enum):
    """
    Transaction stage enum.
    """

    Unknown = 'Unknown'
    """Unknown stage. Transaction is not observed yet even by the source blockchain client."""

    InboundSubmitted = 'InboundSubmitted'
    """Transaction is submitted on the inbound chain, but not observed yet by THORChain"""

    InboundObserved = 'InboundObserved'
    """Transaction is observed by THORChain"""

    InboundConfirmationCounted = 'InboundConfirmationCounted'
    """Transaction is observed and has enough confirmations"""

    InboundFinalised = 'InboundFinalised'
    """Transaction is finalised on the inbound chain"""

    SwapFinalised = 'SwapFinalised'
    """Swap transaction is finalised"""

    OutboundDelayWait = 'OutboundDelayWait'
    """Outbound transaction is waiting for delay"""

    OutboundSigned = 'OutboundSigned'
    """Outbound transaction is signed by THORChain"""

    OutboundConfirmed = 'OutboundConfirmed'
    """Outbound transaction is confirmed in the outbound chain"""


class TxDetails(NamedTuple):
    """
    Transaction details, stage and status
    """

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
    def create_from_thorchain(cls, signers: Optional[TxSignersResponse], status_details: Optional[TxStatusResponse],
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
            status = TxStatus.Pending
        if cls.get_stage(status_details, 'inbound_finalised'):
            stage = TxStage.InboundFinalised
            status = TxStatus.Pending
        if cls.get_stage(status_details, 'swap_finalised'):
            stage = TxStage.SwapFinalised
        if cls.get_stage(status_details, 'outbound_delay'):
            stage = TxStage.OutboundDelayWait
        if cls.get_stage(status_details, 'outbound_signed'):
            stage = TxStage.OutboundSigned

        if stage == TxStage.OutboundSigned:
            if memo.action in (ActionType.SWAP, ActionType.WITHDRAW, ActionType.LOAN_OPEN,
                               ActionType.UNBOND):
                status = TxStatus.Done
        elif stage == TxStage.SwapFinalised and status_details.out_txs:
            # outbound inside THORChain blockchain
            status = TxStatus.DONE
        elif stage == TxStage.InboundFinalised:
            if memo.action in (ActionType.ADD_LIQUIDITY, ActionType.BOND, ActionType.DONATE):
                status = TxStatus.Done
        elif stage == TxStage.InboundObserved or stage == TxStage.InboundFinalised:
            status = TxStatus.Pending

        refunds = cls.find_refunds(status_details)
        if refunds:
            status = TxStatus.Refunded

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

    @classmethod
    def dry_run_success(cls, tx_hash: str):
        """
        Create TxDetails that represents successful dry-run transaction

        :param tx_hash: TX hash string
        :return: TxDetails
        """
        # noinspection PyTypeChecker
        return cls(
            tx_hash,
            ActionType.UNKNOWN,
            TxStatus.DONE,
            TxStage.Unknown,
            None, None
        )

import asyncio

from xchainpy2_midgard.rest import ApiException
from xchainpy2_thornode import TxStatusResponse, TxSignersResponse
from xchainpy2_utils import DEFAULT_CHAIN_ATTRS
from .cache import THORChainCache
from .models import TxDetails, TxStatus, TxStage

DEFAULT_POLL_INTERVAL = 10  # sec


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
                print(f'Still pending...')

        :param txid: inbound TX hash
        :param interval: Interval between requests in seconds
        :return: async generator
        """
        return TransactionTrackerAsyncGenerator(self, interval, txid, stage, status)


class TransactionTrackerAsyncGenerator:
    def __init__(self, tracker: TransactionTracker, interval, txid, stage=True, status=True):
        self.tracker = tracker
        self.interval = interval
        self.txid = txid
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
            details = await self.tracker.check_tx_progress(self.txid)

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

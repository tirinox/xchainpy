import asyncio

from xchainpy2_thornode import TxStatusResponse, TxSignersResponse
from xchainpy2_utils import DEFAULT_CHAIN_ATTRS
from .cache import THORChainCache
from .models import TxDetails, TxStatus

DEFAULT_POLL_INTERVAL = 10  # sec


class TransactionTracker:
    def __init__(self, cache: THORChainCache, chain_attributes=DEFAULT_CHAIN_ATTRS):
        self.cache = cache
        self.chain_attributes = chain_attributes

    async def check_tx_progress(self, inbound_tx_hash: str) -> TxDetails:
        if len(inbound_tx_hash) <= 10:
            raise ValueError('inbound_tx_hash is too short')
        tx_details: TxSignersResponse = await self.cache.tx_api.tx_signers(inbound_tx_hash)
        tx_status: TxStatusResponse = await self.cache.tx_api.tx_status(inbound_tx_hash)

        return TxDetails.create(tx_details, tx_status)

    def poll(self, txid: str, interval=DEFAULT_POLL_INTERVAL):
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
        return TransactionTrackerAsyncGenerator(self, interval, txid)


class TransactionTrackerAsyncGenerator:
    def __init__(self, tracker: TransactionTracker, interval, txid):
        self.tracker = tracker
        self.interval = interval
        self.txid = txid

        self._previous_status = TxStatus.UNKNOWN

    def __aiter__(self):
        return self

    async def __anext__(self):
        if self._previous_status in TxStatus.finished():
            raise StopIteration

        while True:
            details = await self.tracker.check_tx_progress(self.txid)
            print('.')
            if details.status == self._previous_status:
                await asyncio.sleep(self.interval)
            else:
                self._previous_status = details.status
                return details

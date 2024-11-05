import asyncio
from typing import Optional

from xchainpy2_client import XChainClient
from xchainpy2_midgard.rest import ApiException
from xchainpy2_thornode import TxStatusResponse, TxSignersResponse
from xchainpy2_utils import DEFAULT_CHAIN_ATTRS, remove_0x_prefix
from .dtypes import TxDetails, TxStage, TxStatus
from ..cache import THORChainCache

DEFAULT_POLL_INTERVAL = 5  # sec
"""
Default poll interval in seconds for polling transaction status
"""


class TransactionTracker:
    def __init__(self, cache: THORChainCache, chain_attributes=None,
                 inbound_chain_client: Optional[XChainClient] = None,
                 outbound_chain_client: Optional[XChainClient] = None
                 ):
        """
        Transaction tracker.

        :param cache: THORChain cache provides access to THORChain API
        :param chain_attributes: chain attributes, don't change unless you know what you are doing
        :param inbound_chain_client: Optional, provide if you want to check tx status before it's observed by THORChain
        :param outbound_chain_client: Optional, provide if you want to check tx status after it's singed by THORChain
        """

        self.cache = cache
        self.chain_attributes = chain_attributes or DEFAULT_CHAIN_ATTRS
        self.inbound_chain_client = inbound_chain_client
        self.outbound_chain_client = outbound_chain_client

    @staticmethod
    def _validate_tx_hash(tx_hash: str):
        if not isinstance(tx_hash, str):
            raise ValueError('tx_hash should be a string')

        if len(tx_hash) <= 10:
            raise ValueError('tx_hash is too short')

    async def check_tx_outside_thorchain(self, tx_hash: str, is_inbound: bool):
        """
        Check transaction status outside THORChain, namely in the inbound or outbound chain.
        :param tx_hash: Transaction hash (tx_id)
        :param is_inbound: If True, check transaction status before it's observed by THORChain, otherwise after it's signed by THORChain
        :return:
        """
        self._validate_tx_hash(tx_hash)

        if is_inbound:
            if not self.inbound_chain_client:
                raise ValueError('inbound_chain_client is not set')
            tx_details = await self.inbound_chain_client.get_transaction_data(tx_hash)
        else:
            if not self.outbound_chain_client:
                raise ValueError('outbound_chain_client is not set')
            tx_details = await self.outbound_chain_client.get_transaction_data(tx_hash)

        return TxDetails(tx_details, )

    async def tc_get_tx_details(self, inbound_tx_hash: str, height=0) -> Optional[TxSignersResponse]:
        try:
            tx_details: TxSignersResponse = await self.cache.tx_api.tx_signers(inbound_tx_hash, height=height)
            return tx_details
        except ApiException as e:
            if e.status == 404:
                return
            raise

    async def tc_get_tx_status(self, inbound_tx_hash: str, height=0) -> Optional[TxStatusResponse]:
        """
        Get transaction status from THORChain.
        https://thornode.ninerealms.com/thorchain/tx/status/inbound_tx_hash
        According to the current implementation, if the transaction is not found, it doesn't return "None"
         but something like that

        {
          "stages": {
            "inbound_observed": {
              "started": false,
              "final_count": 0,
              "completed": false
            }
          }
        }

        :param inbound_tx_hash: Tx hash without 0x prefix
        :param height: Block height, if not provided, the latest block height is used
        :return: Optional[TxStatusResponse]
        """
        try:
            tx_status: TxStatusResponse = await self.cache.tx_api.tx_status(inbound_tx_hash, height=height)
            return tx_status
        except ApiException as e:
            if e.status == 404:
                return
            raise

    async def check_tx_progress(self, inbound_tx_hash: str) -> TxDetails:
        """
        Check transaction progress.

        :param inbound_tx_hash: Transaction hash (tx_id)
        :return: Transaction details
        """
        self._validate_tx_hash(inbound_tx_hash)

        if 'dry-run' in inbound_tx_hash.lower():
            return TxDetails.dry_run_success(inbound_tx_hash)

        tx_details = await self.tc_get_tx_details(inbound_tx_hash)
        tx_status = await self.tc_get_tx_status(inbound_tx_hash)

        if tx_details is None or tx_status is None:
            return TxDetails.create_from_thorchain(tx_details, tx_status, inbound_tx_hash)

        # todo: if there is scheduled outbound tx, check its status in its own chain

        return TxDetails.create_from_thorchain(tx_details, tx_status)

    def poll(self, txid: str, interval=DEFAULT_POLL_INTERVAL, stage=True, status=True):
        """
        Poll TX status.
        Usages:

        async for details in tracker.poll(txid):
            if not details.pending:
                print(f'Finished: {details}')
                break
            else:
                print('Still pending...')

        :param status: Flag to check status of TX
        :param stage: Flag to check stage of TX
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

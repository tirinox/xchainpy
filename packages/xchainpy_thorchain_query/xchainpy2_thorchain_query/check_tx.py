import json
import logging
import re
from datetime import datetime, timedelta
from typing import Union, List

from xchainpy2_mayanode import LastBlock as LastBlockMaya
from xchainpy2_thornode import LastBlock, TxDetailsResponse
from xchainpy2_utils import DEFAULT_CHAIN_ATTRS, Asset, Chain, CryptoAmount, Amount
from xchainpy2_utils.swap import get_decimal
from .cache import THORChainCache
from .models import TxProgress, TxType, InboundStatus, InboundTx, SwapStatus, SwapInfo, AddLpStatus, AddLpInfo, \
    WithdrawStatus, WithdrawInfo, AddSaverStatus, AddSaverInfo, WithdrawSaverInfo, RefundStatus, RefundInfo

logger = logging.getLogger(__name__)


class TransactionStage:
    def __int__(self, cache: THORChainCache, chain_attributes=DEFAULT_CHAIN_ATTRS):
        self.cache = cache
        self.chain_attributes = chain_attributes

    async def check_tx_progress(self, inbound_tx_hash: str) -> TxProgress:
        if len(inbound_tx_hash) <= 10:
            raise ValueError('inbound_tx_hash is too short')

        try:
            tx_data = await self.cache.tx_api.tx_signers(inbound_tx_hash)
        except Exception as e:
            logger.exception(e)
            return TxProgress(TxType.Unknown)

        progress = await self.determine_observed(tx_data)

        if progress.tx_type == TxType.Swap:
            return await self.check_swap_progress(tx_data, progress)
        elif progress.tx_type == TxType.AddLP:
            return await self.check_add_liquidity_progress(tx_data, progress)
        elif progress.tx_type == TxType.WithdrawLP:
            return await self.check_withdraw_progress(tx_data, progress)
        elif progress.tx_type == TxType.AddSaver:
            return await self.check_add_saver_progress(tx_data, progress)
        elif progress.tx_type == TxType.WithdrawSaver:
            return await self.check_withdraw_saver_progress(tx_data, progress)
        elif progress.tx_type == TxType.Refund:
            return await self.check_refund_progress(tx_data, progress)

        return progress

    async def determine_observed(self, tx_data: TxDetailsResponse) -> TxProgress:
        progress = TxProgress(TxType.Unknown)

        if not tx_data.tx:
            return progress

        memo = tx_data.tx.memo or ''
        parts = memo.split(':')
        operation = get_part(parts, 0)
        if tx_data.tx.tx.coins and len(tx_data.tx.tx.coins) > 0:
            asset_in = Asset.from_string(tx_data.tx.tx.coins[0].asset)
            inbound_amount = tx_data.tx.tx.coins[0].amount
        else:
            asset_in = 'unknown'
            inbound_amount = 0

        from_address = tx_data.tx.tx.from_address or 'unknown'

        if tx_data.tx.tx.chain == self.cache.chain:
            block = tx_data.finalised_height
        else:
            block = tx_data.tx.finalise_height

        if tx_data.tx.tx.chain == self.cache.chain:
            finalize_block = tx_data.finalised_height
        else:
            finalize_block = tx_data.tx.finalise_height

        if tx_data.tx.status.lower() == 'done':
            status = InboundStatus.Observed_Consensus
        else:
            status = InboundStatus.Observed_Incomplete

        has_slash = '/' in parts[1]
        has_dot = '.' in parts[1]

        if re.search(r'swap|s|=', operation, re.IGNORECASE):
            progress.txType = TxType.Swap
        if has_slash and \
                (re.search(r'add', operation, re.IGNORECASE) or re.search(r'a|[+]', operation, re.IGNORECASE)):
            progress.txType = TxType.AddSaver
        if has_dot and \
                (re.search(r'add', operation, re.IGNORECASE) or re.search(r'a|[+]', operation, re.IGNORECASE)):
            progress.txType = TxType.AddLP
        if re.search(r'withdraw|wd|-', operation, re.IGNORECASE) and has_slash:
            progress.txType = TxType.WithdrawSaver
        if re.search(r'withdraw|wd|-', operation, re.IGNORECASE) and has_dot:
            progress.txType = TxType.WithdrawLP
        if re.search(r'refund', operation, re.IGNORECASE):
            progress.txType = TxType.Refund
        if re.search(r'out', operation, re.IGNORECASE):
            progress.txType = TxType.Other

        amount = await self.get_crypto_amount(inbound_amount, asset_in)

        date_observed = await self.block_to_date(self.cache.chain, tx_data, 0)
        if tx_data.tx.tx.chain == self.cache.chain:
            expected_confirmation_date = date_observed
        else:
            expected_confirmation_date = await self.block_to_date(Chain(asset_in.chain.upper()), tx_data, 0)

        progress.inbound_observed = InboundTx(
            status,
            date_observed,
            block,
            finalize_block,
            expected_confirmation_date,
            amount,
            from_address,
            memo
        )
        return progress

    @property
    def native_asset(self):
        return self.cache.native_asset

    async def check_swap_progress(self, tx_data: TxDetailsResponse, progress: TxProgress):
        if not progress.inbound_observed:
            return progress

        memo = tx_data.tx.memo or ''
        action, asset, dest_address, limit, affiliate_address, affiliate_fee = self.parse_swap_memo(memo)
        asset_out = Asset.from_string(asset.upper())

        if tx_data.out_txs[0].memo.startswith('OUT'):
            status = SwapStatus.Complete
        else:
            status = SwapStatus.Complete_Refunded

        # current height of thorchain, need for confirmations
        chain_height = await self.get_block_height(self.native_asset)

        # expected outbound height
        outbound_height = tx_data.outbound_height or tx_data.finalised_height
        expected_block_out = tx_data.outbound_height or tx_data.finalised_height
        expected_out_date = await self.block_to_date(self.cache.chain, tx_data, outbound_height)
        confirmations = chain_height - outbound_height if chain_height > outbound_height else 0

        miminum_amount_out = await self.get_crypto_amount(limit or 0, asset_out)
        affiliate_fee = await self.get_crypto_amount(affiliate_fee or 0, asset_out)

        # TODO get out tx
        progress.swap_info = SwapInfo(
            status,
            to_address=dest_address,
            minimum_amount_out=miminum_amount_out,
            affliate_fee=affiliate_fee,
            expected_out_block=expected_block_out,
            expected_out_date=expected_out_date,
            confirmations=confirmations,
            expected_amount_out=miminum_amount_out,  # TODO call estimateSwap()
        )

        return progress

    async def check_add_liquidity_progress(self, tx_data, progress: TxProgress):
        if not progress.inbound_observed:
            return progress

        memo = tx_data.tx.memo or ''
        action, asset, paired_address, affiliate_address, affiliate_fee = self.parse_add_liquidity_memo(memo)
        asset = Asset.from_string(asset.upper())
        is_symmetric = bool(paired_address)
        asset_tx = progress.inbound_observed if progress.inbound_observed.amount.asset != self.native_asset else None
        rune_tx = progress.inbound_observed if progress.inbound_observed.amount.asset == self.native_asset else None
        paired_asset_expected_confirmation_date = await self.block_to_date(Chain(asset.chain), tx_data, 0)
 
        check_lp_position = await self.cache.lp_api.liquidity_provider(
            asset,
            progress.inbound_observed.from_address
        )
        status = AddLpStatus.Complete if check_lp_position else AddLpStatus.Incomplete

        progress.add_liquidity_info = AddLpInfo(
            status,
            is_symmetric,
            asset_tx,
            rune_tx,
            paired_asset_expected_confirmation_date,
            pool=asset,
        )

        return progress

    async def check_withdraw_progress(self, tx_data: TxDetailsResponse, progress: TxProgress):
        if not progress.inbound_observed:
            return progress

        memo = tx_data.tx.memo or ''
        action, asset, paired_address, affiliate_address, affiliate_fee = self._parse_withdraw_lp_memo(memo)
        asset = Asset.from_string(asset)

        last_block_obj = await self.cache.network_api.lastblock()
        if not last_block_obj:
            raise ValueError("No last block")

        if tx_data.tx.status.lower() == 'done':
            outbound_height = int(tx_data.finalised_height)
            status = WithdrawStatus.Complete
            out_amount = parse_amount(tx_data)
        else:
            outbound_height = int(tx_data.outbound_height)
            status = WithdrawStatus.Incomplete
            out_amount = 0

        expected_confirmation_date = await self.block_to_date(self.cache.chain, tx_data, outbound_height)

        outbound_block = int(tx_data.outbound_height or tx_data.finalised_height)
        current_height = self.get_last_native_block(last_block_obj[0])

        if outbound_block > current_height:
            avg_block_time = self.chain_attributes[self.cache.chain].avg_block_time
            estimated_wait_time = (outbound_block - current_height) * avg_block_time
        else:
            estimated_wait_time = 0

        withdraw_amount = await self.get_crypto_amount(out_amount, asset)

        progress.withdraw_lp_info = WithdrawInfo(
            status,
            withdraw_amount,
            expected_confirmation_date,
            current_height,
            outbound_block,
            estimated_wait_time,
        )

        return progress

    async def check_add_saver_progress(self, tx_data: TxDetailsResponse, progress: TxProgress):
        if not progress.inbound_observed:
            return progress

        if progress.inbound_observed.amount.asset != self.native_asset:
            asset_tx = progress.inbound_observed
        else:
            asset_tx = None

        check_saver_vaults = await self.cache.saver_api.saver(
            tx_data.tx.tx.coins[0].asset,
            asset_tx.from_address if asset_tx else ''
        )

        if check_saver_vaults:
            status = AddSaverStatus.Complete
        else:
            status = AddSaverStatus.Incomplete

        progress.add_saver_info = AddSaverInfo(
            status,
            asset_tx,
            check_saver_vaults
        )

        return progress

    async def check_withdraw_saver_progress(self, tx_data: TxDetailsResponse, progress: TxProgress):
        if not progress.inbound_observed:
            return progress

        memo = tx_data.tx.tx.memo or ''
        action, asset, paired_address, affiliate_address, affiliate_fee = self._parse_withdraw_lp_memo(memo)

        last_block_obj = await self.cache.network_api.lastblock()
        if not last_block_obj:
            raise ValueError("No last block")

        # find the date in which the asset should be seen in the wallet
        if tx_data.tx.status.lower() == 'done':
            outbound_height = int(tx_data.finalised_height)
        else:
            outbound_height = int(tx_data.outbound_height)

        # always pass in thorchain
        expected_confirmation_date = await self.block_to_date(self.cache.chain, tx_data, outbound_height)

        out_amount = parse_amount(tx_data) if tx_data.out_txs else 0
        outbound_block = int(tx_data.outbound_height)
        finalised_height = int(tx_data.finalised_height)
        current_tc_height = int(self.get_last_native_block(last_block_obj[0])) if last_block_obj else 0

        if outbound_block > current_tc_height:
            avg_block_time = self.chain_attributes[self.cache.chain].avg_block_time
            estimated_wait_time = (outbound_block - current_tc_height) * avg_block_time
        else:
            estimated_wait_time = 0

        if tx_data.out_txs:
            status = WithdrawStatus.Complete
        else:
            status = WithdrawStatus.Incomplete

        withdraw_amount = await self.get_crypto_amount(out_amount, Asset.from_string(asset))

        progress.withdraw_saver_info = WithdrawSaverInfo(
            status,
            withdraw_amount,
            expected_confirmation_date,
            current_tc_height,
            finalised_height,
            outbound_block,
            estimated_wait_time,
        )

        return progress

    async def check_refund_progress(self, tx_data: TxDetailsResponse, progress: TxProgress):
        if not progress.inbound_observed:
            return progress

        last_block_obj = await self.cache.network_api.lastblock()
        if not last_block_obj:
            raise ValueError("No last block")

        if tx_data.tx.status.lower() == 'done':
            outbound_height = int(tx_data.finalised_height)
        else:
            outbound_height = int(tx_data.outbound_height)

        expected_confirmation_date = await self.block_to_date(self.cache.chain, tx_data, outbound_height)
        amount = tx_data.tx.tx.coins[0].amount
        asset = Asset.from_string(tx_data.tx.tx.coins[0].asset)
        to_address = str(tx_data.tx.tx.to_address)
        outbound_block = self.get_chain_height(last_block_obj, asset.chain)
        finalised_height = int(tx_data.finalised_height)
        current_tc_height = int(self.get_last_native_block(last_block_obj[0])) if last_block_obj else 0

        if outbound_block > current_tc_height:
            avg_block_time = self.chain_attributes[self.cache.chain].avg_block_time
            estimated_wait_time = ((outbound_block - current_tc_height) * avg_block_time +
                                   self.chain_attributes[asset.chain].avg_block_time)
        else:
            estimated_wait_time = 0

        if tx_data.tx.status.lower() == 'done':
            status = RefundStatus.Complete
        else:
            status = RefundStatus.Incomplete

        progress.refund_info = RefundInfo(
            status,
            amount,
            to_address,
            expected_confirmation_date,
            finalised_height,
            current_tc_height,
            outbound_block,
            estimated_wait_time
        )

        return progress

    def get_last_native_block(self, last_block: Union[LastBlock, LastBlockMaya]):
        if self.cache.chain == Chain.THORChain:
            return last_block.thorchain
        elif self.cache.chain == Chain.Maya:
            return last_block.mayachain
        else:
            raise ValueError('Unsupported chain')

    async def get_block_height(self, asset: Asset):
        """
        Returns current block height of an asset's native chain
        :param asset:
        :return:
        """
        last_block_obj = await self.cache.network_api.lastblock()

        if asset.chain == self.native_asset.chain or asset.synth:
            last_block = last_block_obj[0]
            return self.get_last_native_block(last_block)
        else:
            return self.get_chain_height(last_block_obj, asset.chain)

    @staticmethod
    def get_chain_height(last_block_obj: List[LastBlock], chain: str) -> int:
        last_block = [obj for obj in last_block_obj if obj.chain == chain]
        last_block = last_block[0]

        if not last_block:
            raise ValueError(f'No block height found for {chain}')
        return last_block.last_observed_in

    async def block_to_date(self, chain: Chain, tx_data: TxDetailsResponse, outbound_block: int):
        """
        Private function to return the date stamp from block height and chain
        :param chain: input chain
        :param tx_data: txResponse
        :param outbound_block:
        :return: datetime
        """
        last_block_obj = await self.cache.network_api.lastblock()
        time = datetime.now()

        last_block = [obj for obj in last_block_obj if obj.chain == chain]
        if not last_block:
            raise ValueError(f'No block height found for {chain}')

        tc_height = self.get_last_native_block(last_block_obj[0])

        chain_block_time = self.chain_attributes[chain].avg_block_time

        recorded_chain_height = tx_data.tx.block_height
        if outbound_block:
            if outbound_block > tc_height:
                block_difference = outbound_block - tc_height
                seconds = time.timestamp() + block_difference * chain_block_time
                time = datetime.fromtimestamp(seconds)
            else:  # outbound_block <= tc_height
                # already processed find the date it was completed
                block_difference = tc_height - outbound_block
                seconds = time.timestamp() - block_difference * chain_block_time
                return datetime.fromtimestamp(seconds)

        if chain == self.cache.native_asset.chain:
            # RUNE in THORChain or CACAO in MAYA
            finalised_height = tx_data.finalised_height
            block_difference = tc_height - finalised_height
            seconds = time.timestamp() - block_difference * chain_block_time
            return datetime.fromtimestamp(seconds)
        else:
            chain_height = self.get_chain_height(last_block_obj, chain.value)
            block_difference = chain_height - recorded_chain_height
            time = time - timedelta(seconds=block_difference * chain_block_time)
            return time

    @staticmethod
    def _parse_withdraw_lp_memo(memo: str):
        # ADD: POOL:PAIREDADDR: AFFILIATE:FEE
        parts = memo.split(':')
        action = parts[0]
        asset = parts[1]
        # optional fields
        paired_address = get_part(parts, 2)
        affiliate_address = get_part(parts, 3)
        affiliate_fee = get_part(parts, 4)
        return action, asset, paired_address, affiliate_address, affiliate_fee

    @staticmethod
    def parse_add_liquidity_memo(memo: str):
        # ADD:POOL:PAIREDADDR:AFFILIATE:FEE
        parts = memo.split(':')
        action = parts[0]
        asset = parts[1]
        # optional fields
        paired_address = get_part(parts, 2)
        affiliate_address = get_part(parts, 3)
        affiliate_fee = get_part(parts, 4)
        return action, asset, paired_address, affiliate_address, affiliate_fee

    @staticmethod
    def parse_swap_memo(memo: str):
        # SWAP:ASSET:DESTADDR:LIM:AFFILIATE:FEE
        parts = memo.split(':')
        action = parts[0]
        asset = parts[1]
        dest_address = parts[2]
        limit = get_part(parts, 3)
        affiliate_address = get_part(parts, 4)
        affiliate_fee = get_part(parts, 5)
        return action, asset, dest_address, limit, affiliate_address, affiliate_fee

    async def get_crypto_amount(self, base_amount: Union[str, int], asset: Asset):
        try:
            decimals = get_decimal(asset)
        except ValueError:
            pool = await self.cache.get_pool_for_asset(asset)
            decimals = pool.thornode_details.decimals
        return CryptoAmount(Amount.from_base(base_amount, decimals), asset)


def get_part(parts: List[str], index: int):
    return parts[index] if len(parts) > index and parts[index] else None


def parse_amount(tx_data: TxDetailsResponse):
    return int(json.dumps(tx_data.out_txs).split('"amount":"')[1].split('"')[0])  # fixme: ugly!

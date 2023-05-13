import logging
from datetime import datetime, timedelta
from typing import Union, List

from xchainpy2_mayanode import LastBlock as LastBlockMaya
from xchainpy2_thornode import TxSignersResponse, LastBlock
from xchainpy2_utils import DEFAULT_CHAIN_ATTRS, Asset, Chain
from .cache import THORChainCache
from .models import TxProgress, TxType

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

    async def determine_observed(self, tx_data) -> TxProgress:
        pass  # todo

    async def check_swap_progress(self, tx_data, progress):
        pass  # todo

    async def check_add_liquidity_progress(self, tx_data, progress):
        pass  # todo

    async def check_withdraw_progress(self, tx_data, progress):
        pass  # todo

    async def check_add_saver_progress(self, tx_data, progress):
        pass  # todo

    async def check_withdraw_saver_progress(self, tx_data, progress):
        pass  # todo

    async def check_refund_progress(self, tx_data, progress):
        pass  # todo

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

        if asset.chain == self.cache.native_asset.chain or asset.synth:
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

    async def get_last_block(self):
        return await self.cache.network_api.lastblock()

    async def block_to_date(self, chain: Chain, tx_data: TxSignersResponse, outbound_block: int):
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


"""
 /**
   * Private function to return the date stamp from block height and chain
   * @param chain - input chain
   * @param txData - txResponse
   * @returns date()
   */
  private async blockToDate(chain: Chain, txData: TxSignersResponse, outboundBlock?: number) {
    const lastBlockObj = await this.thorchainCache.thornode.getLastBlock()
    const time = new Date()
    let blockDifference: number
    const currentHeight = lastBlockObj.find((obj) => obj.chain == chain)
    const chainHeight = Number(`${currentHeight?.last_observed_in}`)
    const recordedChainHeight = Number(`${txData.tx.block_height}`)
    // If outbound time is required
    if (outboundBlock) {
      const currentHeight = lastBlockObj.find((obj) => obj)
      const thorchainHeight = Number(`${currentHeight?.thorchain}`)
      if (outboundBlock > thorchainHeight) {
        blockDifference = outboundBlock - thorchainHeight
        time.setSeconds(time.getSeconds() + blockDifference * this.chainAttributes[chain].avgBlockTimeInSecs)
        console.log(time)
      } else {
        blockDifference = thorchainHeight - outboundBlock // already processed find the date it was completed
        time.setSeconds(time.getSeconds() - blockDifference * this.chainAttributes[chain].avgBlockTimeInSecs)
        return time
      }
    }
    // find out how long ago it was processed for all chains
    if (chain == THORChain) {
      const currentHeight = lastBlockObj.find((obj) => obj)
      const thorchainHeight = Number(`${currentHeight?.thorchain}`) // current height of the TC
      const finalisedHeight = Number(`${txData.finalised_height}`) // height tx was completed in
      blockDifference = thorchainHeight - finalisedHeight
      time.setSeconds(time.getSeconds() - blockDifference * this.chainAttributes[chain].avgBlockTimeInSecs) // note if using data from a tx that was before a thorchain halt this calculation becomes inaccurate...
    } else {
      // set the time for all other chains
      blockDifference = chainHeight - recordedChainHeight
      time.setSeconds(time.getSeconds() - blockDifference * this.chainAttributes[chain].avgBlockTimeInSecs)
    }
    return time
  }


"""

import abc
import logging
from datetime import datetime
from typing import List, Optional

from xchainpy2_utils import Chain, CryptoAmount, NetworkType, Asset
from .base_client import XChainClient
from .fees import calc_fees_async, standard_fee_rates
from .models import UTXOOnlineDataProviders, FeeRates, \
    FeeRate, TxPage, XcTx, UTXO, FeesWithRates, FeeOption, Fees, Fee, FeeBounds, RootDerivationPaths

logger = logging.getLogger(__name__)


class UTXOClient(XChainClient, abc.ABC):
    def __init__(
            self,
            chain: Chain,
            network: Optional[NetworkType] = None,
            phrase: Optional[str] = None,
            fee_bound: Optional[FeeBounds] = None,
            root_derivation_paths: Optional[RootDerivationPaths] = None,
            data_providers: Optional[UTXOOnlineDataProviders] = None
    ):
        super().__init__(chain, network, phrase, fee_bound=fee_bound, root_derivation_paths=root_derivation_paths)
        self.data_providers = data_providers

    @abc.abstractmethod
    async def get_suggested_fee_rate(self) -> FeeRates:
        pass

    @abc.abstractmethod
    async def calc_fee(self, fee_type: FeeOption, fee_rate: FeeRate, memo: str = '') -> Fee:
        pass

    async def get_transactions(self, address: str = '',
                               offset: int = 0,
                               limit: int = 0,
                               start_time: Optional[datetime] = None,
                               end_time: Optional[datetime] = None,
                               asset: Optional[Asset] = None, ) -> TxPage:
        """
        Get transaction history of a given address with pagination options.
        By default, it will return the transaction history of the current wallet.
        :param address: The address to get the transaction history. (#0 by default)
        :param offset: The offset to start getting the transaction history. (0 by default)
        :param limit: The number of transaction history to get. (10 by default)
        :param start_time: The start time of the transaction history. (optional)
        :param end_time: The end time of the transaction history. (optional)
        :param asset: The asset to get the transaction history. (optional)
        :return: The transaction history.
        """
        address = address or self.get_address()

        return await self._round_robin('get_transactions', address, offset, limit, start_time, end_time, asset)

    async def get_transaction_data(self, tx_id: str) -> Optional[XcTx]:
        """
        Get the transaction details of a given transaction id.
        :param tx_id: The transaction id.
        :return: The transaction details of the given transaction id.
        """
        return await self._round_robin('get_transaction_data', tx_id)

    async def get_balance(self, address: str, confirmed_only=True) -> List[CryptoAmount]:
        """
        Get the balance of a given address.
        :param address: BTC address to get balances from
        :param confirmed_only: Flag to get balances of confirmed txs only
        :return: BTC balances
        """
        return await self._round_robin('get_balance', address)

    async def get_fees_with_rates(self, memo='') -> FeesWithRates:
        rates = await self.get_fee_rates()
        fees = await calc_fees_async(
            rates,
            self.calc_fee,
            memo,
        )
        return FeesWithRates(fees=fees, rates=rates)

    async def get_fees(self, memo='') -> Fees:
        return (await self.get_fees_with_rates(memo)).fees

    async def get_fee_rates(self, cache=None) -> FeeRates:
        """
        Get the fee rates. First from THORChain node. If it fails, get it from the suggested.
        :param cache: THORChainCache instance from the xchainpy2_thorchain_query packages
        :return: FeeRates
        """
        fee_rate = None
        try:
            if cache:
                inbound_details = await cache.get_inbound_details()
                for details in inbound_details.values():
                    if details.chain == self.chain:
                        fee_rate = float(details.gas_rate)
        except Exception as e:
            logger.error(f'Error getting inbound details: {e}')

        if fee_rate is None:
            fee_rate = await self.get_suggested_fee_rate()

        return standard_fee_rates(fee_rate)

    async def broadcast_tx(self, tx_hex: str) -> str:
        """
        Broadcast the given transaction.
        :param tx_hex: The transaction hex to broadcast.
        :return: The transaction id.
        """
        return await self._round_robin('broadcast_tx', tx_hex)

    async def _round_robin(self, func_name, *args, **kwargs):
        for provider_fam in self.data_providers:
            provider = provider_fam[self.network]
            try:
                return await getattr(provider, func_name)(*args, **kwargs)
            except Exception as e:
                logger.error(f'Error doing function "{func_name}" in {provider!r}: {e}')
        raise Exception(f'No provider is to do "{func_name}"')

    async def _scan_utxos(self, address: str, confirmed_only: bool = True) -> List[UTXO]:
        """
        Scan UTXOs of a given address.
        (direct implementation of roundRobinGetUnspentTxs)
        :param address:
        :param confirmed_only:
        :return:
        """
        if confirmed_only:
            return await self._round_robin('get_confirmed_unspent_txs', address)
        else:
            return await self._round_robin('get_unspent_txs', address)

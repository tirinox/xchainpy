from datetime import datetime
from typing import Union, Optional

from xchainpy2_client import FeeOption
from xchainpy2_thorchain import THORChainClient
from xchainpy2_thorchain_query import THORChainQuery, SwapEstimate
from xchainpy2_utils import CryptoAmount, Asset, Chain, is_gas_asset
from .consts import THOR_BASIS_POINT_MAX
from .wallet import Wallet


class SwapException(Exception):
    def __init__(self, message, errors: list = None):
        super().__init__(message)
        self.errors = errors


class THORChainAMM:
    def __init__(self, wallet: Wallet, query: Optional[THORChainQuery] = None):
        self.query = query or wallet.query_api or THORChainQuery()
        self.wallet = wallet

    async def do_swap(self, input_amount: CryptoAmount,
                      destination_asset: Union[Asset, str],
                      destination_address: str = '',
                      tolerance_bps=0,
                      affiliate_bps=0,
                      affiliate_address: str = '',
                      streaming_interval=0,
                      streaming_quantity=0,
                      fee_option=FeeOption.FAST) -> str:
        """
        Do a swap using the THORChain protocol AMM

        :param input_amount: input amount and asset to swap
        :param destination_asset: output asset to swap to
        :param destination_address: destination address to send swapped asset to
        :param tolerance_bps: price tolerance in basis points (0-10000)
        :param affiliate_bps: affiliate fee in basis points (0-10000)
        :param affiliate_address: affiliate address to collect affiliate fee
        :param streaming_interval: streaming interval in THORChain blocks (6 sec), 0 to disable streaming
        :param streaming_quantity: streaming swap quantity, 0 for automatic
        :param fee_option: fee option to use for swap (refer to input chain client for fee options)
        :return: hash of the inbound transaction (used to track transaction status)
        """
        if not destination_address:
            dest_chain = self._dest_chain(Asset.automatic(destination_asset))
            dest_client = self.wallet.get_client(dest_chain)
            if not dest_client:
                raise SwapException('No destination address')
            destination_address = dest_client.get_address()

        validation_error = await self._validate_swap(input_amount, destination_asset, destination_address,
                                                     tolerance_bps, affiliate_bps,
                                                     affiliate_address)

        if validation_error:
            raise SwapException(f'Invalid swap: {validation_error}')

        estimate = await self.query.quote_swap(
            input_amount.amount,
            input_amount.asset,
            destination_address,
            destination_asset,
            tolerance_bps,
            affiliate_bps,
            affiliate_address,
            streaming_interval,
            streaming_quantity
        )

        if not estimate.can_swap:
            raise SwapException(f'Swap is not possible: {estimate.errors}', estimate.errors)

        if self.is_thorchain_asset(input_amount.asset):
            # do a deposit
            return await self._swap_thorchain_asset(input_amount, estimate)
        else:
            # do a transfer / contract call
            return await self._swap_other_asset(input_amount, estimate)

    async def add_liquidity(self):
        ...

    async def remove_liquidity(self):
        ...

    async def borrow(self):
        ...

    async def repay_loan(self):
        ...

    async def add_savers(self):
        ...

    async def remove_savers(self):
        ...

    async def register_name(self, thorname: str, owner: str = '',
                            chain: Chain = Chain.THORChain, chain_address: str = '',
                            preferred_asset: Optional[Asset] = None,
                            expiry: datetime = None):
        """
        Register a THORName with a default expirity of one year. By default,
         chain and chainAddress is getting from wallet instance and is BTC.
        :param thorname: The THORName to register
        :param owner:  The owner of the THORName (optional)
        :param chain: The chain associated with the THORName (optional)
        :param chain_address: The address associated with the THORName (optional)
        :param preferred_asset: Preferred asset associated with the THORName (optional)
        :param expiry:  Expiry date for the THORName (optional)
        :return:
        """

    async def update_name(self, thorname: str, owner: str = '',
                          chain: Chain = Chain.THORChain, chain_address: str = '',
                          preferred_asset: Optional[Asset] = None,
                          expiry: datetime = None):
        """
        Register a THORName
        :param thorname: The THORName to register
        :param owner:  The owner of the THORName (optional)
        :param chain: The chain associated with the THORName (optional)
        :param chain_address: The address associated with the THORName (optional)
        :param preferred_asset: Preferred asset associated with the THORName (optional)
        :param expiry:  Expiry date for the THORName (optional)
        :return:
        """

    # -----------------------------------------

    @staticmethod
    def is_erc20_asset(asset: Asset) -> bool:
        return Chain(asset.chain).is_evm and not is_gas_asset(asset)

    @staticmethod
    def is_thorchain_asset(asset: Asset) -> bool:
        return asset.chain == Chain.THORChain.value or asset.synth

    async def _swap_thorchain_asset(self, input_amount: CryptoAmount, quote: SwapEstimate) -> str:
        client = self.wallet.get_client(Chain.THORChain)
        if not client:
            raise Exception('THORChain client not found')
        if not isinstance(client, THORChainClient):
            raise Exception('Invalid THORChain client')
        return await client.deposit(input_amount, quote.memo)

    async def _swap_other_asset(self, input_amount: CryptoAmount, quote: SwapEstimate) -> str:
        chain = Chain(input_amount.asset.chain)
        client = self.wallet.get_client(chain)
        if not client:
            raise Exception(f'{input_amount.asset.chain} client not found')

        if chain.is_evm:
            # todo: implement EVM chain swap
            raise NotImplementedError('EVM chain swap not supported yet')
        else:
            return await client.transfer(input_amount, quote.details.inbound_address, memo=quote.memo)

    def _dest_chain(self, dest_asset: Asset) -> Chain:
        return Chain.THORChain if self.is_thorchain_asset(dest_asset) else Chain(dest_asset.chain)

    async def _validate_swap(self,
                             input_amount: CryptoAmount,
                             destination_asset: Union[Asset, str], destination_address: str = '',
                             tolerance_bps=0.0,
                             affiliate_bps=0.0,
                             affiliate_address: str = ''):
        if not input_amount.asset.chain or not input_amount.asset.symbol:
            return 'Invalid input asset'

        destination_asset = Asset.automatic(destination_asset)
        if not destination_asset.chain or not destination_asset.symbol:
            return f'Invalid destination asset "{destination_asset}"'

        chain = self._dest_chain(destination_asset)

        if not destination_address:
            return 'Destination address is required'
        else:
            client = self.wallet.get_client(chain)
            if not client:
                return f'Client for {chain} not found'
            elif not client.validate_address(destination_address):
                return f'Address validation failed "{destination_address}" is invalid for "{chain}"'

        if tolerance_bps < 0 or tolerance_bps > THOR_BASIS_POINT_MAX:
            return f'Invalid tolerance: {tolerance_bps}; must be between 0 and {THOR_BASIS_POINT_MAX}'

        if affiliate_bps < 0 or affiliate_bps > THOR_BASIS_POINT_MAX:
            return f'Invalid affiliate fee: {affiliate_bps}; must be between 0 and {THOR_BASIS_POINT_MAX}'

        if affiliate_address:
            is_valid = self.wallet.get_client(Chain.THORChain).validate_address(affiliate_address)
            if not is_valid:
                thor_name = await self.query.cache.get_name_details(affiliate_address)
                if not thor_name:
                    return f'Affiliate address "{affiliate_address}" is not a valid THORChain address'

        if input_amount.amount.internal_amount <= 0:
            return f'Invalid input amount: {input_amount.amount}; must be greater than 0'

        if input_amount.asset.synth:
            return

        if self.is_erc20_asset(input_amount.asset):
            # todo: validate allowance
            return 'ERC20 allowance not implemented yet...'

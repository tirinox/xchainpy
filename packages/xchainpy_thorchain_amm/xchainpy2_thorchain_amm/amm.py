import datetime
from contextlib import suppress
from typing import Union, Optional

from xchainpy2_client import FeeOption
from xchainpy2_thorchain import THORChainClient, THORMemo
from xchainpy2_thorchain_query import THORChainQuery, SwapEstimate, TransactionTracker
from xchainpy2_utils import CryptoAmount, Asset, Chain, is_gas_asset, AssetRUNE
from .consts import THOR_BASIS_POINT_MAX
from .wallet import Wallet


class AMMException(Exception):
    def __init__(self, message, errors: list = None):
        super().__init__(message)
        self.errors = errors


class SwapException(AMMException):
    ...


class THORNameException(AMMException):
    ...


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
        :param streaming_quantity: sub swap quantity, 0 for automatic
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
            return await self._swap_other_asset(input_amount, estimate, fee_option)

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

    async def register_name(self, thorname: str,
                            chain: Chain = Chain.THORChain, chain_address: str = '',
                            owner: str = '',
                            preferred_asset: Optional[Asset] = None,
                            days: float = 365):
        """
        Register a THORName with a default expiry of one year. By default,
         chain and chainAddress is getting from wallet instance and is BTC.
        :param thorname: The THORName to register
        :param chain: The chain associated with the THORName (optional)
        :param chain_address: The address associated with the THORName (optional)
        :param owner: The owner of the THORName; may be different from the sender (optional)
        :param preferred_asset: Preferred asset associated with the THORName (optional)
        :param days: Expiry date for the THORName (optional)
        :return:
        """
        if days <= 0:
            raise THORNameException('Invalid expiry days. If you want to unregister, use unregister_name() instead.')

        expiry = datetime.datetime.now() + datetime.timedelta(days=days)
        estimate = await self.query.estimate_thor_name(False, thorname, expiry)
        if not estimate.can_register:
            raise THORNameException(f'Cannot register THORName: {estimate.reason}')

        return await self.general_thorname_call(
            estimate.cost, thorname, chain, chain_address, owner, preferred_asset,
            estimate.expiry_block_from_date(expiry)
        )

    async def renew_name(self, thorname: str, days: float, thor_address: str = '') -> str:
        """
        Renew a THORName
        :param thorname: The THORName to renew
        :param days: Expiry date for the THORName
        :param thor_address: The THOR address associated with the THORName, if different from the sender
        :return: str TX hash
        """

        if days <= 0:
            raise THORNameException('Invalid expiry days. If you want to unregister, use unregister_name() instead.')

        expiry = datetime.datetime.now() + datetime.timedelta(days=days)
        estimate = await self.query.estimate_thor_name(True, thorname, expiry)
        if not estimate.can_register:
            raise THORNameException(f'Cannot renew THORName: {estimate.reason}')

        if not thor_address:
            thor_address = self._get_thorchain_client().get_address()

        return await self.general_thorname_call(estimate.cost, thorname, Chain.THORChain, thor_address)

    async def unregister_name(self, thorname: str, chain: Optional[Chain] = None, chain_address: str = ''):
        """
        Unregister a THORName
        :param chain: The chain associated with the THORName (optional)
        :param chain_address: The address associated with the THORName (optional)
        :param thorname: The THORName to unregister
        :return: TX hash
        """
        if not chain_address:
            chain_address = self._get_thorchain_client().get_address()

        if not chain:
            chain = Chain.THORChain

        return await self.general_thorname_call(
            CryptoAmount.zero(AssetRUNE),
            thorname,
            chain=chain,
            chain_address=chain_address,
            expiry_block=1242  # define a block in the past to unregister
        )

    async def general_thorname_call(self, payment: CryptoAmount, thorname: str,
                                    chain: Chain = Chain.THORChain, chain_address: str = '',
                                    owner: str = '',
                                    preferred_asset: Optional[Asset] = None,
                                    expiry_block: Optional[int] = None,
                                    check_balance: bool = True):
        """
        General THORName call to register, update, or unregister a THORName
        :param payment: How much to pay for the THORName (normally 10 Rune one time and 1 Rune per year)
        :param thorname: The THORName to register
        :param chain: The chain associated with the THORName (optional)
        :param chain_address: The address associated with the THORName (optional)
        :param owner: The owner of the THORName; may be different from the sender (optional)
        :param preferred_asset: Preferred asset associated with the THORName (optional)
        :param expiry_block: Expiry block for the THORName (optional)
        :param check_balance: Check the balance before sending the transaction (optional)
        :return:
        """
        if not self.validate_thorname(thorname):
            raise THORNameException('Invalid THORName')

        expiry_block = '' if expiry_block is None else str(expiry_block)
        preferred_asset = str(preferred_asset) if preferred_asset else ''

        memo = THORMemo.thorname_register_or_renew(
            thorname, chain.value, chain_address, owner,
            preferred_asset=preferred_asset,
            expiry=expiry_block
        )

        thor_client = self._get_thorchain_client()
        return await thor_client.deposit(payment, memo, check_balance=check_balance)

    @staticmethod
    def validate_thorname(name: str):
        # The THORName's string. Must be Between 1-30 hexadecimal characters and -_+ special characters.;
        if not name:
            return False

        if len(name) < 1 or len(name) > 30:
            return False

        # must contain only letters, digits and +_-
        for c in name:
            if not c.isalnum() and c not in '-_+':
                return False

        return True

    # -----------------------------------------

    @staticmethod
    def is_erc20_asset(asset: Asset) -> bool:
        return Chain(asset.chain).is_evm and not is_gas_asset(asset)

    @staticmethod
    def is_thorchain_asset(asset: Asset) -> bool:
        return asset.chain == Chain.THORChain.value or asset.synth

    def _get_thorchain_client(self) -> THORChainClient:
        client = self.wallet.get_client(Chain.THORChain)
        if not client:
            raise AMMException('THORChain client not found')
        if not isinstance(client, THORChainClient):
            raise AMMException('Invalid THORChain client')
        return client

    async def _swap_thorchain_asset(self, input_amount: CryptoAmount, quote: SwapEstimate) -> str:
        client = self._get_thorchain_client()
        return await client.deposit(input_amount, quote.memo)

    async def _swap_other_asset(self, input_amount: CryptoAmount, quote: SwapEstimate,
                                fee_option=FeeOption.FAST) -> str:
        chain = Chain(input_amount.asset.chain)
        client = self.wallet.get_client(chain)
        if not client:
            raise SwapException(f'{input_amount.asset.chain} client not found')

        if chain.is_evm:
            # todo: implement EVM chain swap
            raise NotImplementedError('EVM chain swap not supported yet')
        else:
            return await client.transfer(input_amount, quote.details.inbound_address, memo=quote.memo,
                                         fee_option=fee_option)

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

    def tracker(self):
        return TransactionTracker(self.query.cache)

    async def close(self):
        with suppress(Exception):
            await self.wallet.close()
        with suppress(Exception):
            await self.query.close()
        with suppress(Exception):
            await self.query.cache.close()

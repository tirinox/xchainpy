import datetime
from contextlib import suppress
from typing import Union, Optional

from xchainpy2_client import FeeOption
from xchainpy2_thorchain import THORChainClient, THORMemo
from xchainpy2_thorchain_query import THORChainQuery, SwapEstimate, TransactionTracker, WithdrawMode
from xchainpy2_utils import CryptoAmount, Asset, Chain, is_gas_asset, AssetRUNE, Amount
from .consts import THOR_BASIS_POINT_MAX
from .models import AMMException, SwapException, THORNameException
from .wallet import Wallet


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

    async def donate(self, amount: CryptoAmount, pool: Union[Asset, str] = '',
                     fee_option=FeeOption.FAST, check_balance=True):
        """
        Donate to a pool
        :param amount: CryptoAmount to donate
        :param pool: Pool name to donate to; can be empty if you donate non-Rune assets
        :param fee_option: Fee option to use for transfer (optional, default: FeeOption.FAST)
        :param check_balance: Check the balance before sending the transaction (optional, default: True)
        :return:
        """
        self._validate_crypto_amount(amount)

        if amount.asset.synth:
            raise AMMException(f'Donating synth assets is not allowed')

        if self.is_thorchain_asset(amount.asset) and not pool:
            raise AMMException(f'Pool name is required for Rune donations')
        else:
            pool = str(amount.asset)

        pools = await self.query.cache.get_pools()
        if not pools:
            raise AMMException('No pools found')

        if pool not in pools:
            raise AMMException(f'No pool found for {pool}')

        memo = THORMemo.donate(pool).build()

        if self.is_thorchain_asset(amount.asset):
            inbound_address = ''
        else:
            inbound_details = await self.query.cache.get_inbound_details()
            if not inbound_details:
                raise AMMException('Could not get inbound details')
            inbound_chain_details = inbound_details.get(amount.asset.chain)
            if not inbound_chain_details:
                raise AMMException(f'No inbound details for {amount.asset.chain}')
            if inbound_chain_details.halted_lp:
                raise AMMException(f'LP actions are halted on {amount.asset.chain} chain')

            inbound_address = inbound_chain_details.address

        return await self.general_deposit(amount, inbound_address, memo, fee_option, check_balance)

    async def add_liquidity_rune_side(self, amount: Amount,
                                      pool: Union[Asset, str],
                                      paired_address: str,
                                      affiliate_address: str = '',
                                      affiliate_bps: int = 0,
                                      check_balance=True):

        self._validate_bps(affiliate_bps, 'affiliate_bps')
        self._validate_crypto_amount(CryptoAmount(amount, AssetRUNE))

        if affiliate_address and not self._validate_affiliate_address(affiliate_address):
            raise AMMException(f'Invalid affiliate address: {affiliate_address}')

        pool_name = Asset.automatic(pool).upper()
        memo = THORMemo.add_liquidity(pool_name, paired_address).build()

        return await self.general_deposit(CryptoAmount(amount, AssetRUNE), '',
                                          memo, FeeOption.FAST, check_balance)

    async def add_liquidity_asset_side(self,
                                       amount: CryptoAmount,
                                       paired_rune_address: str,
                                       affiliate_address: str = '',
                                       affiliate_bps: int = 0,
                                       check_balance=True):
        self._validate_bps(affiliate_bps, 'affiliate_bps')
        self._validate_crypto_amount(amount)

        if affiliate_address:
            if not await self._validate_affiliate_address(affiliate_address):
                raise AMMException(f'Invalid affiliate address: {affiliate_address}')

        pool_name = str(amount.asset)

        memo = THORMemo.add_liquidity(pool_name, paired_rune_address).build()
        return await self.general_deposit(amount, '', memo, FeeOption.FAST, check_balance)

    async def add_liquidity_rune_only(self,
                                      amount: Amount,
                                      pool: Union[Asset, str],
                                      affiliate_address: str = '',
                                      affiliate_bps: int = 0,
                                      check_balance=True):
        return await self.add_liquidity_rune_side(amount, pool, '',
                                                  affiliate_address, affiliate_bps,
                                                  check_balance)

    async def add_liquidity_asset_only(self,
                                       amount: CryptoAmount,
                                       affiliate_address: str = '',
                                       affiliate_bps: int = 0,
                                       check_balance=True):
        raise await self.add_liquidity_asset_side(amount, '', affiliate_address, affiliate_bps, check_balance)

    async def withdraw_liquidity(self,
                                 asset: Union[Asset, str],
                                 mode: WithdrawMode, withdraw_bps: int = THOR_BASIS_POINT_MAX):
        asset = Asset.automatic(asset)

        rune_address = ''
        if mode == WithdrawMode.RuneOnly or mode == WithdrawMode.Symmetric:
            rune_address = self._get_thorchain_client().get_address()

        asset_address = ''
        if mode == WithdrawMode.AssetOnly or mode == WithdrawMode.Symmetric:
            asset_client = self.wallet.get_client(Chain(asset.chain))
            if not asset_client:
                raise AMMException(f'Client for {asset.chain} not found')
            asset_address = asset_client.get_address()

        if not rune_address or not asset_address:
            raise AMMException('Cannot determine addresses for liquidity withdrawal')

        estimate = await self.query.estimate_withdraw_lp(asset, mode, withdraw_bps,
                                                         rune_address, asset_address)

        if not estimate.can_withdraw:
            raise AMMException(f'Cannot withdraw liquidity: {estimate.errors}', estimate.errors)

        return await self.general_deposit(estimate.deposit_amount, estimate.inbound_address, estimate.memo)

    async def open_loan(self,
                        amount: CryptoAmount,
                        target_asset: Union[str, Asset],
                        destination_address: str,
                        min_out: int = 0,
                        affiliate: str = '',
                        affiliate_bps: int = 0,
                        fee_option=FeeOption.FAST):
        """
        Open a loan or add assets to an existing loan.
        Payload is the collateral to open the loan with. Must be L1 supported by THORChain.
        :param amount: Payload, collateral to open the loan with.
        :param target_asset: Target debt asset identifier.	Can be shortened.
        :param destination_address: The destination address to send the debt to. Can use THORName.
        :param min_out: Similar to LIM, Min debt amount, else a refund.	Optional, 1e8 format.
        :param affiliate: The affiliate address. The affiliate is added to the pool as an LP. Optional. Must be THORName or THOR Address.
        :param affiliate_bps: The affiliate fee. Fee is allocated to the affiliate.	Optional. Limited from 0 to 1000 Basis Points.
        :param fee_option: Fee option to use for transfer (optional, default: FeeOption.FAST)
        :return: str TX hash submitted to the network
        """
        raise NotImplementedError('Borrow not implemented yet')

    async def repay_loan(self,
                         amount: CryptoAmount,
                         destination_address: str,
                         min_out: int = 0,
                         fee_option=FeeOption.FAST):
        """
        Repay a loan (or part of it) with assets.
        :param amount: Amount and asset to repay. Target collateral asset identifier. Can be shortened.
        :param destination_address: The destination address to send the collateral to. Can use THORName.
        :param min_out: Similar to LIM, Min collateral to receive else a refund. Optional, 1e8 format,
        loan needs to be fully repaid to close.
        :param fee_option: Fee option to use for transfer (optional, default: FeeOption.FAST)
        :return: str TX hash submitted to the network
        """
        raise NotImplementedError('Repay not implemented yet')

    async def add_savers(self,
                         input_amount: CryptoAmount,
                         fee_option=FeeOption.FAST):
        """
        Adds assets to a savers value
        :param input_amount: CryptoAmount to add to the savers value
        :param fee_option: fee option to use for transfer
        :return: str TX hash submitted to the network
        """
        estimate = await self.query.estimate_add_saver(input_amount)
        if not estimate.can_add_saver:
            raise AMMException(f'Cannot add savers: {estimate.errors}', estimate.errors)

        return await self.general_deposit(input_amount, estimate.to_address, estimate.memo, fee_option)

    async def withdraw_savers(self,
                              asset: Union[Asset, str],
                              address: str,
                              withdraw_bps: int,
                              fee_option=FeeOption.FAST):
        """
        Withdraw assets from a savers value
        :param asset: Asset to withdraw from the savers value
        :param address: Address to withdraw to
        :param withdraw_bps: Percentage of the savers value to withdraw (0-10000)
        :param fee_option: Fee option to use for transfer (optional, default: FeeOption.FAST)
        :return:
        """
        asset = Asset.automatic(asset)

        estimate = await self.query.estimate_withdraw_saver(asset, address, withdraw_bps)
        if not estimate.can_withdraw:
            raise AMMException(f'Cannot withdraw savers: {estimate.errors}', estimate.errors)

        return await self.general_deposit(estimate.dust_amount, estimate.to_address, estimate.memo, fee_option)

    async def general_deposit(self,
                              input_amount: CryptoAmount,
                              to_address: str,
                              memo: str,
                              fee_option=FeeOption.FAST,
                              check_balance=True):
        """
        General deposit function to deposit assets to a specific inbound address with a memo.
        In case of Rune, it will invoke a MsgDeposit in the THORChain.
        In case of other assets, it will invoke a transfer to the inbound address with the memo.
        :param input_amount: Input amount and asset to deposit
        :param to_address: Inbound address to deposit to
        :param memo: Memo to include with the deposit to identify your intent
        :param fee_option: Fee option to use for transfer (optional, default: FeeOption.FAST)
        :param check_balance: Check the balance before sending the transaction (optional, default: True)
        :return:
        """
        chain = Chain(input_amount.asset.chain)

        # noinspection PyTypeChecker
        client = self.wallet.get_client(chain)
        memo = str(memo)

        # determine the inbound address if not provided
        if not to_address:
            inbound_details = await self.query.cache.get_inbound_details()
            if not inbound_details:
                raise AMMException('Could not get inbound details')
            inbound_chain_details = inbound_details.get(chain.value)
            if not inbound_chain_details:
                raise AMMException(f'No inbound details for {chain}')
            if inbound_chain_details.halted_chain:
                raise AMMException(f'Actions are halted on {chain} chain')
            to_address = inbound_chain_details.address

        if not input_amount.asset.chain or not input_amount.asset.symbol:
            raise AMMException(f'Invalid asset: {input_amount.asset}')

        if self.is_thorchain_asset(input_amount.asset):
            client: THORChainClient
            # invoke a THORChain's MsgDeposit call
            return await client.deposit(input_amount, memo, check_balance=check_balance)
        elif chain.is_evm:
            # ToDo: EVM chain case
            raise NotImplementedError('EVM chain add savers not supported yet')
        elif chain.is_utxo:
            fees = await client.get_fees()
            fee = int(fees.fees[fee_option])
            return await client.transfer(input_amount, to_address, memo=memo, fee_rate=fee,
                                         check_balance=check_balance)
        else:
            return await client.transfer(input_amount, to_address, memo=memo,
                                         check_balance=check_balance)

    async def register_name(self,
                            thorname: str,
                            chain: Chain = Chain.THORChain, chain_address: str = '',
                            owner: str = '',
                            days: float = 365):
        """
        Register a THORName with a default expiry of one year. By default,
         chain and chainAddress is getting from wallet instance and is BTC.
        :param thorname: The THORName to register
        :param chain: The chain associated with the THORName (optional)
        :param chain_address: The address associated with the THORName (optional)
        :param owner: The owner of the THORName; may be different from the sender (optional)
        :param days: Expiry date for the THORName (optional)
        :return: str TX hash
        """
        if days <= 0:
            raise THORNameException('Invalid expiry days. If you want to unregister, use unregister_name() instead.')

        expiry = datetime.datetime.now() + datetime.timedelta(days=days)
        estimate = await self.query.estimate_thor_name(False, thorname, expiry)
        if not estimate.can_register:
            raise THORNameException(f'Cannot register THORName: {estimate.reason}')

        return await self.general_thorname_call(
            estimate.cost, thorname, chain, chain_address, owner, None,
            estimate.expiry_block_from_date(expiry)
        )

    async def set_preferred_asset_name(self,
                                       thorname: str, preferred_asset: Union[Asset, str],
                                       chain: Chain, chain_address: str,
                                       owner: str = '') -> str:
        """
        Set the preferred asset for a THORName
        :param thorname: The THORName to set the preferred asset for
        :param preferred_asset: Asset to set as preferred
        :param chain: Chain to set the preferred asset for
        :param chain_address: Address to collect affiliate fee
        :param owner: The owner of the THORName; may be different from the sender (optional)
        :return: str TX hash
        """
        if not preferred_asset:
            raise THORNameException('Invalid preferred asset')

        if not owner:
            owner = self._get_thorchain_client().get_address()

        return await self.general_thorname_call(
            CryptoAmount.zero(AssetRUNE),
            thorname,
            chain=chain,
            chain_address=chain_address,
            owner=owner,
            preferred_asset=preferred_asset
        )

    async def set_name_alias_for_chain(self,
                                       thorname: str, chain: Chain, chain_address: str,
                                       owner: str = '') -> str:
        """
        Add or update an alias for a THORName on a specific chain
        :param thorname: THORName to add or update an alias for
        :param chain: The chain to add or update an alias for
        :param chain_address: The address to add or update an alias for
        :param owner: The owner of the THORName; may be different from the sender (optional)
        :return: str TX hash
        """
        if not owner:
            owner = self._get_thorchain_client().get_address()

        return await self.general_thorname_call(
            CryptoAmount.zero(AssetRUNE),
            thorname,
            chain=chain,
            chain_address=chain_address,
            owner=owner
        )

    async def renew_name(self,
                         thorname: str, days: float, thor_address: str = '') -> str:
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
        :return: str TX hash
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
        :return: str TX hash
        """
        if not self.validate_thorname(thorname):
            raise THORNameException('Invalid THORName')

        expiry_block = '' if expiry_block is None else str(expiry_block)
        preferred_asset = str(preferred_asset) if preferred_asset else ''

        memo = THORMemo.thorname_register_or_renew(
            thorname, chain.value, chain_address, owner,
            preferred_asset=preferred_asset,
            expiry=expiry_block
        ).build()

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

    def tracker(self):
        return TransactionTracker(self.query.cache)

    async def close(self):
        with suppress(Exception):
            await self.wallet.close()
        with suppress(Exception):
            await self.query.close()
        with suppress(Exception):
            await self.query.cache.close()

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
                             tolerance_bps=0,
                             affiliate_bps=0,
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

        self._validate_bps(tolerance_bps, 'tolerance_bps')
        self._validate_bps(affiliate_bps, 'affiliate_bps')

        if affiliate_address:
            if not await self._validate_affiliate_address(affiliate_address):
                return f'Affiliate address "{affiliate_address}" is not a valid THORChain address'

        if input_amount.amount.internal_amount <= 0:
            return f'Invalid input amount: {input_amount.amount}; must be greater than 0'

        if input_amount.asset.synth:
            return

        if self.is_erc20_asset(input_amount.asset):
            # todo: validate allowance
            return 'ERC20 allowance not implemented yet...'

    async def _validate_affiliate_address(self, affiliate_address: str) -> bool:
        if affiliate_address:
            is_valid = self._get_thorchain_client().validate_address(affiliate_address)
            if not is_valid:
                thor_name = await self.query.cache.get_name_details(affiliate_address)
                if not thor_name:
                    return True
            return False
        else:
            return True

    @staticmethod
    def _validate_bps(bps: int, tag: str = ''):
        if bps < 0 or bps > THOR_BASIS_POINT_MAX:
            raise AMMException(f'Invalid basis points ({tag}): {bps}; must be between 0 and {THOR_BASIS_POINT_MAX}')
        return True

    @staticmethod
    def _validate_crypto_amount(amount: CryptoAmount, allow_synthetic: bool = False):
        if amount.amount.internal_amount <= 0:
            raise AMMException(f'Invalid amount: {amount.amount}')

        if not amount.asset.chain or not amount.asset.symbol:
            raise AMMException(f'Invalid asset: {amount.asset}')

        if not allow_synthetic and amount.asset.synth:
            raise AMMException(f'Synthetic assets are not allowed: {amount.asset}')

        return True

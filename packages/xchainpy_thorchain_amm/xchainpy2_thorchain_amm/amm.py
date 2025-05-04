import datetime
from contextlib import suppress
from typing import Union, Optional

from xchainpy2_client import FeeOption
# todo fix this!
from xchainpy2_ethereum import EthereumClient, GasOptions
from xchainpy2_thorchain import THORChainClient, THORMemo
from xchainpy2_thorchain_query import THORChainQuery, TransactionTracker, WithdrawMode
from xchainpy2_thornode import Amount
from xchainpy2_utils import CryptoAmount, Asset, Chain, AssetRUNE, remove_0x_prefix, AssetTCY
from xchainpy2_utils.versions import deprecated
from xchainpy2_wallet import Wallet
from .consts import THOR_BASIS_POINT_MAX, DEFAULT_TOLERANCE_BPS, THOR_SWAP_TRACKER_URL, DEFAULT_EXPIRY
from .evm_helper import EVMHelper
from .models import AMMException, THORNameException
from .utils import is_erc20_asset


class THORChainAMM:
    def __init__(self, wallet: Wallet, query: Optional[THORChainQuery] = None,
                 dry_run: bool = False,
                 check_balance: bool = True,
                 check_allowance: bool = True,
                 fee_option: FeeOption = FeeOption.FAST):
        """
        THORChain Automated Market Maker (AMM) interface.
        The AMM interface provides a set of functions to interact with the THORChain protocol.

        :param wallet: Wallet instance is mandatory
        :param query: THORChainQuery instance (optional)
        :param dry_run: If True, the transaction will not be submitted to the network, default is False
        :param check_balance: This flag is used to check the balance before submitting a transaction, default is True
        :param check_allowance: This flag is used to check the allowance before submitting a ERC20 transaction, default is True
        :param fee_option: Default fee option to use for transactions, default is FeeOption.FAST
        """

        self.query = query or wallet.query_api or THORChainQuery()
        self.wallet = wallet
        self.dry_run = dry_run
        self.check_balance = check_balance
        self.check_allowance = check_allowance
        self.fee_option = fee_option
        self.swap_tracker_url = THOR_SWAP_TRACKER_URL
        self.evm_expiration_sec = DEFAULT_EXPIRY

    def get_track_url(self, tx_id) -> str:
        """
        Get the URL to the website to track the transaction.

        :param tx_id: Transaction ID
        :return: str URL to track the transaction
        """
        if not tx_id:
            raise ValueError('Invalid transaction ID')

        tx_id = remove_0x_prefix(tx_id)

        return self.swap_tracker_url.format(
            tx_id=tx_id,
            network=self.query.cache.network.value,
        )

    # ---------------------------- SWAPS ----------------------------

    async def swap(self,
                   input_amount: CryptoAmount,
                   destination_asset: Union[Asset, str],
                   destination_address: str = '',
                   tolerance_bps=DEFAULT_TOLERANCE_BPS,
                   affiliate_bps=0,
                   affiliate_address: str = '',
                   streaming_interval=0,
                   streaming_quantity=0,
                   gas_options: Optional[GasOptions] = None,
                   allowance_check=True) -> str:
        # todo: add an ability to override swap limit
        """
        Do a swap using the THORChain protocol AMM.
        In case of EVM ERC20-like tokens, it will approve the token and then do the swap.
        # todo: explain the swap process better

        :param input_amount: input amount and asset to swap
        :param destination_asset: output asset to swap to
        :param destination_address: destination address to send swapped asset to
        :param tolerance_bps: price tolerance in basis points (0-10000), default is 500 which is 0.5%
        :param affiliate_bps: affiliate fee in basis points (0-10000), default 0
        :param affiliate_address: affiliate address to collect affiliate fee
        :param streaming_interval: streaming interval in THORChain blocks (6 sec), 0 to disable streaming
        :param streaming_quantity: sub swap quantity, 0 for automatic
        :param gas_options: gas options. You can set gas price explicitly or use automatic fee option
        :param allowance_check: Check allowance before swap ERC20 token, default is True
        :return: hash of the inbound transaction (used to track transaction status)
        """
        if not destination_address:
            dest_chain = self._dest_chain(Asset.automatic(destination_asset))
            dest_client = self.wallet.get_client(dest_chain)
            if not dest_client:
                raise AMMException('No destination address')
            destination_address = dest_client.get_address()

        validation_error = await self._validate_swap(input_amount, destination_asset, destination_address,
                                                     tolerance_bps, affiliate_bps,
                                                     affiliate_address)

        if validation_error:
            raise AMMException(f'Invalid swap: {validation_error}')

        estimate = await self.query.quote_swap(
            input_amount,
            destination_address,
            destination_asset,
            tolerance_bps,
            affiliate_bps,
            affiliate_address,
            streaming_interval,
            streaming_quantity
        )

        if not estimate.can_swap:
            raise AMMException(f'Swap is not possible: {estimate.errors}', estimate.errors)

        return await self.general_deposit(input_amount, estimate.details.inbound_address, estimate.memo, gas_options)

    @deprecated("Use swap() method instead")
    async def do_swap(self, *args, **kwargs) -> str:
        """
        This method is obsolete and will be removed in the future.
        Please use "swap" method instead.
        """
        return await self.swap(*args, **kwargs)

    # ---------------------------- LIQUIDITY ----------------------------

    async def donate(self, amount: CryptoAmount, pool: Union[Asset, str] = '',
                     gas_options: Optional[GasOptions] = None) -> str:
        """
        Donate some crypto to the pool. You can donate Rune or non-Rune assets.
        Caution! After donating, you will not be able to withdraw the donation! This is irreversible.

        :param amount: CryptoAmount to donate
        :param pool: Pool name to donate to; can be empty if you donate non-Rune assets
        :param gas_options: gas options. You can set gas price explicitly or use automatic fee option
        :return: TX hash submitted to the network
        """
        self._validate_crypto_amount(amount)

        if not amount.asset.is_native:
            raise AMMException(f'Donating "{amount.asset.kind}" assets is not allowed')

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

        inbound_address = await self._get_inbound_address(amount.asset)
        return await self.general_deposit(amount, inbound_address, memo, gas_options)

    async def add_liquidity_rune_side(self, amount: CryptoAmount,
                                      pool: Union[Asset, str],
                                      paired_address: str,
                                      affiliate_address: str = '',
                                      affiliate_bps: int = 0,
                                      gas_options: Optional[GasOptions] = None) -> str:
        """
        Add liquidity to a pool on the Rune side.
        Attention: you must also add liquidity to the paired asset side (add_liquidity_asset_side)
        to complete the liquidity addition! If you don't, your funds will be stuck in the pool.

        :param amount: Amount of Rune to add
        :param pool: Pool name to add liquidity to
        :param paired_address: Address of the paired asset
        :param affiliate_address: Affiliate address to collect affiliate fee (optional)
        :param affiliate_bps: Affiliate fee in basis points (optional; default: 0)
        :param gas_options: gas options. You can set gas price explicitly or use automatic fee option
        :return: TX hash submitted to the network
        """
        self._validate_crypto_amount(amount)

        if amount.asset != AssetRUNE:
            raise AMMException(f'Invalid asset: {amount.asset}; must be Rune')

        self._validate_bps(affiliate_bps, 'affiliate_bps')

        if affiliate_address:
            if not await self._validate_affiliate_address(affiliate_address):
                raise AMMException(f'Invalid affiliate address: {affiliate_address}')

        pool_name = Asset.automatic(pool).upper()
        memo = THORMemo.add_liquidity(pool_name, paired_address).build()

        return await self.general_deposit(amount, '', memo, gas_options)

    async def add_liquidity_asset_side(self,
                                       amount: CryptoAmount,
                                       paired_rune_address: str,
                                       affiliate_address: str = '',
                                       affiliate_bps: int = 0,
                                       gas_options: Optional[GasOptions] = None) -> str:
        """
        Add liquidity to a pool on the asset side.
        Attention: you must also add liquidity to the Rune side (add_liquidity_rune_side); if you don't,
        your funds will be stuck in the pool.

        :param amount: Amount of the asset to add
        :param paired_rune_address: Address of the paired Rune
        :param affiliate_address: Affiliate address to collect affiliate fee (optional)
        :param affiliate_bps: Affiliate fee in basis points (optional; default: 0)
        :param gas_options: gas options. You can set gas price explicitly or use automatic fee option
        :return: TX hash submitted to the network
        """

        self._validate_bps(affiliate_bps, 'affiliate_bps')
        self._validate_crypto_amount(amount)

        if affiliate_address:
            if not await self._validate_affiliate_address(affiliate_address):
                raise AMMException(f'Invalid affiliate address: {affiliate_address}')

        pool_name = str(amount.asset)

        memo = THORMemo.add_liquidity(pool_name, paired_rune_address).build()
        return await self.general_deposit(amount, '', memo, gas_options)

    async def add_liquidity_rune_only(self,
                                      amount: CryptoAmount,
                                      pool: Union[Asset, str],
                                      affiliate_address: str = '',
                                      affiliate_bps: int = 0,
                                      gas_options: Optional[GasOptions] = None) -> str:
        """
        Add liquidity to a pool on the Rune side only.

        :param amount: Amount of Rune to add
        :param pool: Pool name to add liquidity to
        :param affiliate_address: Affiliate address to collect affiliate fee (optional)
        :param affiliate_bps: Affiliate fee in basis points (optional; default: 0)
        :param gas_options: gas options. You can set gas price explicitly or use automatic fee option
        :return: String TX hash submitted to the network
        """
        if amount.asset != AssetRUNE:
            raise AMMException(f'Invalid asset: {amount.asset}; must be Rune')

        return await self.add_liquidity_rune_side(amount, pool, '',
                                                  affiliate_address, affiliate_bps, gas_options)

    async def add_liquidity_asset_only(self,
                                       amount: CryptoAmount,
                                       affiliate_address: str = '',
                                       affiliate_bps: int = 0,
                                       gas_options: Optional[GasOptions] = None) -> str:
        """
        Add liquidity to a pool on the asset side only.

        :param amount: CryptoAmount of the asset to add
        :param affiliate_address: Affiliate address to collect affiliate fee (optional)
        :param affiliate_bps: Affiliate fee in basis points (optional; default: 0)
        :param gas_options: gas options. You can set gas price explicitly or use automatic fee option
        :return: String TX hash submitted to the network
        :rtype: str
        """

        raise await self.add_liquidity_asset_side(amount, '',
                                                  affiliate_address, affiliate_bps, gas_options)

    async def add_liquidity_symmetric(self,
                                      asset_amount: CryptoAmount,
                                      rune_amount: CryptoAmount,
                                      affiliate_address: str = '',
                                      affiliate_bps: int = 0,
                                      gas_options: Optional[GasOptions] = None) -> (str, str):
        """
        Add liquidity to a pool on both sides (Rune and asset) at the same time.
        This is 2-step operation: first, Rune side, then asset side.
        Note: liquidity addition is not atomic; if one side fails, the other side will still be added.
        Note: this method do not guarantee that your addition is symmetric; you need to check it yourself.

        :param asset_amount: Amount of the asset to add
        :param rune_amount: Amount of Rune to add
        :param affiliate_address: Affiliate address to collect affiliate fee (optional)
        :param affiliate_bps: Affiliate fee in basis points (optional; default: 0)
        :param gas_options: gas options. You can set gas price explicitly or use automatic fee option
        :return: Tuple of TX hashes submitted to the network
        """
        asset_chain = Chain(asset_amount.asset.chain)
        asset_client = self.wallet.get_client(asset_chain)
        if not asset_client:
            raise AMMException(f'Client for {asset_chain} not found')

        asset_address = asset_client.get_address()
        rune_address = self.default_thor_address

        stage1 = await self.add_liquidity_rune_side(rune_amount, '',
                                                    asset_address,
                                                    affiliate_address, affiliate_bps, gas_options)
        if not stage1:
            raise AMMException('Rune side liquidity addition failed.')

        stage2 = await self.add_liquidity_asset_side(asset_amount,
                                                     rune_address,
                                                     affiliate_address, affiliate_bps, gas_options)
        return stage1, stage2

    async def withdraw_liquidity(self,
                                 asset: Union[Asset, str],
                                 mode: WithdrawMode, withdraw_bps: int = THOR_BASIS_POINT_MAX,
                                 gas_options: Optional[GasOptions] = None) -> str:
        """
        Withdraw liquidity from a pool

        :param asset: The pool name to withdraw liquidity from
        :param mode: Withdraw mode (RuneOnly, AssetOnly, Symmetric)
        :param withdraw_bps: Percentage of the pool to withdraw (0-10000)
        :param gas_options: gas options. You can set gas price explicitly or use automatic fee option
        :return: TX hash submitted to the network
        """
        asset = Asset.automatic(asset)

        rune_address = ''
        if mode == WithdrawMode.RuneOnly or mode == WithdrawMode.Symmetric:
            rune_address = self.default_thor_address

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

        return await self.general_deposit(estimate.deposit_amount, estimate.inbound_address, estimate.memo,
                                          gas_options)

    # ---------------------------- TRADE ACCOUNT ----------------------------

    async def deposit_to_trade_account(self, what: CryptoAmount,
                                       target_thor_address: str = None,
                                       gas_options: Optional[GasOptions] = None) -> str:
        """
        Deposit assets to the trade account.
        Trade Accounts provide professional traders (mostly arbitrage bots) a method to execute instant trades on
        THORChain without involving Layer1 transactions on external blockchains. Trade Accounts create a new type
        of asset, backed by the network security rather than the liquidity in a pool (Synthetics),
        or by the RUNE asset (Derived Assets).
        See: https://dev.thorchain.org/concepts/trade-accounts.html

        :param what: CryptoAmount to deposit (it must be normal L1 asset, not synth, not rune, etc.)
        :type what: CryptoAmount
        :param target_thor_address: Target THORChain address that will receive the deposit of the trade asset
        :type target_thor_address: Optional[str]
        :param gas_options: gas options. You can set gas price explicitly or use automatic fee option
        :type gas_options: Optional[GasOptions]
        :return: str TX hash submitted to the network
        :rtype str
        """
        if not what:
            raise AMMException('Invalid amount to deposit')

        if not what.asset.is_native:
            raise AMMException(f'Invalid asset: {what.asset}! It must be a normal asset.')

        if not target_thor_address:
            target_thor_address = self.default_thor_address

        memo = THORMemo.deposit_trade_account(target_thor_address)
        inbound_address = await self._get_inbound_address(what.asset)
        return await self.general_deposit(what, inbound_address, memo, gas_options)

    async def withdraw_from_trade_account(self, what: CryptoAmount,
                                          target_l1_address: str = None,
                                          gas_options: Optional[GasOptions] = None) -> str:
        """
        Withdraw assets from the trade account.
        See: https://dev.thorchain.org/concepts/trade-accounts.html

        :param what:
        :param target_l1_address:
        :param gas_options:
        :return:
        """
        if not what:
            raise AMMException('Invalid amount to withdraw')

        if not what.asset.is_trade:
            raise AMMException(f'Invalid asset: {what.asset}! It must be a trade asset.')

        chain = Chain(what.asset.chain)
        if not target_l1_address:
            cli = self.wallet.get_client(chain)
            if not cli:
                raise AMMException(f'Client for {chain} not found')
            target_l1_address = cli.get_address()
            if not target_l1_address:
                raise AMMException(f'Cannot determine address for {chain} client')

        memo = THORMemo.withdraw_trade_account(target_l1_address)
        return await self.general_deposit(what, '', memo, gas_options)

    # ---------------------------- RUNEPOOL ----------------------------

    async def deposit_to_runepool(self, what: CryptoAmount) -> str:
        """
        Deposit assets to the RUNEPool.
        Attention! After depositing, you will not be able to withdraw the deposit until the lock up period ends.
        See constant/Mimir: RUNEPoolDepositMaturityBlocks

        :param what: CryptoAmount to deposit, Rune only
        :return: str TX hash submitted to the network
        """

        self._validate_crypto_amount(what)
        if not what.asset.is_rune_native:
            raise AMMException('Invalid amount to deposit. Only Rune is allowed.')

        memo = THORMemo.runepool_add()
        return await self.general_deposit(what, '', memo)

    async def withdraw_from_runepool(self, bp: int, affiliate_bps=0, affiliate_address: str = '') -> str:
        """
        Withdraw assets from the RUNEPool.
        Attention! After depositing, you will not be able to withdraw the deposit until the lock up period ends.
        See constant/Mimir: RUNEPoolDepositMaturityBlocks

        :param bp: Basis points to withdraw (0-10000)
        :param affiliate_bps: Affiliate fee in basis points (0-10000), default 0
        :param affiliate_address: Affiliate address to collect affiliate fee THORName or THOR address
        :return: str TX hash submitted to the network
        """
        self._validate_bps(bp, 'bp')
        self._validate_bps(affiliate_bps, 'affiliate_bps')

        if affiliate_address:
            if not await self._validate_affiliate_address(affiliate_address):
                raise AMMException(f'Invalid affiliate address: {affiliate_address}')

        memo = THORMemo.runepool_withdraw(bp, affiliate_address, affiliate_bps)
        return await self.general_deposit(CryptoAmount.zero(AssetRUNE), '', memo)

    # ---------------------------- LOANS ----------------------------

    async def open_loan(self,
                        amount: CryptoAmount,
                        target_asset: Union[str, Asset],
                        destination_address: str,
                        min_out: int = 0,
                        affiliate: str = '',
                        affiliate_bps: int = 0,
                        gas_options: Optional[GasOptions] = None) -> str:
        """
        Open a loan or add assets to an existing loan.
        Payload is the collateral to open the loan with. Must be L1 supported by THORChain.
        You deposit the collateral and receive the debt in the target asset (At least Min_out USD)

        :param amount: Payload, collateral to open the loan with.
        :param target_asset: Target debt asset identifier. Can be shortened.
        :param destination_address: The destination address to send the debt to. Can use THORName.
        :param min_out: Minimum debt amount, else a refund. Optional, 1e8 format.
        :param affiliate: The affiliate address. The affiliate is added to the pool as an LP. Optional.
        Must be THORName or THOR Address.
        :param affiliate_bps: The affiliate fee. Fee is allocated to the affiliate.	Optional.
        Limited from 0 to 1000 Basis Points.
        :param gas_options: gas options. You can set gas price explicitly or use automatic fee option
        :return: str TX hash submitted to the network
        """
        memo = THORMemo.loan_open(target_asset, destination_address, min_out, affiliate, affiliate_bps).build()
        return await self.general_deposit(amount, '', memo, gas_options)

    async def repay_loan(self,
                         amount: CryptoAmount,
                         collateral_asset: Union[str, Asset],
                         destination_address: str,
                         min_out: int = 0,
                         gas_options: Optional[GasOptions] = None) -> str:
        """
        Repay the debt and receive the collateral back.

        :param amount: Amount and asset to repay. Target collateral asset identifier. Can be shortened.
        :param collateral_asset: The target collateral asset identifier. Can be shortened.
        :param destination_address: The destination address to send the collateral to. Owner of the loan.
        :param min_out: Min collateral to receive else a refund. Optional, 1e8 format. Loan needs to be fully repaid to close.
        :param gas_options: gas options. You can set gas price explicitly or use automatic fee option
        :return: str TX hash submitted to the network
        """
        memo = THORMemo.loan_close(collateral_asset, destination_address, min_out).build()
        return await self.general_deposit(amount, '', memo, gas_options)

    async def add_savers(self, input_amount: CryptoAmount, gas_options: Optional[GasOptions] = None) -> str:
        """
        Adds assets to a savers value.

        :param input_amount: CryptoAmount to add to the savers value
        :param gas_options: gas options. You can set gas price explicitly or use automatic fee option
        :return: str TX hash submitted to the network
        """
        estimate = await self.query.estimate_add_saver(input_amount)
        if not estimate.can_add_saver:
            raise AMMException(f'Cannot add savers: {estimate.errors}', estimate.errors)

        return await self.general_deposit(input_amount, estimate.to_address, estimate.memo, gas_options)

    async def withdraw_savers(self,
                              asset: Union[Asset, str],
                              address: str,
                              withdraw_bps: int,
                              gas_options: Optional[GasOptions] = None) -> str:
        """
        Withdraw assets from a savers value.

        :param asset: Asset to withdraw from the savers value
        :param address: Address to withdraw to
        :param withdraw_bps: Percentage of the savers value to withdraw (0-10000)
        :param gas_options: gas options. You can set gas price explicitly or use automatic fee option
        :return: str TX hash submitted to the network
        """
        asset = Asset.automatic(asset)

        estimate = await self.query.estimate_withdraw_saver(asset, address, withdraw_bps)
        if not estimate.can_withdraw:
            raise AMMException(f'Cannot withdraw savers: {estimate.errors}', estimate.errors)

        return await self.general_deposit(estimate.dust_amount, estimate.to_address, estimate.memo, gas_options)

    async def general_deposit(self,
                              input_amount: CryptoAmount,
                              to_address: str,
                              memo: Union[str, THORMemo],
                              gas_options: Optional[GasOptions] = None) -> str:
        """
        General deposit function to deposit assets to a specific inbound address with a memo.
        In case of Rune, it will invoke a MsgDeposit in the THORChain.
        In case of other assets, it will invoke a transfer to the inbound address with the memo.

        :param input_amount: Input amount and asset to deposit
        :type input_amount: CryptoAmount
        :param to_address: Inbound address to deposit to. It can be an empty string when depositing native Thor assets.
        :type to_address: str
        :param memo: Memo to include with the deposit to identify your intent
        :type memo: str or THORMemo
        :param gas_options: gas options. You can set gas price explicitly or use automatic fee option
        :type gas_options: Optional[GasOptions]
        :return: str TX hash submitted to the network
        """

        chain = Chain(input_amount.asset.chain)
        is_thor = self.is_thorchain_asset(input_amount.asset)
        if not is_thor:
            if not to_address:
                # determine the inbound address if not provided
                to_address = await self._get_inbound_address(input_amount.asset)

        if is_thor:
            # this is synth or trade asset, so we manage it with THORChain client
            chain = Chain.THORChain

        # noinspection PyTypeChecker
        client = self.wallet.get_client(chain)

        if not input_amount.asset.chain or not input_amount.asset.symbol:
            raise AMMException(f'Invalid asset: {input_amount.asset}')

        memo = str(memo)

        if is_thor:
            client: THORChainClient

            if self.dry_run:
                return f'Dry-run: THORChain deposit {input_amount} with memo {memo!r}'

            # invoke a THORChain's MsgDeposit call
            return await client.deposit(input_amount, memo, check_balance=self.check_balance)
        elif chain.is_evm:
            return await self._deposit_evm(input_amount, memo, gas_options)
        else:
            if chain.is_utxo:
                fees = await client.get_fees()
                fee_rate = int(fees.fees[self.fee_option])
            else:
                fee_rate = None

            if self.dry_run:
                chain_tag = 'UTXO' if chain.is_utxo else 'Other'
                return (f'Dry-run: transfer (chain: {chain_tag}) '
                        f'{input_amount} to {to_address!r} with memo {memo!r};'
                        f'fee_rate: {fee_rate}')

            return await client.transfer(input_amount, to_address,
                                         memo=memo, fee_rate=fee_rate,
                                         check_balance=self.check_balance)

    async def _deposit_evm(self, input_amount: CryptoAmount, memo: str, gas_options: Optional[GasOptions] = None):
        if self.dry_run:
            return f'Dry-run: EVM deposit {input_amount} with memo {memo!r}; expiration: {self.evm_expiration_sec}'

        # todo: add check_balance

        # noinspection PyTypeChecker
        helper = self._get_evm_helper(input_amount.asset)
        gas_options = gas_options or GasOptions.automatic(self.fee_option)
        tx_hash = await helper.deposit(input_amount, memo, gas_options, self.evm_expiration_sec,
                                       check_allowance=self.check_allowance)
        return tx_hash

    # ---------------------------- THORNAME ----------------------------

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
        Set the preferred asset for a THORName.

        :param thorname: The THORName to set the preferred asset for
        :param preferred_asset: Asset to set as preferred
        :param chain: Chain to set the preferred asset for
        :param chain_address: Address to collect affiliate fee
        :param owner: The owner of the THORName; may be different from the sender (optional)
        :return: str hash of the transaction
        """
        if not preferred_asset:
            raise THORNameException('Invalid preferred asset')

        if not owner:
            owner = self.default_thor_address

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
        Add or update an alias for a THORName on a specific chain.

        :param thorname: THORName to add or update an alias for
        :param chain: The chain to add or update an alias for
        :param chain_address: The address to add or update an alias for
        :param owner: The owner of the THORName; may be different from the sender (optional)
        :return: str TX hash
        """
        if not owner:
            owner = self.default_thor_address

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
        Renew a THORName.

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
            thor_address = self.default_thor_address

        return await self.general_thorname_call(estimate.cost, thorname, Chain.THORChain, thor_address)

    async def unregister_name(self, thorname: str, chain: Optional[Chain] = None, chain_address: str = ''):
        """
        Unregister a THORName.

        :param chain: The chain associated with the THORName (optional)
        :param chain_address: The address associated with the THORName (optional)
        :param thorname: The THORName to unregister
        :return: str TX hash
        """
        if not chain_address:
            chain_address = self.default_thor_address

        if not chain:
            chain = Chain.THORChain

        return await self.general_thorname_call(
            CryptoAmount.zero(AssetRUNE),
            thorname,
            chain=chain,
            chain_address=chain_address,
            expiry_block=1242  # define a block in the past to unregister
        )

    # ---------------------------- ERC20 ALLOWANCE ----------------------------

    async def is_tc_router_approved_to_spend(self, amount: CryptoAmount):
        """
        Check if the TC Router is approved to spend the amount of the asset.

        :param amount: CryptoAmount to check
        :return: True if the TC Router is approved to spend the amount
        """
        if not amount or not amount.asset or amount.amount.internal_amount <= 0:
            raise ValueError(f'Invalid amount: {amount}')

        if not self.is_erc20_asset(amount.asset):
            raise ValueError(f'Asset {amount.asset} is not an ERC20 asset')

        helper = self._get_evm_helper(amount.asset)
        return await helper.is_tc_router_approved_to_spend(amount)

    async def approve_tc_router_to_spend(self, amount: CryptoAmount, gas_options: Optional[GasOptions] = None):
        """
        Approve the TC Router to spend the amount of the asset.

        :param amount: CryptoAmount to approve
        :param gas_options: gas options. You can set gas price explicitly or use automatic fee option
        :return: str TX hash submitted to the network
        """
        if not amount or not amount.asset or amount.amount.internal_amount <= 0:
            raise ValueError(f'Invalid amount: {amount}')

        if not self.is_erc20_asset(amount.asset):
            raise ValueError(f'Asset {amount.asset} is not an ERC20 asset')

        helper = self._get_evm_helper(amount.asset)
        return await helper.approve_tc_router(amount, gas_options)

    # ------------------------------ TCY ------------------------------

    async def tcy_claim(self, thor_address: str = '', gas_options: Optional[GasOptions] = None) -> str:
        """
        Claim TCY tokens. Call this from your L1 address.
        TCY live in the THORChain blockchain so you will need thor_address to claim them.

        :param thor_address: Target THORChain address to send the TCY tokens to. By default, it will be the default THORChain address.
        :param gas_options: Gas options. You can set gas price explicitly or use automatic fee option
        :return: str TX hash
        """
        if not thor_address:
            thor_address = self.default_thor_address

        memo = THORMemo.tcy_claim(thor_address).build()
        inbound_address = await self._get_inbound_address(AssetRUNE)
        return await self.general_deposit(CryptoAmount.zero(AssetRUNE), inbound_address, memo, gas_options)

    async def tcy_stake(self, amount: Union[int, float, Amount, CryptoAmount]) -> str:
        """
        Stake TCY tokens. This method invokes a deposit from your THORChain account
        :param amount: amount of TCY to stake
        :return: str TX hash
        """
        if not isinstance(amount, CryptoAmount):
            amount = CryptoAmount.automatic(amount, AssetTCY, self._get_thorchain_client().decimal)
        elif amount.asset != AssetTCY:
            raise ValueError(f'Asset {amount.asset} is not {AssetTCY}')

        memo = THORMemo.tcy_stake().build()
        return await self.general_deposit(amount, '', memo)

    async def tcy_unstake(self, bp_units: int) -> str:
        """
        Unstake TCY tokens.
        :param bp_units: amount of TCY to unstake in basic points 0..10000 where 10k is 100%
        :return: str TX hash
        """
        if not isinstance(bp_units, int) or bp_units <= 0:
            raise ValueError(f'Invalid amount: {bp_units}')

        memo = THORMemo.tcy_unstake(bp_units).build()
        return await self.general_deposit(CryptoAmount.zero(AssetRUNE), '', memo)

    # ---------------------------- GENERAL ----------------------------

    async def general_thorname_call(self, payment: CryptoAmount, thorname: str,
                                    chain: Chain = Chain.THORChain, chain_address: str = '',
                                    owner: str = '',
                                    preferred_asset: Optional[Asset] = None,
                                    expiry_block: Optional[int] = None):
        """
        General THORName call to register, update, or unregister a THORName.

        :param payment: How much to pay for the THORName (normally 10 Rune one time and 1 Rune per year)
        :param thorname: The THORName to register
        :param chain: The chain associated with the THORName (optional)
        :param chain_address: The address associated with the THORName (optional)
        :param owner: The owner of the THORName; may be different from the sender (optional)
        :param preferred_asset: Preferred asset associated with the THORName (optional)
        :param expiry_block: Expiry block for the THORName (optional)
        :return: str TX hash
        """
        if not self.validate_thorname(thorname):
            raise THORNameException('Invalid THORName')

        if payment.asset != AssetRUNE:
            raise THORNameException('Invalid payment asset; must be Rune')

        expiry_block = '' if expiry_block is None else str(expiry_block)
        preferred_asset = str(preferred_asset) if preferred_asset else ''

        memo = THORMemo.thorname_register_or_renew(
            thorname, chain.value, chain_address, owner,
            preferred_asset=preferred_asset,
            expiry=expiry_block
        ).build()

        return await self.general_deposit(payment, '', memo)

    @staticmethod
    def validate_thorname(name: str):
        """
        Validate a THORName. It must be between 1-30 hexadecimal characters and -_+ special characters.

        :param name: THORName to validate
        :return: bool True if the THORName is valid
        """
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
        """
        Get a transaction tracker to track the status of a swap transaction

        :return: TransactionTracker
        """
        return TransactionTracker(self.query.cache)

    async def close(self):
        """
        Close the wallet and connections.

        :return: None
        """
        with suppress(Exception):
            await self.wallet.close()
        with suppress(Exception):
            await self.query.close()
        with suppress(Exception):
            await self.query.cache.close()

    @property
    def default_thor_address(self) -> str:
        """
        Get the default THORChain address from the wallet.
        :return: str address
        """
        address = self._get_thorchain_client().get_address()
        if not address:
            raise AMMException('No default THORChain address!')
        return address

    @staticmethod
    def is_erc20_asset(asset: Asset) -> bool:
        """
        Check if the asset is an ERC20-like token. Basically, it calls is_erc20_asset from xchainpy2_utils.

        :param asset:
        :return:
        """
        return is_erc20_asset(asset)

    @staticmethod
    def is_thorchain_asset(asset: Asset) -> bool:
        """
        Check if the asset is a THORChain asset. Namely, it's either native Rune or a synthetic asset.
        :param asset: Asset to check
        :return: bool True if the asset is a THORChain asset
        """
        return asset.chain.upper() == Chain.THORChain.value or asset.is_synth or asset.is_trade

    # ---------------------------- PRIVATE ----------------------------

    def _get_thorchain_client(self) -> THORChainClient:
        client = self.wallet.get_client(Chain.THORChain)
        if not client:
            raise AMMException('THORChain client not found')
        if not isinstance(client, THORChainClient):
            raise AMMException('Invalid THORChain client')
        return client

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

        if input_amount.asset.is_native:
            return

        if self.is_erc20_asset(input_amount.asset):
            if not await self.is_tc_router_approved_to_spend(input_amount):
                return f'TC Router is not allowed to spend {input_amount}'

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
        if not amount or not amount.amount or not amount.asset:
            raise AMMException(f'Invalid amount: {amount}')

        if amount.amount.internal_amount <= 0:
            raise AMMException(f'Invalid amount: {amount.amount}')

        if not amount.asset.chain or not amount.asset.symbol:
            raise AMMException(f'Invalid asset: {amount.asset}')

        if not allow_synthetic and amount.asset.synth:
            raise AMMException(f'Synthetic assets are not allowed: {amount.asset}')

        return True

    async def _get_inbound_address(self, asset: Asset) -> str:
        if self.is_thorchain_asset(asset):
            return ''
        else:
            inbound_details = await self.query.cache.get_inbound_details()
            if not inbound_details:
                raise AMMException('Could not get inbound details')
            inbound_chain_details = inbound_details.get(asset.chain)
            if not inbound_chain_details:
                raise AMMException(f'No inbound details for {asset.chain}')
            if inbound_chain_details.halted_lp:
                raise AMMException(f'LP actions are halted on {asset.chain} chain')

            return inbound_chain_details.address

    def _get_evm_helper(self, asset: Asset):
        # noinspection PyTypeChecker
        client: EthereumClient = self.wallet.get_client(asset)
        return EVMHelper(client, self.query.cache)

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()
        return False

    def __enter__(self):
        raise Exception('Use async with')

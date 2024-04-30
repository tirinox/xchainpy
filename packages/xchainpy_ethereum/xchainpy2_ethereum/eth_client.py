import logging
import os
from datetime import datetime
from typing import Optional, List, Union

from eth_account import Account
from hexbytes import HexBytes
from web3 import Web3, middleware
from web3.contract import Contract
from web3.exceptions import TransactionNotFound
from web3.providers import BaseProvider
from web3.types import TxParams

from xchainpy2_client import XChainClient, RootDerivationPaths, FeeBounds, Fees, XcTx, TxPage, FeeRate, TxType, \
    TokenTransfer, FeeOption
from xchainpy2_utils import Chain, NetworkType, CryptoAmount, AssetETH, Asset, Amount
from .const import ETH_ROOT_DERIVATION_PATHS, ETH_DECIMALS, DEFAULT_ETH_EXPLORER_PROVIDERS, \
    FREE_ETH_PROVIDERS, GAS_LIMITS, ETH_CHAIN_ID
from .extra.base import EVMDataProvider
from .extra.etherscan import EtherscanDataProvider
from .gas import GasOptions, GasEstimator
from .utils import is_valid_eth_address, get_erc20_abi, select_random_free_provider

logger = logging.getLogger(__name__)


class EthereumClient(XChainClient):
    def __init__(self,
                 network=NetworkType.MAINNET,
                 phrase: Optional[str] = None,
                 private_key: Union[str, bytes, callable, None] = None,
                 fee_bound: Optional[FeeBounds] = None,
                 root_derivation_paths: Optional[RootDerivationPaths] = None,
                 explorer_providers=DEFAULT_ETH_EXPLORER_PROVIDERS.copy(),
                 wallet_index=0,
                 provider: Optional[BaseProvider] = None,
                 extra_data_provider: Optional[EVMDataProvider] = None,
                 **kwargs
                 ):
        """
        Initialize Ethereum
        :param network: Network type. Default is `NetworkType.MAINNET`
        :param phrase: Mnemonic phrase
        :param private_key: Private key (if you want to use a private key instead of a mnemonic phrase)
        :param fee_bound: Fee bound structure. See: FeeBounds
        :param root_derivation_paths: Dictionary of derivation paths for each network type. See: ROOT_DERIVATION_PATHS
        :param explorer_providers: Dictionary of explorer providers for each network type.
        :param wallet_index: int (default 0)
        :param provider: EVM Web3 RPC provider. Default is `None` (will use a random free provider)
        :param extra_data_provider: EVMDataProvider object for fetching extra data from the blockchain
        """
        root_derivation_paths = root_derivation_paths.copy() \
            if root_derivation_paths else ETH_ROOT_DERIVATION_PATHS.copy()

        super().__init__(Chain.Ethereum, network, phrase, private_key, fee_bound, root_derivation_paths, wallet_index)

        self.explorers = explorer_providers
        self._gas_asset = AssetETH
        self._decimal = ETH_DECIMALS

        self.tx_responses = {}
        self.gas_limits = GAS_LIMITS
        self._chain_ids = ETH_CHAIN_ID

        self._remake_provider(provider)
        self._ex_provider = extra_data_provider or EtherscanDataProvider(
            self.chain, self.network, os.environ.get('ETHERSCAN_API_KEY', '')
        )
        self.fee_estimation_percentiles = (20, 50, 80)
        self.fee_estimation_block_history = 20

    @property
    def get_chain_id(self):
        return self._chain_ids[self.network]

    @property
    def provider(self):
        return self.web3.provider

    @provider.setter
    def provider(self, provider: BaseProvider):
        self._remake_provider(provider)

    def _remake_provider(self, provider: BaseProvider):
        if not provider:
            provider = self._get_default_provider()
        # todo: support multiple providers and round robin algorithm
        self.web3 = Web3(provider)

    def _get_default_provider(self):
        return select_random_free_provider(self.network, FREE_ETH_PROVIDERS)

    def validate_address(self, address: str) -> bool:
        """
        Validates an Ethereum address.
        :param address: Address string
        :return: True if valid, False otherwise.
        """
        return is_valid_eth_address(address)

    def get_address(self) -> str:
        """
        Get the address for the given wallet index.
        :return: string address
        """
        account = self.get_account()
        return account.address

    async def get_balance(self, address: str = '', with_erc20=False) -> List[CryptoAmount]:
        """
        Get the balance of a given address.
        :param address: By default, it will return the balance of the current wallet. (optional)
        :param with_erc20: If True, it will return the balance of all ERC20 tokens as well. (optional)
        :return:
        """
        address = address or self.get_address()
        eth_balance = await self.call_service(self.web3.eth.get_balance, address)
        balances = [
            self.gas_amount(int(eth_balance))
        ]

        if with_erc20:
            erc20_balances = await self._ex_provider.get_erc20_token_balances(address)
            balances.extend(erc20_balances)

        return balances

    def get_erc20_as_contract(self, contract_address: str):
        """
        Get the ERC20 contract object for a given contract address.
        :param contract_address: Contract address
        :return: Contract object
        """
        contract_address = self.validated_checksum_address(contract_address)
        # noinspection PyTypeChecker
        return self.web3.eth.contract(address=contract_address, abi=get_erc20_abi())

    async def get_erc20_token_balance(self, contract_address: str, address: str = '') -> CryptoAmount:
        """
        Get the balance of a given address.
        """
        address = address or self.get_address()
        contract = self.get_erc20_as_contract(contract_address)
        balance = await self.call_service(contract.functions.balanceOf(address).call)

        token_info = await self.get_erc20_token_info(contract)
        return CryptoAmount(Amount(balance, token_info.amount.decimals), token_info.asset)

    async def get_erc20_token_info(self, contract) -> CryptoAmount:
        """
        Returns zero balance and token symbol for a given contract address.
        The balance is zero because we are only interested in the token symbol and decimals.
        :param contract: Contract object
        """
        if not isinstance(contract, Contract):
            contract = self.get_erc20_as_contract(contract)

        decimals = await self.call_service(contract.functions.decimals().call)
        token_symbol = await self.call_service(contract.functions.symbol().call)
        return CryptoAmount(Amount.zero(decimals), Asset(self.chain.value, token_symbol, contract.address))

    async def get_erc20_allowance(self, contract_address: Union[Asset, str],
                                  spender: str, address: str = '') -> CryptoAmount:
        """
        Get the allowance of a given address.
        :param contract_address: ERC20 Contract address. Can be an Asset object or a string.
        :param spender: Spender address
        :param address: By default, it will return the allowance of the current wallet. (optional)
        :return: CryptoAmount
        """
        if not address:
            address = self.get_address()

        if isinstance(contract_address, Asset):
            contract_address = contract_address.contract
        contract_address = self.validated_checksum_address(contract_address)
        contract = self.get_erc20_as_contract(contract_address)

        spender = self.validated_checksum_address(spender)

        token_info = await self.get_erc20_token_info(contract)
        allowance = await self.call_service(contract.functions.allowance(address, spender).call)

        return CryptoAmount(Amount(allowance, token_info.amount.decimals), token_info.asset)

    def get_public_key(self):
        """
        Get the public key for the current wallet.
        """
        return self.get_account().public_key

    def get_account(self) -> Account:
        """
        Get the account object (web3) for the current wallet.
        """
        return Account.from_key(self.get_private_key())

    async def get_transactions(self, address: str, offset: int = 0, limit: int = 0,
                               start_time: Optional[datetime] = None, end_time: Optional[datetime] = None,
                               asset: Optional[Asset] = None) -> TxPage:

        txs = await self._ex_provider.get_address_transactions(address)
        return TxPage(len(txs), txs)

    async def get_transaction_data(self, tx_id: str, with_timestamp=False) -> Optional[XcTx]:
        try:
            receipt = await self.call_service(self.web3.eth.get_transaction_receipt, tx_id)
            tx_data = await self.call_service(self.web3.eth.get_transaction, tx_id)
        except TransactionNotFound:
            return None

        timestamp = 0
        if with_timestamp and receipt:
            timestamp = await self.get_block_timestamp(receipt['blockNumber'])

        return self._convert_tx_data(receipt, tx_data, timestamp) if receipt else None

    def _convert_tx_data(self, receipt, tx_data, timestamp) -> XcTx:
        # todo: decode input data to token transfers
        value = tx_data['value']
        destination = tx_data['to']
        tx_hash = tx_data['hash'].hex()
        transfers = [
            TokenTransfer(
                asset=AssetETH,
                from_address=tx_data['from'],
                to_address=destination,
                amount=self.gas_amount(int(value)).amount,
                tx_hash=tx_hash,
            )
        ]
        return XcTx(
            asset=AssetETH,
            transfers=transfers,
            height=tx_data['blockNumber'],
            is_success=receipt['status'] == 1,
            original=tx_data,
            hash=tx_hash,
            date=timestamp,
            memo='',
            type=TxType.TRANSFER,
        )

    async def get_fees(self) -> Fees:
        """
        Get EVM gas rates for the current network.
        Fees are estimated based on the last 20 blocks.
        All FeeRate are in Gwei!
        """
        estimator = GasEstimator(self.web3, self.fee_estimation_percentiles, self.fee_estimation_block_history)
        return await estimator.estimate()

    async def get_last_fee(self) -> FeeRate:
        """
        Get the last Ethereum fee
        FeeRate is in Gwei
        """
        # noinspection PyProtectedMember
        fee = await self.call_service(self.web3.eth._gas_price)
        return Web3.from_wei(fee, 'gwei')

    async def transfer(self, what: CryptoAmount, recipient: str, memo: Optional[str] = None,
                       gas: Optional[GasOptions] = None, **kwargs) -> str:
        """
        Transfer Ethereum or ERC20 token. Do not use it for swap or something like this.
        Use AMM's `deposit` method instead.
        :param what: Amount to transfer
        :param recipient: Recipient address or contract address to call
        :param memo: Memo (optional, not supported for ERC20 token transfer)
        :param gas: Gas options. Default is `GasOptions.automatic(FeeOption.FAST)`

        :return: Transaction hash
        """
        if not gas:
            gas = GasOptions.automatic(FeeOption.FAST)

        if what.asset.upper() == self.gas_asset.upper():
            # transfer ETH
            return await self._transfer_eth(what, recipient, gas, memo)
        else:
            # transfer ERC20 token
            return await self._transfer_erc20_token(what, recipient, gas, memo)

    @staticmethod
    def _fill_gas_params(params: dict, gas: GasOptions):
        # Gas limit for the transaction
        params['gas'] = gas.gas_limit
        if gas.max_fee_per_gas and gas.max_priority_fee_per_gas:
            # Maximum amount you’re willing to pay
            params['maxFeePerGas'] = gas.max_fee_per_gas
            # Priority fee to include the transaction in the block (if the block is full)
            params['maxPriorityFeePerGas'] = gas.max_priority_fee_per_gas
        elif gas.gas_price:
            params['gasPrice'] = gas.gas_price
        return params

    def _prepare_tx_params(self, to: str, value: int, nonce: int, gas: GasOptions, data: Optional[str] = None):
        params = {
            'value': value,
            'nonce': nonce,
            'from': self.get_address(),
            'chainId': self.get_chain_id,
        }
        if data:
            params['data'] = data.encode('utf-8')
        if to:
            params['to'] = to

        params = self._fill_gas_params(params, gas)
        return params

    def _get_gas_limit(self):
        return self.gas_limits[self.network]

    # noinspection PyTypeChecker
    async def _deduct_gas(self, fee_option: FeeOption, gas_limit=23000) -> GasOptions:
        """
        Deduct gas amount from hi-level fee options
        """
        fees = await self.get_fees()

        # Select the fee option
        max_fee = fees.fees[fee_option]
        if isinstance(max_fee, Amount):
            max_fee = float(max_fee)

        # noinspection PyProtectedMember
        max_priority_fee = fees.fees[FeeOption._ETH_PRIORITY_FEE]
        if isinstance(max_priority_fee, Amount):
            max_priority_fee = float(max_priority_fee)

        return GasOptions.eip1559_in_gwei(max_fee, max_priority_fee, gas_limit)

    async def _transfer_eth(self, what: CryptoAmount, recipient: str, gas: GasOptions,
                            memo: Optional[str] = None) -> str:
        nonce = await self.get_nonce()

        gas = gas.updates_gas_limit(self._get_gas_limit().transfer_gas_asset_gas_limit)
        if gas.is_automatic:
            gas = await self._deduct_gas(gas.fee_option, gas.gas_limit)

        tx_params = self._prepare_tx_params(recipient, what.amount.internal_amount, nonce, gas, memo)
        tx = TxParams(**tx_params)
        acc = self.get_account()
        signed_tx = acc.sign_transaction(tx)
        tx_hash = await self.broadcast_tx(signed_tx.rawTransaction.hex())
        return tx_hash

    async def _transfer_erc20_token(self, what: CryptoAmount, recipient: str, gas: GasOptions,
                                    memo: Optional[str] = None) -> str:
        if not what.asset.contract:
            raise ValueError("Contract address is required for ERC20 token transfer")

        if memo:
            raise ValueError("Memo is not supported for ERC20 token transfer")

        gas = gas.updates_gas_limit(self._get_gas_limit().transfer_token_gas_limit)
        if gas.is_automatic:
            gas = await self._deduct_gas(gas.fee_option, gas.gas_limit)

        contract_address = self.validated_checksum_address(what.asset.contract)
        contract = self.get_erc20_as_contract(contract_address)

        call = contract.functions.transfer(recipient, what.amount.internal_amount)
        gas_limit = self._get_gas_limit().transfer_token_gas_limit
        return await self.make_contract_call(call, 0, gas, gas_limit=gas_limit)

    async def make_contract_call(self, method_pointer, value, gas: GasOptions, gas_limit=-1, nonce=-1) -> str:
        """
        Make a contract call
        :param method_pointer: Contract method pointer
        :param value: Value to send
        :param gas: Gas options
        :param gas_limit: Gas limit
        :param nonce: Nonce (optional) if not provided, it will fetch the nonce from the blockchain
        :return: Transaction hash
        """
        gas_limit_transfer = self._get_gas_limit().transfer_token_gas_limit
        gas = gas.updates_gas_limit(gas_limit if gas_limit > 0 else gas_limit_transfer)
        if gas.is_automatic:
            gas = await self._deduct_gas(gas.fee_option, gas.gas_limit)

        if nonce < 0:
            nonce = await self.get_nonce()  # todo: bsc nonce is mistakenly high

        tx_params = self._prepare_tx_params('', value, nonce, gas)
        tx = method_pointer.build_transaction(tx_params)
        signed_tx = self.get_account().sign_transaction(tx)
        tx_hash = await self.broadcast_tx(signed_tx.rawTransaction.hex())
        return tx_hash

    async def get_block_timestamp(self, block_number: int) -> int:
        block = await self.call_service(self.web3.eth.get_block, block_number)
        if not block:
            raise LookupError(f"Block {block_number} not found")
        timestamp = block['timestamp']
        return timestamp

    async def wait_for_transaction(self, tx_id: str, timeout: int = 120, with_timestamp=False) -> Optional[XcTx]:
        """
        Wait for a transaction to be mined.
        If the transaction is not mined within the timeout, it will raise a TimeExhausted exception.
        :param tx_id: Transaction ID
        :param timeout: Timeout in seconds. Default is 120 seconds
        :param with_timestamp: If True, it will return the timestamp of the block
        :return: Transaction object XcTx
        """
        if not tx_id:
            raise ValueError("Transaction ID is required")

        receipt = await self.call_service(self.web3.eth.wait_for_transaction_receipt, tx_id, timeout)

        timestamp = 0
        if with_timestamp and receipt:
            timestamp = await self.get_block_timestamp(receipt['blockNumber'])

        tx_data = await self.call_service(self.web3.eth.get_transaction, tx_id)

        return self._convert_tx_data(receipt, tx_data, timestamp)

    async def approve_erc20_token(self, spender: str, amount: CryptoAmount,
                                  gas: GasOptions) -> str:
        """
        Approve ERC20 token for a spender
        :param spender: Spender address
        :param amount: Amount to approve
        :param gas: Gas options. Default is `GasOptions.automatic(FeeOption.FAST)`
        :return: Transaction hash
        """
        spender = self.validated_checksum_address(spender)
        contract_address = self.validated_checksum_address(amount.asset.contract)
        contract = self.get_erc20_as_contract(contract_address)
        raw_amount = amount.amount.internal_amount

        call = contract.functions.approve(spender, raw_amount)

        gas_limit = self._get_gas_limit().approve_gas_limit
        return await self.make_contract_call(call, 0, gas, gas_limit=gas_limit)

    async def revoke_erc20_token_allowance(self, spender: str, token: Union[str, Asset], gas: GasOptions) -> str:
        """
        Revoke ERC20 token allowance for a spender
        :param spender: Spender address
        :param token: Token symbol or Asset object
        :param gas: Gas options. Default is `GasOptions.automatic(FeeOption.FAST)`
        """
        if isinstance(token, str):
            asset = self.erc20_asset_from_contract(token, "dummy")
        else:
            asset = token
        return await self.approve_erc20_token(spender, CryptoAmount.zero(asset), gas)

    def erc20_asset_from_contract(self, contract: Union[Contract, str], symbol: str):
        if isinstance(contract, Contract):
            contract = contract.address
        return Asset(self.chain.value, symbol.upper(), contract)

    async def broadcast_tx(self, tx_hex: str) -> str:
        return await self.call_service(self.web3.eth.send_raw_transaction, tx_hex)

    async def get_nonce(self, address: str = '') -> int:
        if not address:
            address = self.get_address()
        return await self.call_service(self.web3.eth.get_transaction_count, address, 'pending')

    def get_explorer_tx_url(self, tx_id: str) -> str:
        if isinstance(tx_id, HexBytes):
            tx_id = tx_id.hex()
        if not tx_id.startswith('0x'):
            tx_id = '0x' + tx_id
        return super().get_explorer_tx_url(tx_id)

    get_explorer_tx_url.__doc__ = XChainClient.get_explorer_tx_url.__doc__

    def validated_checksum_address(self, address: str) -> str:
        if not address:
            raise ValueError("Address is required")
        if address.isupper():  # if it is in uppercase, that means it probably came from THORChain or other similar AMM
            address = self.web3.to_checksum_address(address)
        if not self.validate_address(address):
            raise ValueError(f'Invalid address: {address}')
        return address

    def enable_web3_caching(self):
        w3 = self.web3
        w3.middleware_onion.add(middleware.time_based_cache_middleware)
        w3.middleware_onion.add(middleware.latest_block_based_cache_middleware)
        w3.middleware_onion.add(middleware.simple_cache_middleware)

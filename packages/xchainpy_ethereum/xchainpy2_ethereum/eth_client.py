import logging
from datetime import datetime
from typing import Optional, List, Union

from eth_account import Account
from hexbytes import HexBytes
from web3 import Web3
from web3.exceptions import TransactionNotFound
from web3.providers import BaseProvider
from web3.types import TxParams

from xchainpy2_client import XChainClient, RootDerivationPaths, FeeBounds, Fees, XcTx, TxPage, FeeRate, TxType, \
    TokenTransfer, FeeOption
from xchainpy2_ethereum.const import ETH_ROOT_DERIVATION_PATHS, ETH_DECIMALS, DEFAULT_ETH_EXPLORER_PROVIDERS, \
    FREE_ETH_PROVIDERS, GAS_LIMITS, ETH_CHAIN_ID
from xchainpy2_ethereum.gas import GasOptions
from xchainpy2_ethereum.utils import is_valid_eth_address, estimate_fees, get_erc20_abi, select_random_free_provider
from xchainpy2_utils import Chain, NetworkType, CryptoAmount, AssetETH, Asset, Amount

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
                 provider: Optional[BaseProvider] = None
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
        :param provider: EVM RPC provider
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
        Validates a Ethereum address.
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

    async def get_balance(self, address: str = '') -> List[CryptoAmount]:
        """
        Get the balance of a given address.
        :param address: By default, it will return the balance of the current wallet. (optional)
        :return:
        """
        address = address or self.get_address()
        eth_balance = await self._call_service(self.web3.eth.get_balance, address)

        return [
            self.gas_amount(int(eth_balance))
        ]

    def get_erc20_as_contract(self, contract_address: str):
        """
        Get the ERC20 contract object for a given contract address.
        :param contract_address: Contract address
        :return: Contract object
        """
        return self.web3.eth.contract(address=contract_address, abi=get_erc20_abi())

    async def get_erc20_token_balance(self, contract_address: str, address: str = '') -> CryptoAmount:
        """
        Get the balance of a given address.
        """
        address = address or self.get_address()
        contract = self.get_erc20_as_contract(contract_address)
        balance = await self._call_service(contract.functions.balanceOf(address).call)

        token_info = await self.get_erc20_token_info(contract)
        return CryptoAmount(Amount(balance, token_info.amount.decimals), token_info.asset)

    async def get_erc20_token_info(self, contract) -> CryptoAmount:
        """
        Returns zero balance and token symbol for a given contract address.
        The balance is zero because we are only interested in the token symbol and decimals.
        :param contract: Contract object
        """
        decimals = await self._call_service(contract.functions.decimals().call)
        token_symbol = await self._call_service(contract.functions.symbol().call)
        return CryptoAmount(Amount.zero(decimals), Asset(self.chain.value, token_symbol, contract.address))

    async def get_approved_erc20_token(self, contract_address: str, spender: str, address: str = '') -> CryptoAmount:
        """
        Get the allowance of a given address.
        :param contract_address: ERC20 Contract address
        :param spender: Spender address
        :param address: By default, it will return the allowance of the current wallet. (optional)
        :return: CryptoAmount
        """
        if not address:
            address = self.get_address()

        contract = self.get_erc20_as_contract(contract_address)
        token_info = await self.get_erc20_token_info(contract)
        allowance = await self._call_service(contract.functions.allowance(address, spender).call)

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
        raise NotImplementedError("Ethereum transaction fetching is not implemented yet")

    async def get_transaction_data(self, tx_id: str, with_timestamp=False) -> Optional[XcTx]:
        try:
            receipt = await self._call_service(self.web3.eth.get_transaction_receipt, tx_id)
            tx_data = await self._call_service(self.web3.eth.get_transaction, tx_id)
        except TransactionNotFound:
            return None

        timestamp = 0
        if with_timestamp and receipt:
            block = await self._call_service(self.web3.eth.get_block, receipt['blockNumber'])
            timestamp = block['timestamp']

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
        Get Ethereum fees
        Fees are estimated based on the last 20 blocks.
        FeeRate is in Gwei
        """
        return await self._call_service(estimate_fees, self.web3)

    async def get_last_fee(self) -> FeeRate:
        """
        Get the last Ethereum fee
        FeeRate is in Gwei
        """
        fee = await self._call_service(self.web3.eth._gas_price)
        return Web3.from_wei(fee, 'gwei')

    async def transfer(self, what: CryptoAmount, recipient: str, memo: Optional[str] = None,
                       gas: Optional[GasOptions] = None, **kwargs) -> str:
        """
        Transfer Ethereum or ERC20 token. Do not use it for swap. Use AMM's `deposit` method instead.

        :param what: Amount to transfer
        :param recipient: Recipient address or contract address to call
        :param memo: Memo (optional)
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

    def _prepare_tx_params(self, to: str, value: int, nonce: int, gas: GasOptions, data: Optional[str] = None):
        params = {
            'to': to,
            'value': value,
            'nonce': nonce,
            'from': self.get_address(),
            'gas': gas.gas_limit,
            'chainId': self.get_chain_id,
        }
        if data:
            params['data'] = data.encode('utf-8')

        if gas.max_fee_per_gas and gas.max_priority_fee_per_gas:
            params['maxFeePerGas'] = gas.max_fee_per_gas
            params['maxPriorityFeePerGas'] = gas.max_priority_fee_per_gas
        elif gas.gas_price:
            params['gasPrice'] = gas.gas_price

        return params

    def _get_gas_limit(self):
        return self.gas_limits[self.network]

    async def _transfer_eth(self, what: CryptoAmount, recipient: str, gas: GasOptions,
                            memo: Optional[str] = None) -> str:
        nonce = await self.get_nonce()
        gas = gas.updates_gas_limit(self._get_gas_limit().transfer_gas_asset_gas_limit)
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

        gas = gas.updates_gas_limit(self._get_gas_limit().transfer_token_gas_limit)

        raise NotImplementedError("ERC20 token transfer is not implemented yet")

    async def wait_for_transaction(self, tx_id: str, timeout: int = 120) -> XcTx:
        results = await self._call_service(self.web3.eth.wait_for_transaction_receipt, tx_id, timeout)
        return self._convert_tx_data(results, tx_id, results['timestamp'])

    async def approve_erc20_token(self, spender: str, amount: CryptoAmount,
                                  fee_option: Optional[FeeOption] = FeeOption.FAST,
                                  fee_rate: FeeRate = 0) -> str:
        """
        Approve ERC20 token for a spender
        :param spender: Spender address
        :param amount: Amount to approve
        :param fee_option: Fee option. Default is `FeeOption.FAST` (only used if fee_rate is not set)
        :param fee_rate: Fee rate in Gwei. If fee rate is set, fee_option will be ignored.
        :return: Transaction hash
        """

        # todo: use GasOptions

        if not fee_rate:
            fees = await self.get_fees()
            fee_rate = fees.fees[fee_option]

        contract_address = self.web3.to_checksum_address(amount.asset.contract)
        contract = self.get_erc20_as_contract(contract_address)
        raw_amount = amount.amount.internal_amount

        # estimate gas needed
        # gas = await self._call_service(contract.functions.approve(spender, raw_amount).estimateGas)
        gas = self._get_gas_limit().approve_gas_limit

        tx = contract.functions.approve(spender, raw_amount).buildTransaction({
            'nonce': await self.get_nonce(),
            'gas': gas,
            'gasPrice': self.web3.to_wei(fee_rate, 'gwei'),
        })
        # sign
        signed_tx = self.get_account().sign_transaction(tx)
        tx_hash = await self.broadcast_tx(signed_tx.rawTransaction.hex())
        return tx_hash

    async def broadcast_tx(self, tx_hex: str) -> str:
        return await self._call_service(self.web3.eth.send_raw_transaction, tx_hex)

    async def get_nonce(self, address: str = '') -> int:
        if not address:
            address = self.get_address()
        return await self._call_service(self.web3.eth.get_transaction_count, address)

    def get_explorer_tx_url(self, tx_id: str) -> str:
        if isinstance(tx_id, HexBytes):
            tx_id = tx_id.hex()
        if not tx_id.startswith('0x'):
            tx_id = '0x' + tx_id
        return super().get_explorer_tx_url(tx_id)

    get_explorer_tx_url.__doc__ = XChainClient.get_explorer_tx_url.__doc__

import datetime

from web3.contract import Contract

from xchainpy2_ethereum import EthereumClient, GasOptions, EVM_NULL_ADDRESS
from xchainpy2_ethereum.utils import get_router_abi
from xchainpy2_thorchain_amm import AMMException, DEFAULT_EXPIRY
from xchainpy2_thorchain_query import THORChainCache
from xchainpy2_utils import CryptoAmount, Chain

DEFAULT_EVM_DEPOSIT_GAS_LIMIT = 160_000


class EVMHelper:
    """
    EVMHelper is a helper class for EVM clients (e.g. EthereumClient, BinanceSmartChainClient) that
    provides methods to interact with THORChain router contract and manage ERC20 token allowance.
    """

    # todo: make BaseEVMClient
    def __init__(self, evm_client: EthereumClient, tc_cache: THORChainCache):
        self.evm_client = evm_client
        self._tc_cache = tc_cache
        self._router_abi = get_router_abi()
        self.deposit_gas_limit = DEFAULT_EVM_DEPOSIT_GAS_LIMIT

    async def deposit(self, amount: CryptoAmount, memo: str, gas: GasOptions, expiration_sec: int = -1,
                      check_allowance: bool = True) -> str:
        """
        Send deposit to THORChain router
        :param amount: amount and asset you want to deposit
        :param memo: memo contains the request details (e.g. swap details)
        :param gas: gas options
        :param expiration_sec: expiration time in seconds
        :param check_allowance: check if the router is approved to spend the asset
        :return: str (submitted transaction hash)
        """
        router = await self.get_router()
        if not router:
            raise AMMException('Failed to get router contract')

        chain = Chain(amount.asset.chain)
        details = await self._tc_cache.get_details_for_chain(chain)
        if not details:
            raise AMMException(f'Failed to get inbound details for chain {chain.value}')

        vault = details.address
        if not vault:
            raise AMMException(f'Failed to get vault address for chain {chain.value}')
        vault = self.evm_client.validated_checksum_address(vault.upper())

        if check_allowance and not await self.is_tc_router_approved_to_spend(amount):
            raise AMMException(f'Router has not been approved yet for ERC20 token or allowance is insufficient:'
                               f' {amount} more is required')

        if amount.asset.contract:
            asset = amount.asset.contract
            asset = self._to_checksum_address(asset)
        else:
            asset = EVM_NULL_ADDRESS

        memo = memo or ''

        if expiration_sec < 0:
            expiration_sec = DEFAULT_EXPIRY

        """
         "inputs": [
          { "internalType": "address payable", "name": "vault", "type": "address" },
          { "internalType": "address", "name": "asset", "type": "address" },
          { "internalType": "uint256", "name": "amount", "type": "uint256" },
          { "internalType": "string", "name": "memo", "type": "string" },
          { "internalType": "uint256", "name": "expiration", "type": "uint256" }
        ],
        """
        expiration_ts = int(datetime.datetime.now().timestamp()) + expiration_sec
        raw_amount = int(amount.amount)

        if self.evm_client.gas_asset == amount.asset:
            value = raw_amount
        else:
            value = 0

        return await self.deposit_unsafe(asset, expiration_ts, gas, memo, raw_amount, router, value, vault)

    async def deposit_unsafe(self, asset_contract, expiration_ts, gas: GasOptions, memo, raw_amount, router, value,
                             vault, nonce=-1):
        """
        Deposit amount to THORChain router without any checks
        :param asset_contract: Asset contract address
        :param expiration_ts: Expiration timestamp, the transaction will be rejected if it is mined after this time
        :param gas: Gas options
        :param memo: Transaction memo that contains the request details (e.g. swap details)
        :param raw_amount: Amount of ERC20 token to deposit
        :param router: THORChain router contract address
        :param value: Eth Value to send with the transaction
        :param vault: THORChain vault address
        :param nonce: Transaction nonce, -1 means automatic
        :return:
        """
        deposit_method = router.functions.depositWithExpiry(vault, asset_contract, raw_amount, memo, expiration_ts)
        gas_limit = self.deposit_gas_limit
        tx_hash = await self.evm_client.make_contract_call(deposit_method, value, gas, gas_limit=gas_limit,
                                                           nonce=nonce)
        return tx_hash

    async def is_tc_router_approved_to_spend(self, amount: CryptoAmount) -> bool:
        """
        Check if THORChain router is approved to spend the asset
        :param amount: amount and asset you want to deposit
        :return: bool
        """
        if int(amount.amount) == 0:
            return True

        if int(amount.amount) < 0:
            raise ValueError('Amount should be greater than 0')

        if amount.asset.chain != self.chain.value:
            raise ValueError('Invalid chain')

        if amount.asset == self.evm_client.gas_asset:
            # No need to approve the gas asset
            return True

        router = await self.get_router_address()
        router = self._to_checksum_address(router)  # we trust the router address from the TC API

        spend_from = self.evm_client.get_address()
        if not spend_from:
            raise ValueError('Failed to get the address of the client')

        approved = await self.evm_client.get_erc20_allowance(amount.asset, router, spend_from)
        return approved.amount >= amount.amount

    async def approve_tc_router(self, amount: CryptoAmount, gas: GasOptions) -> str:
        """
        Approve THORChain router to spend the asset
        :param amount: amount and asset you want to deposit
        :param gas: gas options
        :return: str (submitted transaction hash)
        """
        router = await self.get_router_address()
        return await self.evm_client.approve_erc20_token(router, amount, gas)

    @property
    def chain(self) -> Chain:
        """
        Get the chain of the EVM client

        :return: Chain
        """
        return self.evm_client.chain

    async def get_router_address(self) -> str:
        """
        Get THORChain router contract address from TC API (inbound_details request)

        :return: str (router contract address)
        """
        inbound = await self._tc_cache.get_inbound_details()
        if not inbound:
            raise ValueError('Failed to get inbound details')

        chain_info = inbound.get(self.chain.value)
        if not chain_info:
            raise ValueError(f'Failed to get inbound details for chain {self.chain.value}')

        router = chain_info.router
        if not router:
            raise ValueError(f'Failed to get router address for chain {self.chain.value}')

        router = self._to_checksum_address(router)  # we trust the router address from the TC API

        return router

    async def get_router(self, router_address='') -> Contract:
        """
        Get THORChain router contract instance

        :param router_address: Router contract address, if not provided it will be fetched from the TC API
        :return: Contract of web3 library
        """
        if not router_address:
            router_address = await self.get_router_address()

        if router_address and router_address.startswith('0x'):
            router_address = router_address.upper()  # so it will easily pass the following line
        router_address = self.evm_client.validated_checksum_address(router_address)
        # noinspection PyTypeChecker
        return self.evm_client.web3.eth.contract(address=router_address, abi=self._router_abi)

    def _to_checksum_address(self, address: str) -> str:
        return self.evm_client.web3.to_checksum_address(address)

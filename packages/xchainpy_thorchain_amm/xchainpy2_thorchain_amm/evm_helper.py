import datetime

from web3.contract import Contract

from xchainpy2_ethereum import EthereumClient, GasOptions
from xchainpy2_ethereum.utils import get_router_abi
from xchainpy2_thorchain_amm import AMMException, DEFAULT_EXPIRY
from xchainpy2_thorchain_query import THORChainCache
from xchainpy2_utils import CryptoAmount, Chain


class EVMHelper:
    # todo: make BaseEVMClient
    def __init__(self, evm_client: EthereumClient, tc_cache: THORChainCache):
        self.evm_client = evm_client
        self._tc_cache = tc_cache
        self._router_abi = get_router_abi()

    async def deposit(self, amount: CryptoAmount, memo: str, gas: GasOptions, expiration_timestamp: int = -1) -> str:
        """
        Send deposit to THORChain router
        :param amount: amount and asset you want to deposit
        :param memo: memo contains the request details (e.g. swap details)
        :param gas: gas options
        :param expiration_timestamp: expiration timestamp (default if negative: 15 minutes from now)
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

        asset = amount.asset.contract or ''
        memo = memo or ''

        if expiration_timestamp < 0:
            expiration_timestamp = (DEFAULT_EXPIRY + int(datetime.datetime.utcnow().timestamp()))

        """
         "inputs": [
          { "internalType": "address payable", "name": "vault", "type": "address" },
          { "internalType": "address", "name": "asset", "type": "address" },
          { "internalType": "uint256", "name": "amount", "type": "uint256" },
          { "internalType": "string", "name": "memo", "type": "string" },
          { "internalType": "uint256", "name": "expiration", "type": "uint256" }
        ],
        """
        deposit_method = router.functions.depositWithExpiry(vault, asset, amount, memo, expiration_timestamp)

        if self.evm_client.gas_asset == amount.asset:
            value = int(amount.amount)
        else:
            value = 0

        tx_hash = await self.evm_client.make_contract_call(deposit_method, value, gas)
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

        if amount.asset.chain != self.chain:
            raise ValueError('Invalid chain')

        if amount.asset == self.evm_client.gas_asset:
            return True

        router = await self.get_router_address()
        approved = await self.evm_client.get_erc20_allowance(amount.asset, router, self.evm_client.get_address())
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
    def chain(self):
        return self.evm_client.chain

    async def get_router_address(self) -> str:
        inbound = await self._tc_cache.get_inbound_details()
        if not inbound:
            raise ValueError('Failed to get inbound details')

        chain_info = inbound.get(self.chain.value)
        if not chain_info:
            raise ValueError(f'Failed to get inbound details for chain {self.chain.value}')

        return chain_info.router

    async def get_router(self) -> Contract:
        router_address = await self.get_router_address()
        router_address = self.evm_client.validated_checksum_address(router_address)
        # noinspection PyTypeChecker
        return self.evm_client.web3.eth.contract(address=router_address, abi=self._router_abi)

import asyncio
import json
from typing import NamedTuple, Union

from web3 import Web3
from web3.contract import Contract

from .utils import get_erc20_abi, validated_checksum_address
from xchainpy2_utils import Chain, Asset, CryptoAmount, Amount


class TokenInfo(NamedTuple):
    """
    ERC20 Token information
    """
    address: str
    chain_id: int
    chain: Chain
    name: str
    symbol: str
    decimals: int
    logo_uri: str

    @property
    def as_asset(self):
        """
        Convert TokenInfo to Asset instance
        :return:
        """
        return Asset(self.chain.value, self.symbol, self.address)

    def amount_of(self, amount):
        """
        Returns CryptoAmount instance of the given amount of this token
        :param amount:
        :return: CryptoAmount
        """
        return CryptoAmount(Amount.automatic(amount).changed_decimals(self.decimals), self.as_asset)

    @classmethod
    def from_json(cls, data, chain: Chain):
        """
        Create TokenInfo instance from JSON data from 1INCH token lists
        :param data: JSON dict
        :param chain: Chain
        :return: TokenInfo
        """
        return cls(
            address=data['address'],
            chain_id=data['chainId'],
            chain=chain,
            name=data['name'],
            symbol=data['symbol'],
            decimals=data['decimals'],
            logo_uri=data.get('logoURI')
        )


class TokenInfoList:
    """
    TokenInfo loader and cache. Popular tokens are loaded from a JSON file.
    If a token is not found in the cache, it will be loaded from the WEB3 provider.
    """
    def __init__(self, chain: Chain, web3: Web3, filename: str):
        self.chain = chain
        self.web3 = web3
        self.filename = filename
        self.address_to_info = {}
        self._erc20_abi = get_erc20_abi()

    def load(self):
        self.address_to_info.clear()
        with open(self.filename, 'r') as f:
            data = json.load(f)
            for token in data['tokens']:
                info = TokenInfo.from_json(token, self.chain)
                self.address_to_info[info.address.upper()] = info

    async def get_token_info(self, contract: Union[str, Contract, Asset]) -> TokenInfo:
        """
        Get token info from the cache.
        If not found, it will be loaded from the WEB3 provider and stored in the cache.
        :param contract: ERC20 contract address or Asset object
        :return: TokenInfo
        """
        if isinstance(contract, Contract):
            contract = contract.address
        elif isinstance(contract, Asset):
            contract = contract.contract

        contract = contract.upper()
        token_info = self.address_to_info.get(contract)
        if not token_info:
            token_info = await self.load_erc20_token_info(contract)
            self.address_to_info[contract] = token_info
        return token_info

    async def fill_crypto_amount(self, a: CryptoAmount) -> CryptoAmount:
        """
        This method will replace the asset symbol name and decimals of the amount with the token info
        :param a: CryptoAmount
        :return: CryptoAmount
        """

        if a.asset.chain != self.chain:
            raise ValueError(f"Chain mismatch: {a.asset.chain} != {self.chain}")

        contract_address = a.asset.contract.upper()
        token_info: TokenInfo = self.address_to_info.get(contract_address)
        if not token_info:
            token_info = await self.get_token_info(contract_address)

        return CryptoAmount(
            a.amount.changed_decimals(token_info.decimals), token_info.as_asset
        )

    def get_erc20_as_contract(self, contract_address: str):
        """
        Get the ERC20 contract object for a given contract address.
        :param contract_address: Contract address
        :return: Contract object
        """
        contract_address = validated_checksum_address(self.web3, contract_address)
        # noinspection PyTypeChecker
        return self.web3.eth.contract(address=contract_address, abi=self._erc20_abi)

    async def load_erc20_token_info(self, contract: Union[str, Contract]) -> TokenInfo:
        """
        Returns zero balance and token symbol for a given contract address.
        The balance is zero because we are only interested in the token symbol and decimals.
        :param contract: Contract object
        """
        if not isinstance(contract, Contract):
            contract = self.get_erc20_as_contract(contract)

        decimals = await self.call_service(contract.functions.decimals().call)
        token_symbol = await self.call_service(contract.functions.symbol().call)
        return TokenInfo(
            contract.address,
            self.chain_id,
            self.chain,
            token_symbol,
            token_symbol,
            decimals,
            ''
        )

    async def get_erc20_token_balance(self, contract_address: str, address: str = '') -> CryptoAmount:
        """
        Get the balance of a given address.
        """
        contract = self.get_erc20_as_contract(contract_address)
        balance = await self.call_service(contract.functions.balanceOf(address).call)
        token_info = await self.load_erc20_token_info(contract)
        return CryptoAmount(Amount(balance, token_info.decimals), token_info.as_asset)

    async def get_erc20_allowance(self, contract_address: Union[Asset, str],
                                  spender: str, address: str = '') -> CryptoAmount:
        """
        Get the allowance of a given address.
        :param contract_address: ERC20 Contract address. Can be an Asset object or a string.
        :param spender: Spender address
        :param address: By default, it will return the allowance of the current wallet. (optional)
        :return: CryptoAmount
        """
        if isinstance(contract_address, Asset):
            contract_address = contract_address.contract
        contract_address = validated_checksum_address(self.web3, contract_address)
        contract = self.get_erc20_as_contract(contract_address)

        spender = validated_checksum_address(self.web3, spender)

        token_info = await self.get_token_info(contract)
        allowance = await self.call_service(contract.functions.allowance(address, spender).call)

        return CryptoAmount(Amount(allowance, token_info.decimals), token_info.as_asset)

    @property
    def chain_id(self):
        any_token = next(iter(self.address_to_info.values()))
        if not any_token:
            raise ValueError("No tokens loaded")
        return any_token.chain_id

    @classmethod
    async def call_service(cls, method, *args):
        return await asyncio.get_event_loop().run_in_executor(
            None,
            method,
            *args
        )

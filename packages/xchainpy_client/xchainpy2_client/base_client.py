import abc
import asyncio
from datetime import datetime
from decimal import Decimal
from typing import Optional, List, Union

from xchainpy2_client.explorer import ExplorerProvider
from xchainpy2_client.models import XcTx, Fees, TxPage, \
    FeeBounds, RootDerivationPaths, FeeOption
from xchainpy2_crypto import validate_mnemonic, derive_private_key
from xchainpy2_utils import CryptoAmount, Chain, NetworkType, Asset, Amount


class KeyException(Exception):
    ...


class XChainClient(abc.ABC):
    def __init__(self,
                 chain: Chain,
                 network: Optional[NetworkType] = None,
                 phrase: Optional[str] = None,
                 private_key: Union[str, bytes, callable, None] = None,
                 fee_bound: Optional[FeeBounds] = None,
                 root_derivation_paths: Optional[RootDerivationPaths] = None,
                 wallet_index=0,
                 ):
        """
        Client has to be initialised with network type and phrase.
        It will throw an error if an invalid phrase has been passed.

        :param chain: Chain name (see utils/chain.py)
        :param network: Network type (see utils/network_type.py)
        :param phrase: Mnemonic phrase (12-24 words)
        :param private_key: Private key (if you want to use a private key instead of a mnemonic phrase)
        :param fee_bound: Fee bounds
        :param root_derivation_paths: Root derivation paths for private key for each Network type
        :param wallet_index: int (wallet index, default 0) We can derive any number of addresses from a single seed
        """
        self.wallet_index = wallet_index
        self.chain = chain

        self.fee_bound = fee_bound or FeeBounds.infinite()
        self.root_derivation_paths = root_derivation_paths

        self.network = network
        self.set_network(network)

        self.explorers = {network: ExplorerProvider('', '', '')}

        # NOTE: we don't call this.setPhrase() to void generating an address and paying the perf penalty
        if phrase:
            if not validate_mnemonic(phrase):
                raise KeyException('Invalid phrase')
            self.phrase = phrase
        else:
            self.phrase = None

        self._private_key = private_key

        if private_key and phrase:
            raise KeyException('Phrase and private key cannot be provided at the same time')

        self._gas_asset: Optional[Asset] = None
        self._decimal = 8

        self.last_response_dict = {}

    @property
    def decimal(self):
        return self._decimal

    @abc.abstractmethod
    def validate_address(self, address: str) -> bool:
        pass

    @abc.abstractmethod
    def get_address(self) -> str:
        pass

    @abc.abstractmethod
    def get_public_key(self):
        pass

    def get_private_key(self) -> str:
        """
        Get the private key for the given wallet index.
        :return:
        """
        if self.pk_hex:
            return self.pk_hex
        elif self.phrase:
            return derive_private_key(
                self.phrase,
                self.get_full_derivation_path(self.wallet_index)
            ).hex()
        else:
            raise KeyException('Phrase or private key must be provided to do this action')

    def _throw_if_empty_phrase(self):
        if not self.phrase and not self._private_key:
            raise KeyException('Phrase or private key must be provided to do this action')

    @property
    def pk_hex(self):
        if callable(self._private_key):
            return self._private_key()
        elif isinstance(self._private_key, str):
            return self._private_key
        elif isinstance(self._private_key, bytes):
            return self._private_key.hex()
        else:
            return None

    def gas_amount(self, amount: Union[float, str, int, Decimal, Amount]) -> CryptoAmount:
        """
        Easy way to construct CryptoAmount of gas asset
        Type int means base amount (like satoshi, wei, 1e-8 rune, etc)
        Types float and Decimal means asset amount (like btc, eth, rune, etc)
        :param amount: Union[float, str, int, Decimal] amount of asset (not base!)
        :return: CryptoAmount
        """
        return CryptoAmount(Amount.automatic(amount, self._decimal), self._gas_asset)

    def gas_base_amount(self, amount: int) -> CryptoAmount:
        """
        Easy way to construct CryptoAmount of gas asset from base units
        :param amount: base amount of asset (like satoshi, wei, 1e-8 rune, etc); must be int type
        :return:
        """
        assert isinstance(amount, int)
        return CryptoAmount(Amount.from_base(amount, self._decimal), self._gas_asset)

    def gas_asset_amount(self, amount: Union[float, str, Decimal]) -> CryptoAmount:
        """
        Easy way to construct CryptoAmount of gas asset from asset units
        :param amount: asset amount (like btc, eth, rune, etc); must be float or Decimal type or str
        :return:
        """
        assert isinstance(amount, (float, str, Decimal))
        return CryptoAmount(Amount.from_asset(amount, self._decimal), self._gas_asset)

    @property
    def zero_gas_amount(self) -> CryptoAmount:
        return self.gas_base_amount(0)

    async def max_gas_amount(self, balances: List[CryptoAmount] = None) -> CryptoAmount:
        """
        Calculate maximum amount of Gas asset that you can send to empty your wallet
        :param balances: (Optional) if you already have your balance, otherwise they will be loaded
        :return: CryptoAmount
        """
        if balances is None:
            balances = await self.get_balance()

        gas_balance = next((b for b in balances if b.asset == self._gas_asset), None)
        if not gas_balance:
            return self.zero_gas_amount  # no gas at all

        fees = await self.get_fees()
        fee = fees.fees[FeeOption.FAST]
        max_value = gas_balance.amount.as_asset - fee.as_asset
        if max_value.internal_amount < 0:
            # less than fee
            return self.zero_gas_amount
        else:
            return CryptoAmount(max_value, self._gas_asset)

    def set_network(self, network: NetworkType):
        if not network:
            network = NetworkType.MAINNET
        self.network = network

        # Fire off a warning in the console to indicate that stagenet and real assets are being used.
        if self.network == NetworkType.STAGENET:
            print("WARNING: This is using stagenet! Real assets are being used!")

    def get_network(self):
        return self.network

    def set_phrase(self, phrase: str, wallet_index: int = 0):
        if phrase:
            if not validate_mnemonic(phrase):
                raise KeyException('Invalid phrase')
            self.phrase = phrase
        else:
            self.purge_client()
        self.wallet_index = wallet_index

    def purge_client(self):
        self.phrase = ''
        self._private_key = None

    def get_explorer_url(self) -> str:
        """
        Get the explorer url.
        :return: The explorer url based on the network.
        """
        return self.explorers[self.network].explorer_url

    def get_explorer_address_url(self, address: str) -> str:
        """
        Get the explorer url for the given address.
        :param address: address
        :return: The explorer url for the given address based on the network.
        """
        if not address:
            address = self.get_address()
        return self.explorers[self.network].get_address_url(address)

    def get_explorer_tx_url(self, tx_id: str) -> str:
        """
        Get the explorer url for the given transaction id.
        :param tx_id: The transaction id
        :return: str The explorer url for the given transaction id based on the network.
        """
        if not tx_id:
            raise ValueError('tx_id is required')
        return self.explorers[self.network].get_tx_url(tx_id)

    @abc.abstractmethod
    async def get_balance(self, address: str = '') -> List[CryptoAmount]:
        pass

    async def get_gas_balance(self, address: str = '') -> CryptoAmount:
        """
        Get the balance of the gas asset for the given address
        :param address: address (optional)
        :return: CryptoAmount of the gas asset
        """
        balances = await self.get_balance(address)
        gas_balance = next((b for b in balances if b.asset == self._gas_asset), None)
        if not gas_balance:
            return self.zero_gas_amount
        return gas_balance

    async def has_balance(self, amount: CryptoAmount):
        """
        Check if the wallet has enough balance to send the given amount
        :param amount: amount to send
        :return: True if the wallet has enough balance, False otherwise
        """
        balances = await self.get_balance()
        balance = next((b for b in balances if b.asset == amount.asset), None)
        if not balance:
            return False
        return balance.amount >= amount.amount

    def get_full_derivation_path(self, wallet_index: int) -> str:
        if self.root_derivation_paths:
            # BREAKING CHANGE!
            # return f"{self.root_derivation_paths[self.network]}{wallet_index}'"  # original with apostrophe
            return f"{self.root_derivation_paths[self.network]}{wallet_index}"
        return ''

    @abc.abstractmethod
    async def get_transactions(self, address: str = '',
                               offset: int = 0,
                               limit: int = 0,
                               start_time: Optional[datetime] = None,
                               end_time: Optional[datetime] = None,
                               asset: Optional[Asset] = None) -> TxPage:
        pass

    @abc.abstractmethod
    async def get_transaction_data(self, tx_id: str) -> Optional[XcTx]:
        pass

    @abc.abstractmethod
    async def get_fees(self) -> Fees:
        pass

    @abc.abstractmethod
    async def transfer(self, what: CryptoAmount,
                       recipient: str,
                       memo: Optional[str] = None,
                       fee_rate: Optional[int] = None, **kwargs) -> str:
        pass

    async def wait_for_transaction(self, tx_id: str, timeout=1200, poll_period=5):
        """
        Wait for the transaction to be confirmed/mined. It will poll the transaction status every poll_period seconds.

        :param tx_id: transaction ID
        :param timeout: timeout in seconds
        :param poll_period: poll period in seconds
        """

        while poll_period < timeout:
            tx = await self.get_transaction_data(tx_id)
            if tx and tx.is_success:
                return tx
            await asyncio.sleep(poll_period)
            timeout -= poll_period

        raise TimeoutError(f'Transaction {tx_id} was not confirmed in {timeout} seconds')

    @abc.abstractmethod
    async def broadcast_tx(self, tx_hex: str) -> str:
        """
        Broadcast the transaction to the network.
        :param tx_hex: The transaction content in hex format.
        :return: The transaction identifier (or hash).
        """
        pass

    @property
    def gas_asset(self):
        return self._gas_asset

    def _save_last_response(self, txid, result):
        if txid and result:
            self.last_response_dict[txid] = result

    def get_last_response(self, txid: str):
        return self.last_response_dict.get(txid)

    def clear_last_responses(self):
        self.last_response_dict = {}

    @classmethod
    async def call_service(cls, method, *args):
        return await asyncio.get_event_loop().run_in_executor(
            None,
            method,
            *args
        )


class NoClient(XChainClient, abc.ABC):
    ...

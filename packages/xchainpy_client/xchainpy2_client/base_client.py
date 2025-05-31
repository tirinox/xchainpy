import abc
import asyncio
import warnings
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

        # NOTE: we don't call self.set_phrase() to void generating an address and paying the perf penalty
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
        """
        Get the decimal places for the main (gas?) asset.

        :return: int Decimal places for the main asset, default is 8.
        """
        return self._decimal

    @abc.abstractmethod
    def validate_address(self, address: str) -> bool:
        """
        Validate the address for the given chain.

        :param address: str Address to validate.
        :return: bool True if the address is valid, False otherwise.
        """
        pass

    @abc.abstractmethod
    def get_address(self) -> str:
        """
        Get the address for the wallet.

        :return: str Address of the wallet.
        """
        pass

    @abc.abstractmethod
    def get_public_key(self):
        """
        Get the public key for the given wallet index.
        # todo: make it consistent for all clients, some return hex, some return bytes!

        :return: str Public key as hex string.
        """
        pass

    def get_private_key(self) -> str:
        """
        Get the private key for the current wallet.
        First it will try to use the provided private key, then the phrase, and finally raise an exception if neither is available.

        :return: str Hex representation of the private key.
        """
        if callable(self._private_key):
            pk = self._private_key()
            if not pk or not isinstance(pk, str):
                raise KeyException('_private_key function must return a HEX string')
            return pk
        elif isinstance(self._private_key, str):
            return self._private_key
        elif isinstance(self._private_key, bytes):
            return self._private_key.hex()
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

    def gas_amount(self, amount: Union[float, str, int, Decimal, Amount]) -> CryptoAmount:
        """
        Easy way to construct CryptoAmount of gas asset.
        See :py:class:`CryptoAmount` and :py:class:`Amount` for more details.

        :param amount: Union[float, str, int, Decimal] amount of asset (not base!), e.g. 1.1 ETH, 0.05 BTC
        :return: CryptoAmount
        """
        return CryptoAmount(Amount.automatic(amount, self._decimal), self._gas_asset)

    def gas_base_amount(self, amount: int) -> CryptoAmount:
        """
        Easy way to construct CryptoAmount of gas asset from base units (like satoshi, wei, 1e-8 rune, etc); must be int type

        :param amount: int amount of asset in base units
        :return:
        """
        assert isinstance(amount, int)
        return CryptoAmount(Amount.automatic_base(amount, self._decimal), self._gas_asset)

    @property
    def zero_gas_amount(self) -> CryptoAmount:
        """
        Get zero amount of gas asset.

        :return: CryptoAmount of gas asset with zero amount
        """
        return self.gas_base_amount(0)

    async def max_gas_amount(self, balances: List[CryptoAmount] = None) -> CryptoAmount:
        """
        Calculate maximum amount of Gas asset that you can send to empty your wallet.

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
        # note: must be same decimals
        max_value = gas_balance.amount - fee
        if max_value.internal_amount < 0:
            # less than fee
            return self.zero_gas_amount
        else:
            return CryptoAmount(max_value, self._gas_asset)

    def set_network(self, network: NetworkType):
        if not network:
            network = NetworkType.MAINNET

        if not isinstance(network, NetworkType):
            network = NetworkType(network)

        self.network = network

        # Fire off a warning in the console to indicate that stagenet and real assets are being used.
        if self.network == NetworkType.STAGENET:
            warnings.warn("Your are using The Stagenet! "
                          "This means that real assets are being used! "
                          "Don't swap large amounts because pools are very shallow.", UserWarning)

    def get_network(self) -> NetworkType:
        """
        Get the network type for this client.

        :return: NetworkType
        """
        return self.network

    def set_phrase(self, phrase: str, wallet_index: int = 0):
        """
        Set the seed phrase for the client. It will also set the wallet index.

        :param phrase: Mnemonic phrase (12-24 words)
        :param wallet_index: Wallet index (default is 0)
        """
        if phrase:
            if not validate_mnemonic(phrase):
                raise KeyException('Invalid phrase')
            self.phrase = phrase
        else:
            self.purge_client()
        self.wallet_index = wallet_index

    def purge_client(self):
        """
        Purge the client by clearing the phrase and private key.
        """
        self.phrase = ''
        self._private_key = None

    def get_explorer_url(self) -> str:
        """
        Get the explorer url.

        :return: The explorer url based on the network.
        """
        return self.explorers[self.network].explorer_url

    def get_explorer_address_url(self, address: str = '') -> str:
        """
        Get the explorer url for the given address.
        If address is not provided, it will use the address of this client.

        :param address: address
        :return: The explorer url for the given address based on the network.
        """
        if not address:
            address = self.get_address()
        return self.explorers[self.network].get_address_url(address)

    def get_explorer_tx_url(self, tx_id: str) -> str:
        """
        Get the explorer url for the given transaction id.

        :param tx_id: str The transaction id
        :return: str The explorer url for the given transaction id based on the network.
        """
        if not tx_id:
            raise ValueError('tx_id is required')
        return self.explorers[self.network].get_tx_url(tx_id)

    @abc.abstractmethod
    async def get_balance(self, address: str = '') -> List[CryptoAmount]:
        """
        Get the balance of the wallet.

        :param address: Address to get the balance for (optional). If not provided, it will use the address of this client.
        :return: List of CryptoAmount objects representing the balance of each asset in the wallet.
        """
        pass

    async def get_gas_balance(self, address: str = '') -> CryptoAmount:
        """
        Get the balance of the gas asset for the given address.

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
        Check if the wallet has enough balance to send the given amount.

        :param amount: amount to send
        :return: True if the wallet has enough balance, False otherwise
        """
        balances = await self.get_balance()
        balance = next((b for b in balances if b.asset == amount.asset), None)
        if not balance:
            return False
        return balance.amount >= amount.amount

    def get_full_derivation_path(self, wallet_index: int) -> str:
        """
        Get the full derivation path for the given wallet index.

        :param wallet_index: int Wallet index to derive the path for.
        :return: str Full derivation path for the wallet index.
        """
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
            # noinspection PyUnresolvedReferences
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
    def gas_asset(self) -> Asset:
        """
        Get the gas asset for the chain.

        :return: Asset The gas asset for the chain, e.g. AssetRUNE, AssetETH, etc.
        """
        return self._gas_asset

    def _save_last_response(self, txid, result):
        if txid and result:
            self.last_response_dict[txid] = result

    def get_last_response(self, txid: str):
        """
        Get the last response for the given transaction ID.

        :param txid: str Transaction ID to get the last response for.
        :return: dict or None
        """
        return self.last_response_dict.get(txid)

    def clear_last_responses(self):
        """
        Clear the last responses dictionary. Useful for testing or resetting the client state.
        This method will remove all entries from the last_response_dict.
        """
        self.last_response_dict = {}

    @classmethod
    async def call_service(cls, method, *args):
        """
        This is a helper method to call a method of the underlying service in an asynchronous way.

        :param method: Method to call
        :param args: Arguments to pass to the method
        :return: Result of the method call
        """
        return await asyncio.get_event_loop().run_in_executor(
            None,
            method,
            *args
        )


class NoClient(XChainClient, abc.ABC):
    """
    This is a placeholder class for clients that do not have any implementation.
    """
    ...

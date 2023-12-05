import abc
from datetime import datetime
from decimal import Decimal
from typing import Optional, List, Union

from xchainpy2_client.explorer import ExplorerProvider
from xchainpy2_client.models import XcTx, Fees, TxPage, \
    FeeBounds, Fee, RootDerivationPaths, AssetInfo, FeeOption
from xchainpy2_crypto import validate_mnemonic, derive_private_key
from xchainpy2_utils import CryptoAmount, Chain, NetworkType, Asset, Amount

INF_FEE = Fee(1_000_000_000_000_000_000)


class XChainClient(abc.ABC):
    def __init__(self,
                 chain: Chain,
                 network: Optional[NetworkType] = None,
                 phrase: Optional[str] = None,
                 private_key: Union[str, bytes, callable, None] = None,
                 fee_bound: FeeBounds = FeeBounds(lower=Fee(0), upper=INF_FEE),
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

        self.fee_bound = fee_bound
        self.root_derivation_paths = root_derivation_paths

        self.network = network
        self.set_network(network)

        self.explorers = {network: ExplorerProvider('', '', '')}

        # NOTE: we don't call this.setPhrase() to void generating an address and paying the perf penalty
        if phrase:
            if not validate_mnemonic(phrase):
                raise Exception('Invalid phrase')
            self.phrase = phrase
        else:
            self.phrase = None

        self._private_key = private_key

        if private_key and phrase:
            raise Exception('Phrase and private key cannot be provided at the same time')

        self.native_asset: Optional[Asset] = None
        self._decimal = 8

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
        else:
            return derive_private_key(
                self.phrase,
                self.get_full_derivation_path(self.wallet_index)
            ).hex()

    def _throw_if_empty_phrase(self):
        if not self.phrase and not self._private_key:
            raise Exception('Phrase or private key must be provided to do this action')

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

    def gas_amount(self, amount: Union[float, str, int, Decimal]) -> CryptoAmount:
        """
        Easy way to construct CryptoAmount of gas asset
        :param amount: Union[float, str, int, Decimal] amount of asset (not base!)
        :return: CryptoAmount
        """
        return CryptoAmount(Amount.automatic(amount, self._decimal), self.native_asset)

    async def max_gas_amount(self, balances: List[CryptoAmount] = None) -> CryptoAmount:
        """
        Calculate maximum amount of Gas asset that you can send
        :param balances: (Optional) if you already have your balance, otherwise they will be loaded
        :return: CryptoAmount
        """
        if balances is None:
            balances = await self.get_balance()

        gas_balance = next((b for b in balances if b.asset == self.native_asset), None)
        if not gas_balance:
            return self.gas_amount(0)  # no gas at all

        fees = await self.get_fees()
        fee = fees.fees[FeeOption.FAST]
        max_value = gas_balance.amount.as_asset - fee.as_asset
        if max_value.internal_amount < 0:
            # less than fee
            return self.gas_amount(0)
        else:
            return CryptoAmount(max_value, self.native_asset)

    def set_network(self, network: NetworkType):
        if not network:
            raise Exception('Network must be provided')
        self.network = network

        # Fire off a warning in the console to indicate that stagenet and real assets are being used.
        if self.network == NetworkType.STAGENET:
            print("WARNING: This is using stagenet! Real assets are being used!")

    def get_network(self):
        return self.network

    def set_phrase(self, phrase: str, wallet_index: int = 0):
        if phrase:
            if not validate_mnemonic(phrase):
                raise Exception('Invalid phrase')
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
        return self.explorers[self.network].get_address_url(address)

    def get_explorer_tx_url(self, tx_id: str) -> str:
        """
        Get the explorer url for the given transaction id.
        :param tx_id: The transaction id
        :return: str The explorer url for the given transaction id based on the network.
        """
        return self.explorers[self.network].get_tx_url(tx_id)

    @abc.abstractmethod
    async def get_balance(self, address: str = '') -> List[CryptoAmount]:
        pass

    def get_full_derivation_path(self, wallet_index: int) -> str:
        if self.root_derivation_paths:
            # BREAKING CHANGE!
            # return f"{self.root_derivation_paths[self.network]}{wallet_index}'"  # original with apostrophe
            return f"{self.root_derivation_paths[self.network]}{wallet_index}"
        return ''

    @abc.abstractmethod
    async def get_transactions(self, address: str,
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

    @abc.abstractmethod
    async def broadcast_tx(self, tx_hex: str) -> str:
        pass

    @abc.abstractmethod
    def get_gas_asset(self) -> AssetInfo:
        pass

import abc
from datetime import datetime
from typing import Optional, List

from xchainpy2_client.models import XcTx, Fees, TxPage, \
    FeeBounds, Fee, RootDerivationPaths, AssetInfo
from xchainpy2_crypto import validate_mnemonic
from xchainpy2_utils import CryptoAmount, Chain, NetworkType, Asset

INF_FEE = Fee(1_000_000_000_000_000_000)


class XChainClient(abc.ABC):
    def __init__(self,
                 chain: Chain,
                 network: Optional[NetworkType] = None,
                 phrase: Optional[str] = None,
                 fee_bound: FeeBounds = FeeBounds(lower=Fee(0), upper=INF_FEE),
                 root_derivation_paths: Optional[RootDerivationPaths] = None,
                 ):
        """
        Client has to be initialised with network type and phrase.
        It will throw an error if an invalid phrase has been passed.

        :param chain: Chain name (see utils/chain.py)
        :param network: Network type (see utils/network_type.py)
        :param phrase: Mnemonic phrase
        :param fee_bound: Fee bounds
        :param root_derivation_paths: Root derivation paths for private key for each Network type
        """
        self.chain = chain

        self.fee_bound = fee_bound
        self.root_derivation_paths = root_derivation_paths

        self.network = NetworkType.MAINNET
        self.set_network(network)

        # NOTE: we don't call this.setPhrase() to void generating an address and paying the perf penalty
        if phrase:
            if not validate_mnemonic(phrase):
                raise Exception('Invalid phrase')
            self.phrase = phrase
        else:
            self.phrase = None

    @abc.abstractmethod
    def set_network(self, network: NetworkType):
        if not network:
            raise Exception('Network must be provided')
        self.network = network

        # Fire off a warning in the console to indicate that stagenet and real assets are being used.
        if self.network == NetworkType.STAGENET:
            print("WARNING: This is using stagenet! Real assets are being used!")

    @abc.abstractmethod
    def get_network(self):
        pass

    @abc.abstractmethod
    def set_phrase(self, phrase: str, wallet_index: int = 0):
        pass

    @abc.abstractmethod
    def purge_client(self):
        self.phrase = ''

    @abc.abstractmethod
    def get_explorer_url(self) -> str:
        pass

    @abc.abstractmethod
    def get_explorer_address_url(self, address: str) -> str:
        pass

    @abc.abstractmethod
    def get_explorer_tx_url(self, tx_id: str) -> str:
        pass

    @abc.abstractmethod
    def validate_address(self, address: str) -> bool:
        pass

    @abc.abstractmethod
    def get_address(self, wallet_index=0) -> str:
        pass

    @abc.abstractmethod
    async def get_balance(self, address: str) -> List[CryptoAmount]:
        ...

    def get_full_derivation_path(self, wallet_index: int) -> str:
        if self.root_derivation_paths:
            return f"{self.root_derivation_paths[self.network]}{wallet_index}'"
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
                       fee_rate: Optional[int] = None,
                       wallet_index: int = 0, **kwargs) -> str:
        pass

    @abc.abstractmethod
    async def broadcast_tx(self, tx_hex: str) -> str:
        pass

    @abc.abstractmethod
    def get_asset_info(self) -> AssetInfo:
        raise NotImplementedError()

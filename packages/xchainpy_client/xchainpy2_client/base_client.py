import abc
from typing import Optional, List

from packages.xchainpy_client.xchainpy2_client.models import TxParams, XcTx, Fees, TxHistoryParams, TxPage, \
    XChainClientParams, FeeBounds, Fee
from xchainpy2_crypto import validate_mnemonic
from xchainpy2_utils import Address, Asset, CryptoAmount, Chain, NetworkType

INF_FEE = Fee(1_000_000_000_000_000_000)


class XChainClient(abc.ABC):
    def __init__(self, chain: Chain, params: XChainClientParams):
        """
        Client has to be initialised with network type and phrase.
        It will throw an error if an invalid phrase has been passed.
        :param chain: chain type
        :param params: XChainClientParams
        """
        self.chain = chain

        self.fee_bound = params.fee_bound or FeeBounds(lower=Fee(0), upper=INF_FEE)
        self.root_derivation_paths = params.root_derivation_paths

        self.network = NetworkType.MAINNET
        self.set_network(params.network)

        # NOTE: we don't call this.setPhrase() to void generating an address and paying the perf penalty
        if params.phrase:
            if not validate_mnemonic(params.phrase):
                raise Exception('Invalid phrase')
            self.phrase = params.phrase
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
    async def get_transactions(self, params: Optional[TxHistoryParams]) -> TxPage:
        pass

    @abc.abstractmethod
    async def get_transaction_data(self, tx_id: str, asset_address: Optional[Address]) -> XcTx:
        pass

    @abc.abstractmethod
    async def get_fees(self) -> Fees:
        pass

    @abc.abstractmethod
    async def transfer(self, params: TxParams) -> XcTx:
        pass

    @abc.abstractmethod
    async def broadcast_tx(self, tx_hex: str) -> str:
        pass

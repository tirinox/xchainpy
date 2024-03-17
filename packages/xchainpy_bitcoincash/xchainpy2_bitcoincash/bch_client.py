import asyncio
from datetime import datetime
from typing import Optional, Union, List

from bitcash import PrivateKeyTestnet, PrivateKey
from bitcash.cashaddress import Address
from bitcash.exceptions import InvalidAddress
from bitcash.network import NetworkAPI

from xchainpy2_client import FeeBounds, RootDerivationPaths, XChainClient, Fees, XcTx, TxPage
from xchainpy2_utils import NetworkType, Asset, AssetBCH, Chain, CryptoAmount
from .const import ROOT_DERIVATION_PATHS, BCH_DECIMAL, DEFAULT_PROVIDER_NAMES, DEFAULT_BCH_EXPLORERS, \
    BCH_DEFAULT_FEE_BOUNDS, AssetTestBCH


class BitcoinCashClient(XChainClient):
    def __init__(self,
                 network=NetworkType.MAINNET,
                 phrase: Optional[str] = None,
                 private_key: Union[str, bytes, callable, None] = None,
                 fee_bound: Optional[FeeBounds] = BCH_DEFAULT_FEE_BOUNDS,
                 root_derivation_paths: Optional[RootDerivationPaths] = ROOT_DERIVATION_PATHS,
                 explorer_providers=DEFAULT_BCH_EXPLORERS,
                 wallet_index=0,
                 provider_names=DEFAULT_PROVIDER_NAMES):
        """
        BitcoinCashClient interface
        Constructor to create a new Do.

        :param network: The network type
        :param phrase: The seed phrase
        :param private_key: The private key
        :param fee_bound: The fee bound
        :param root_derivation_paths: The root derivation paths
        :param explorer_providers: The explorer providers
        :param wallet_index: The wallet index (default is 0)
        :param provider_names: The provider names
        """

        super().__init__(
            network=network,
            phrase=phrase,
            private_key=private_key,
            fee_bound=fee_bound,
            root_derivation_paths=root_derivation_paths,
            wallet_index=wallet_index,
            chain=Chain.BitcoinCash,
        )

        self._prefix = "bitcoincash:"
        self._decimal = BCH_DECIMAL
        self.explorers = explorer_providers
        self.gas_assets = AssetBCH if network != NetworkType.TESTNET else AssetTestBCH

        if not provider_names:
            provider_names = DEFAULT_PROVIDER_NAMES
        self.provider_names = provider_names
        self.api = NetworkAPI()

    def validate_address(self, address: str) -> bool:
        try:
            Address.from_string(address)
            return True
        except InvalidAddress:
            return False

    def get_private_key_bitcash(self) -> Union[PrivateKey, PrivateKeyTestnet]:
        _class = PrivateKeyTestnet if self.network == NetworkType.TESTNET else PrivateKey
        return _class.from_hex(self.get_private_key())

    def get_public_key(self) -> bytes:
        return self.get_private_key_bitcash().public_key

    def get_address(self) -> str:
        return self.get_private_key_bitcash().address

    async def get_balance(self, address: str = '') -> List[CryptoAmount]:
        result = await self._call_service(self.api.get_balance, address or self.get_address())
        return [self.gas_base_amount(result)]

    async def get_transactions(self, address: str, offset: int = 0, limit: int = 0,
                               start_time: Optional[datetime] = None, end_time: Optional[datetime] = None,
                               asset: Optional[Asset] = None) -> TxPage:
        pass

    async def get_transaction_data(self, tx_id: str) -> Optional[XcTx]:
        pass

    async def get_fees(self) -> Fees:
        pass

    async def transfer(self, what: CryptoAmount, recipient: str, memo: Optional[str] = None,
                       fee_rate: Optional[int] = None, **kwargs) -> str:
        pass

    async def broadcast_tx(self, tx_hex: str) -> str:
        pass

    @staticmethod
    async def _call_service(method, *args):
        return await asyncio.get_event_loop().run_in_executor(
            None,
            method,
            *args
        )




from datetime import datetime
from typing import Optional, Union, List

from xchainpy2_client import AssetInfo, Fees, XChainClient, XcTx, TxPage
from xchainpy2_client import RootDerivationPaths, FeeBounds
from xchainpy2_utils import Chain, NetworkType, CryptoAmount, Asset, AssetBTC
from . import get_btc_address_prefix
from .const import BTC_DECIMAL


class BitcoinClient(XChainClient):
    def get_explorer_url(self) -> str:
        ...

    def get_explorer_address_url(self, address: str) -> str:
        ...

    def get_explorer_tx_url(self, tx_id: str) -> str:
        ...

    async def get_balance(self, address: str = '') -> List[CryptoAmount]:
        ...

    async def get_transactions(self, address: str, offset: int = 0, limit: int = 10,
                               start_time: Optional[datetime] = None, end_time: Optional[datetime] = None,
                               asset: Optional[Asset] = None,
                               height=None, detailed=False) -> TxPage:
        ...

    async def get_transaction_data(self, tx_id: str) -> Optional[XcTx]:
        ...

    async def transfer(self, what: CryptoAmount, recipient: str, memo: Optional[str] = None,
                       fee_rate: Optional[int] = None, is_sync: bool = True, **kwargs) -> str:
        ...

    async def broadcast_tx(self, tx_hex: str, is_sync=True) -> str:
        ...

    async def get_fees(self) -> Fees:
        ...

    def get_address(self) -> str:
        ...

    def get_public_key(self):
        ...

    def get_private_key_cosmos(self):
        ...

    def get_private_key(self) -> str:
        # todo: add to base client
        ...

    def __init__(self,
                 network=NetworkType.MAINNET,
                 phrase: Optional[str] = None,
                 private_key: Union[str, bytes, callable, None] = None,
                 fee_bound: Optional[FeeBounds] = None,
                 root_derivation_paths: Optional[RootDerivationPaths] = None,
                 wallet_index=0,
                 ):

        super().__init__(
            Chain.Bitcoin,
            network, phrase,
            private_key, fee_bound,
            root_derivation_paths,
            wallet_index
        )

        self._prefix = get_btc_address_prefix(network)
        self._decimal = BTC_DECIMAL
        self.native_asset = AssetBTC

    def validate_address(self, address: str) -> bool:
        ...

    def get_asset_info(self) -> AssetInfo:
        return AssetInfo(
            AssetBTC, BTC_DECIMAL
        )

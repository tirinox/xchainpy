from datetime import datetime
from typing import Optional, Union, List

from xchainpy2_client import XChainClient, FeeBounds, RootDerivationPaths, Fees, XcTx, TxPage
from xchainpy2_utils import NetworkType, Chain, AssetRUNE, CryptoAmount, Asset


class MockChainClient(XChainClient):
    def validate_address(self, address: str) -> bool:
        pass

    def get_address(self) -> str:
        pass

    def get_public_key(self):
        pass

    async def get_balance(self, address: str = '') -> List[CryptoAmount]:
        pass

    async def get_transactions(self, address: str = '', offset: int = 0, limit: int = 0,
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

    def __init__(self,
                 network=NetworkType.MAINNET,
                 phrase: Optional[str] = None,
                 private_key: Union[str, bytes, callable, None] = None,
                 fee_bound: Optional[FeeBounds] = None,
                 root_derivation_paths: Optional[RootDerivationPaths] = None,
                 client_urls=None,
                 chain_ids=None,
                 explorer_providers=None,
                 wallet_index=0,
                 ):
        super().__init__(Chain.Cosmos, network, phrase, private_key, fee_bound, root_derivation_paths, wallet_index)

        self.explorers = explorer_providers

        if isinstance(client_urls, str):
            client_urls = {NetworkType.MAINNET: client_urls}

        self._gas_asset = AssetRUNE
        self._prefix = 'mock'

        self._denom = 'mock_d'
        self._decimal = 7
        self._gas_limit = 3333

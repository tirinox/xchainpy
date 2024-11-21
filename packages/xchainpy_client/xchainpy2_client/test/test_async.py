from datetime import datetime
from time import sleep
from typing import Optional, List

import pytest

from xchainpy2_client import XChainClient, Fees, XcTx, TxPage
from xchainpy2_utils import CryptoAmount, Asset, Chain


class MyClient(XChainClient):
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

    async def some_method(self, arg):
        return await self.call_service(self._some_methods_sync, arg)

    def _some_methods_sync(self, x):
        sleep(0.1)
        return x + "foo"


@pytest.mark.asyncio
async def test_call_service():
    cli = MyClient(chain=Chain.Bitcoin)
    assert await cli.some_method('bar') == 'barfoo'

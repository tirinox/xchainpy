from abc import ABC, abstractmethod
from typing import List

from xchainpy2_client import XcTx
from xchainpy2_utils import CryptoAmount, Chain, NetworkType


class EVMDataProvider(ABC):
    def __init__(self, chain: Chain, network: NetworkType, **kwargs):
        self.chain = chain
        self.network = network
        self.kwargs = kwargs

    @abstractmethod
    async def get_erc20_token_balances(self, address: str) -> List[CryptoAmount]:
        ...

    @abstractmethod
    async def get_address_transactions(self, address: str) -> List[XcTx]:
        ...

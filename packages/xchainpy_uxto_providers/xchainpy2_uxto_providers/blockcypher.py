import asyncio
from datetime import datetime
from enum import Enum
from typing import Optional, List

from aiohttp import ClientSession
from pydantic import BaseModel

from xchainpy2_client import UtxoOnlineDataProvider, XcTx, TxPage, UTXO
from xchainpy2_utils import Asset, CryptoAmount, Chain, AssetBTC, Amount


class BlockcypherNetwork(Enum):
    BTC = 'btc/main'
    BTC_TEST = 'btc/test3'
    LTC = 'ltc/main'
    DOGE = 'doge/main'
    DASH = 'dash/main'


class AddressTxDTO(BaseModel, extra='allow'):
    tx_hash: str
    block_height: int
    confirmed: str


class TxInput(BaseModel, extra='allow'):
    output_value: str
    addresses: List[str]
    script_type: Optional[str]


class TxOutput(BaseModel, extra='allow'):
    value: str
    addresses: List[str]
    script_type: Optional[str]
    script: str


class Transaction(BaseModel, extra='allow'):
    hash: str
    block_hash: str
    confirmed: str

    hex: str
    inputs: List[TxInput]
    outputs: List[TxOutput]


class GetBalanceDTO(BaseModel, extra='allow'):
    balance: int
    unconfirmed_balance: int
    final_balance: int
    n_tx: int
    unconfirmed_n_tx: int
    final_n_tx: int


class BlockCypherProvider(UtxoOnlineDataProvider):
    DEFAULT_BASE_URL = 'https://api.blockcypher.com/v1/'

    def __init__(self, chain: Chain, asset: Asset, asset_decimal: int, network: BlockcypherNetwork,
                 api_key: str = '', session: ClientSession = None, base_url=DEFAULT_BASE_URL,
                 concurrency=3) -> None:
        super().__init__()
        self.api_key = api_key
        self.chain = chain
        self.asset = asset
        self.asset_decimal = asset_decimal
        self.network = network
        self.session = session or ClientSession()
        self.base_url = base_url
        self.delay = 1.0
        self.semaphore = asyncio.Semaphore(concurrency)

    @classmethod
    def default_bitcoin(cls, session: ClientSession = None, api_key: str = ''):
        return cls(Chain.Bitcoin, AssetBTC, 8, BlockcypherNetwork.BTC, api_key=api_key, session=session)

    async def get_confirmed_unspent_txs(self, address: str) -> List[UTXO]:
        pass

    async def get_unspent_txs(self, address: str) -> List[UTXO]:
        pass

    def build_url(self, endpoint: str) -> str:
        return f'{self.base_url}/{self.network.value}/{endpoint}'

    async def broadcast_tx(self, tx_hex: str) -> str:
        url = self.build_url('txs/push')
        params = self._params()
        async with self.session.post(url, data={'tx': tx_hex}, params=params) as resp:
            j = await resp.json()
            return j['tx']['hash']

    async def get_balance(self, address: str, confirmed_only=False) -> List[CryptoAmount]:
        balance = await self._api_get_balance(address)
        confirmed_amount = Amount.from_base(balance.balance, self.asset_decimal)
        unconfirmed_amount = Amount.from_base(balance.final_balance, self.asset_decimal)
        amount = confirmed_amount if confirmed_only else unconfirmed_amount
        return [CryptoAmount(amount, self.asset)]

    async def get_transactions(self, address: str, offset: int = 0, limit: int = 0,
                               start_time: Optional[datetime] = None, end_time: Optional[datetime] = None,
                               asset: Optional[Asset] = None) -> TxPage:
        pass

    async def get_transaction_data(self, tx_id: str) -> XcTx:
        pass

    def _params(self, **kwargs):
        if self.api_key:
            kwargs['token'] = self.api_key
        return {k: v for k, v in kwargs.items() if v is not None}

    @staticmethod
    def _bool_to_str(value: bool) -> str:
        return str(value).lower()

    async def _api_get_txs(self, address: str, limit: int = 0, before_block: int = 0,
                           unspent_only=False):
        params = self._params(limit=limit,
                              unspentOnly=self._bool_to_str(unspent_only),
                              before=before_block or None)

        url = self.build_url(f'addrs/{address}')
        async with self.session.get(url, params=params) as resp:
            j = await resp.json()
            return [AddressTxDTO(**tx) for tx in j['txrefs']]

    async def _api_get_tx(self, tx_hash: str) -> Optional[Transaction]:
        async with self.semaphore:
            await asyncio.sleep(self.delay)
            params = self._params()
            url = self.build_url(f'txs/{tx_hash}')
            async with self.session.get(url, params=params) as resp:
                j = await resp.json()
                return Transaction(**j)

    async def _api_get_balance(self, address: str):
        params = self._params()
        url = self.build_url(f'addrs/{address}/balance')

        async with self.session.get(url, params=params) as resp:
            j = await resp.json()
            return GetBalanceDTO(**j)

    async def get_raw_transaction(self, address: str, offset: int = 0, limit: int = 0,
                                  start_time: Optional[datetime] = None, end_time: Optional[datetime] = None,
                                  asset: Optional[Asset] = None, unspent_only=False) -> List[Transaction]:
        offset = offset or 0
        limit = limit or 10
        if offset + limit > 2000:
            raise Exception('offset + limit must be less than 2000')

        if offset < 0 or limit < 0:
            raise Exception('offset and limit must be greater than 0')

        response = await self._api_get_txs(address, offset, unspent_only=unspent_only)

        unique_tx_hashes = list(set(tx.tx_hash for tx in response))
        start = min(len(unique_tx_hashes), offset)
        end = min(len(unique_tx_hashes), offset + limit)
        txs_to_fetch = unique_tx_hashes[start:end]
        tx_hashes_to_fetch = txs_to_fetch[:limit]

        r = await asyncio.gather(*[
            self._api_get_tx(tx_hash) for tx_hash in tx_hashes_to_fetch
        ])
        return r

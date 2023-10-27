import asyncio
from datetime import datetime

import math
from aiohttp import ClientSession

from xchainpy2_client import UtxoOnlineDataProvider, XcTx, TxPage, UTXO, TxType, TxTo, TxFrom, Witness
from xchainpy2_utils import Chain, Asset, CryptoAmount, Amount, AssetBTC, AssetLTC, AssetDOGE
from .sochain_t import *


class SochainProvider(UtxoOnlineDataProvider):
    DEFAULT_BASE_URL = 'https://sochain.com/api/v3'

    @classmethod
    def default_bitcoin(cls, session: ClientSession = None, api_key: str = ''):
        return cls(Chain.Bitcoin, AssetBTC, 8, SochainNetwork.BTC, api_key=api_key, session=session)

    @classmethod
    def default_bitcoin_test(cls, session: ClientSession = None, api_key: str = ''):
        return cls(Chain.Bitcoin, AssetBTC, 8, SochainNetwork.BTC_TEST, api_key=api_key, session=session)

    @classmethod
    def default_litecoin(cls, session: ClientSession = None, api_key: str = ''):
        return cls(Chain.Litecoin, AssetLTC, 8, SochainNetwork.LTC, api_key=api_key, session=session)

    @classmethod
    def default_litecoin_test(cls, session: ClientSession = None, api_key: str = ''):
        return cls(Chain.Litecoin, AssetLTC, 8, SochainNetwork.LTC_TEST, api_key=api_key, session=session)

    @classmethod
    def default_doge(cls, session: ClientSession = None, api_key: str = ''):
        return cls(Chain.Doge, AssetDOGE, 8, SochainNetwork.DOGE, api_key=api_key, session=session)

    @classmethod
    def default_doge_test(cls, session: ClientSession = None, api_key: str = ''):
        return cls(Chain.Doge, AssetDOGE, 8, SochainNetwork.DOGE_TEST, api_key=api_key, session=session)

    def __init__(self, chain: Chain, asset: Asset, asset_decimal: int, network: SochainNetwork,
                 session: ClientSession = None, base_url=DEFAULT_BASE_URL, api_key: str = '',
                 concurrency=5) -> None:
        super().__init__()
        self.chain = chain
        self.asset = asset
        self.asset_decimal = asset_decimal
        self.network = network
        self.session = session or ClientSession()
        self.base_url = base_url
        self.api_key = api_key
        self.batch_size = 10
        self._semaphore = asyncio.Semaphore(concurrency)

    async def get_confirmed_unspent_txs(self, address: str) -> List[UTXO]:
        utxos = await self._api_get_unspent_txs(address, page=1, batch_size=self.batch_size)
        confirmed_utxos = [utxo for utxo in utxos if utxo.block]
        return self._convert_utxos(confirmed_utxos)

    async def get_unspent_txs(self, address: str) -> List[UTXO]:
        utxos = await self._api_get_unspent_txs(address, page=1, batch_size=self.batch_size)
        return self._convert_utxos(utxos)

    async def broadcast_tx(self, tx_hex: str) -> str:
        return await self._api_broadcast(tx_hex)

    async def get_balance(self, address: str) -> List[CryptoAmount]:
        balance = await self._api_get_balance(address)
        return [
            CryptoAmount(amount=Amount.from_base(balance, self.asset_decimal), asset=self.asset)
        ]

    async def get_transactions(self, address: str, offset: int = 0, limit: int = 0,
                               start_time: Optional[datetime] = None, end_time: Optional[datetime] = None,
                               asset: Optional[Asset] = None) -> TxPage:
        offset = offset or 0
        limit = limit or 10
        if offset < 0 or limit < 0:
            raise Exception('Offset and limit must be positive')

        first_page_no = int(math.floor(offset / self.batch_size) + 1)
        if limit > self.batch_size:
            last_page_no = int(first_page_no + math.floor(limit / self.batch_size))
        else:
            last_page_no = first_page_no
        offset_of_first_page = offset % self.batch_size

        tx_hashes_to_fetch = []
        page = first_page_no
        while page <= last_page_no:
            response = await self._api_get_transactions(address, page)
            this_page_txs = response.transactions
            if not this_page_txs:
                break
            if page == first_page_no and len(this_page_txs) > offset_of_first_page:
                txs_to_get = this_page_txs[offset_of_first_page:]
            else:
                txs_to_get = this_page_txs

            # add up to limit
            for tx in txs_to_get:
                if len(tx_hashes_to_fetch) < limit:
                    tx_hashes_to_fetch.append(tx.txid)
                else:
                    break

        txs = await asyncio.gather(*[self.get_transaction_data(tx_hash) for tx_hash in tx_hashes_to_fetch])

        return TxPage(
            total=len(tx_hashes_to_fetch),
            txs=list(txs),
        )

    async def get_transaction_data(self, tx_id: str) -> Optional[XcTx]:
        async with self._semaphore:
            tx_data = await self._api_request(f'transaction/{self.network.value}/{tx_id}')
            return self._convert_tx(tx_data['data'])

    def build_url(self, path: str) -> str:
        return f'{self.base_url}/{path}'

    async def _api_request(self, url):
        async with self.session.get(url, headers=self._headers) as resp:
            return await resp.json()

    @property
    def _headers(self):
        return {'API-KEY': self.api_key}

    async def _api_broadcast(self, tx_hex: str):
        url = self.build_url(f'broadcast_transaction/{self.network.value}')
        async with self.session.post(url, json={'tx_hex': tx_hex}, hearders=self._headers) as resp:
            j = await resp.json()
            return j['tx_hex']

    async def _api_get_balance(self, address: str, confirmed_only=False):
        url = self.build_url(f'balance/{self.network.value}/{address}')
        j = await self._api_request(url)
        data = GetBalanceDTO(**j['data'])
        confirmed = Amount.from_base(data.confirmed, self.asset_decimal)
        unconfirmed = Amount.from_base(data.unconfirmed, self.asset_decimal)
        net_amount = confirmed if confirmed_only else confirmed + unconfirmed
        return net_amount

    async def _api_get_transactions(self, address: str, page: int = 0):
        url = self.build_url(f'transactions/{self.network.value}/{address}/{page}')
        j = await self._api_request(url)
        data = j['data']
        if 'error_message' in data:
            return
        return GetTxsDTO(**data)

    async def _api_get_unspent_txs(self, address: str, page: int, batch_size=10):
        results = []
        while True:
            url = self.build_url(f'unspent_outputs/{self.network.value}/{address}/{page}')
            j = await self._api_request(url)
            this_page = [AddressUTXO(**output) for output in j['data']['outputs']]
            results.extend(this_page)

            if len(this_page) < batch_size:
                break

            page += 1
        return results

    def _convert_tx(self, tx: Transaction) -> XcTx:
        return XcTx(
            asset=self.asset,
            from_txs=[
                TxFrom(
                    i.address,
                    tx.hash,
                    Amount.from_base(i.value, self.asset_decimal), self.asset
                ) for i in tx.inputs
            ],
            to_txs=[
                TxTo(
                    o.address,
                    Amount.from_base(o.value, self.asset_decimal),
                    self.asset
                ) for o in tx.outputs
                if o.type != 'nulldata'
            ],
            date=datetime.fromtimestamp(tx.time),  # todo convert to datetime (checkit)
            type=TxType.TRANSFER,
            hash=tx.txid,
            height=tx.block_no,
        )

    def _convert_utxos(self, utxos: List[AddressUTXO]) -> List[UTXO]:
        return [
            UTXO(
                hash=utxo.txid,
                index=utxo.index,
                value=(value := Amount.from_base(utxo.value, self.asset_decimal)),
                witness_utxo=Witness(
                    value=value,
                    script=bytes.fromhex(utxo.script_hex),
                ),
                tx_hex=utxo.tx_hex,
            ) for utxo in utxos
        ]

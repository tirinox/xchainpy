import asyncio
from datetime import datetime

from aiohttp import ClientSession

from xchainpy2_client import UtxoOnlineDataProvider, XcTx, TxPage, UTXO, TxType, TxTo, TxFrom, Witness
from xchainpy2_utils import Asset, CryptoAmount, Chain, Amount, AssetBTC, AssetBCH
from .haskoin_t import *


class HaskoinProvider(UtxoOnlineDataProvider):
    DEFAULT_BASE_URL = 'https://api.haskoin.com/'

    def __init__(self, chain: Chain, asset: Asset, asset_decimal: int, network: HaskoinNetwork,
                 api_key: str = '', session: ClientSession = None, base_url=DEFAULT_BASE_URL) -> None:
        super().__init__()
        self.api_key = api_key
        self.chain = chain
        self.asset = asset
        self.asset_decimal = asset_decimal
        self.network = network
        self.base_url = base_url
        self.session = session
        self._confirmed_tx_cache = set()
        self._tx_hex_cache = {}

    @classmethod
    def default_bitcoin(cls, session: ClientSession = None, api_key: str = ''):
        return cls(Chain.Bitcoin, AssetBTC, 8, HaskoinNetwork.BTC, api_key=api_key, session=session)

    @classmethod
    def test_bitcoin(cls, session: ClientSession = None, api_key: str = ''):
        return cls(Chain.Bitcoin, AssetBTC, 8, HaskoinNetwork.BTC_TEST, api_key=api_key, session=session)

    @classmethod
    def default_bitcoin_cash(cls, session: ClientSession = None, api_key: str = ''):
        return cls(Chain.BitcoinCash, AssetBCH, 8, HaskoinNetwork.BCH, api_key=api_key, session=session)

    @classmethod
    def test_bitcoin_cash(cls, session: ClientSession = None, api_key: str = ''):
        return cls(Chain.BitcoinCash, AssetBCH, 8, HaskoinNetwork.BCH_TEST, api_key=api_key, session=session)

    async def get_confirmed_unspent_txs(self, address: str, with_hex=True) -> List[UTXO]:
        all_unspent = await self._api_get_unspent_txs(address)
        confirmed = [t for t in all_unspent if t.block]  # todo: check this?
        utxos = self._convert_utxos(confirmed)
        await self._fill_tx_hex(utxos, with_hex)
        return utxos

    async def get_unspent_txs(self, address: str, with_hex=True) -> List[UTXO]:
        all_unspent = await self._api_get_unspent_txs(address)
        utxos = self._convert_utxos(all_unspent)
        await self._fill_tx_hex(utxos, with_hex)
        return utxos

    async def broadcast_tx(self, tx_hex: str) -> str:
        return await self._api_broadcast(tx_hex)

    async def get_balance(self, address: str, confirmed_only: bool = False) -> List[CryptoAmount]:
        account = await self._api_get_account(address)
        balance_raw = account.confirmed if confirmed_only else account.unconfirmed
        return [
            CryptoAmount(amount=Amount.from_base(balance_raw, self.asset_decimal), asset=self.asset)
        ]

    async def get_transactions(self, address: str, offset: int = 0, limit: int = 0,
                               start_time: Optional[datetime] = None, end_time: Optional[datetime] = None,
                               asset: Optional[Asset] = None) -> TxPage:
        limit = limit or 10
        offset = offset or 0
        if offset + limit > 2000:
            raise Exception('Cannot fetch more than last 2000 txs (offset + limit)')

        if offset < 0 or limit < 0:
            raise Exception('Offset and limit must be positive')

        txs = await self._api_get_raw_transactions(address, offset, limit)
        txs = [self._convert_tx(tx) for tx in txs]
        return TxPage(total=len(txs), txs=txs)

    async def get_transaction_data(self, tx_id: str) -> XcTx:
        tx = await self._api_get_tx(tx_id)
        return self._convert_tx(tx)

    def build_url(self, endpoint: str) -> str:
        return f'{self.base_url}/{self.network.value}/{endpoint}'

    async def _api_request(self, url: str, thing: str, params=None):
        async with self.session.get(url, params=params) as resp:
            if resp.status != 200:
                raise Exception(f'Error {thing}: {resp.status}')
            j = await resp.json()
            if 'error' in j:
                raise Exception(f'Error {thing} : {j["error"]}')
            return j['data']

    async def _api_get_account(self, address: str) -> AddressDTO:
        url = self.build_url(f'address/{address}/balance')
        data = await self._api_request(url, 'getting account')
        return AddressDTO(**data)

    async def _api_get_tx(self, tx_id: str) -> Transaction:
        url = self.build_url(f'transaction/{tx_id}')
        data = await self._api_request(url, 'getting tx')
        return Transaction(**data)

    async def _api_get_raw_tx(self, tx_id: str) -> str:
        url = self.build_url(f'transaction/{tx_id}/raw')
        return await self._api_request(url, 'getting raw tx')

    async def _api_get_raw_transactions(self, address: str, offset: int = 0, limit: int = 100):
        url = self.build_url(f'address/{address}/transactions/full')
        params = {
            'offset': offset,
            'limit': limit,
        }
        data = await self._api_request(url, 'getting raw txs', params)
        return [Transaction(**tx) for tx in data]

    async def _api_get_unspent_txs(self, address: str, limit=None):
        if limit is None:
            account = await self._api_get_account(address)
            limit = account.utxo

        url = self.build_url(f'address/{address}/unspent?limit={limit}')
        data = await self._api_request(url, 'getting unspent txs')
        return [TxUnspent(**utxo) for utxo in data]

    async def _api_get_confirmed_tx_status(self, txid: str) -> bool:
        if txid in self._confirmed_tx_cache:
            return True
        tx = await self._api_get_tx(txid)
        if confirmed := tx.confirmations >= 1:
            self._confirmed_tx_cache.add(txid)
        return confirmed

    # async def _api_get_unspent_txs_2(self, address: str) -> List[TxUnspent]:
    #     unspent = await self._api_get_unspent_txs(address)
    #     txs = await asyncio.gather(*[self._api_get_tx(tx.txid) for tx in unspent])
    #     return list(txs)
    #
    # async def _api_get_confirmed_unspent_txs_2(self, address: str) -> List[TxUnspent]:
    #     unspent = await self._api_get_unspent_txs(address)
    #     return [tx for tx in unspent if tx.confirmations >= 1]

    async def _api_get_tx_hex(self, txid: str) -> str:
        if txid in self._tx_hex_cache:
            return self._tx_hex_cache[txid]
        tx_hex = await self._api_get_raw_tx(txid)
        self._tx_hex_cache[txid] = tx_hex
        return tx_hex

    async def _api_broadcast(self, tx_hex: str) -> str:
        url = self.build_url('transactions')

        for retry in range(5):
            async with self.session.post(url, data=tx_hex) as resp:
                if resp.status == 500:
                    await asyncio.sleep(retry * 0.2)
                    continue
                else:
                    j = await resp.json()
                    return j['txid']
        raise Exception('Error broadcasting tx. Max retries exceeded')

    def _convert_tx(self, tx: Transaction) -> XcTx:
        return XcTx(
            asset=self.asset,
            from_txs=[
                TxFrom(
                    from_address=i.address,
                    from_tx_hash=tx.txid,
                    amount=Amount.from_base(i.value, self.asset_decimal),
                    asset=self.asset,
                ) for i in tx.inputs
            ],
            to_txs=[
                TxTo(
                    address=o.address,
                    amount=Amount.from_base(o.value, self.asset_decimal),
                    asset=self.asset,
                ) for o in tx.outputs
                if o.script != 'null-data'  # filter out op_return outputs
            ],
            date=datetime.fromtimestamp(tx.time),
            type=TxType.TRANSFER,
            hash=tx.txid,
            height=tx.block.height,
        )

    def _convert_utxos(self, utxos: List[TxUnspent]) -> List[UTXO]:
        return [
            UTXO(
                u.txid, u.index,
                (value := Amount.from_base(u.value, self.asset_decimal).internal_amount),
                witness_utxo=Witness(
                    value, bytes.fromhex(u.pkscript)
                ),
                tx_hex=''
            ) for u in utxos
        ]

    async def _fill_tx_hex(self, utxos: List[UTXO], with_hex=False):
        if with_hex:
            txs = await asyncio.gather(*[self._api_get_tx_hex(tx.hash) for tx in utxos])
            for tx, tx_hex in zip(utxos, txs):
                tx.tx_hex = tx_hex

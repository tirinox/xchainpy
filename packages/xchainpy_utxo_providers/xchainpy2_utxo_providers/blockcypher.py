import asyncio
from datetime import datetime

from aiohttp import ClientSession

from xchainpy2_client import UtxoOnlineDataProvider, XcTx, TxPage, UTXO, Witness, TokenTransfer, TxType
from xchainpy2_utils import Asset, CryptoAmount, Chain, AssetBTC, Amount, AssetLTC, AssetDOGE, AssetDASH, parse_iso_date
from .blockcypher_t import *


class BlockCypherProvider(UtxoOnlineDataProvider):
    DEFAULT_BASE_URL = 'https://api.blockcypher.com/v1'

    def __init__(self, chain: Chain, asset: Asset, asset_decimal: int, network: BlockcypherNetwork,
                 api_key: str = '', session: ClientSession = None, base_url=DEFAULT_BASE_URL,
                 concurrency=3) -> None:

        assert chain in (Chain.Bitcoin, Chain.Litecoin, Chain.Doge, Chain.Dash), f"BlockCypher does not support {chain}"

        super().__init__()

        self.api_key = api_key
        self.chain = chain
        self.asset = asset
        self.asset_decimal = asset_decimal
        self.network = network
        self.session = session or ClientSession()
        self.base_url = base_url
        self.delay = 1.0
        self._semaphore = asyncio.Semaphore(concurrency)

    @classmethod
    def default_bitcoin(cls, session: ClientSession = None, api_key: str = ''):
        return cls(Chain.Bitcoin, AssetBTC, 8, BlockcypherNetwork.BTC, api_key=api_key, session=session)

    @classmethod
    def default_litecoin(cls, session: ClientSession = None, api_key: str = ''):
        return cls(Chain.Litecoin, AssetLTC, 8, BlockcypherNetwork.LTC, api_key=api_key, session=session)

    @classmethod
    def default_doge(cls, session: ClientSession = None, api_key: str = ''):
        return cls(Chain.Doge, AssetDOGE, 8, BlockcypherNetwork.DOGE, api_key=api_key, session=session)

    @classmethod
    def default_dash(cls, session: ClientSession = None, api_key: str = ''):
        return cls(Chain.Dash, AssetDASH, 8, BlockcypherNetwork.DASH, api_key=api_key, session=session)

    async def get_confirmed_unspent_txs(self, address: str) -> List[UTXO]:
        all_unspent = await self.get_raw_transaction(address, limit=2000)
        all_unspent = [tx for tx in all_unspent if tx.confirmed]
        return self.convert_utxos(address, all_unspent)

    async def get_unspent_txs(self, address: str) -> List[UTXO]:
        all_unspent = await self.get_raw_transaction(address, limit=2000)
        return self.convert_utxos(address, all_unspent)

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
        if balance is None:
            return []
        confirmed_amount = Amount.from_base(balance.balance, self.asset_decimal)
        unconfirmed_amount = Amount.from_base(balance.final_balance, self.asset_decimal)
        amount = confirmed_amount if confirmed_only else unconfirmed_amount
        return [CryptoAmount(amount, self.asset)]

    async def get_transactions(self, address: str, offset: int = 0, limit: int = 0,
                               start_time: Optional[datetime] = None, end_time: Optional[datetime] = None,
                               asset: Optional[Asset] = None) -> TxPage:
        raw_txs = await self.get_raw_transaction(address, offset, limit, start_time, end_time, asset)
        txs = [self.convert_tx(tx) for tx in raw_txs]
        return TxPage(len(txs), txs)

    async def get_transaction_data(self, tx_id: str) -> Optional[XcTx]:
        tx = await self._api_get_tx(tx_id)
        return self.convert_tx(tx)

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
        async with self._semaphore:
            await asyncio.sleep(self.delay)
            params = self._params()
            url = self.build_url(f'txs/{tx_hash}')
            async with self.session.get(url, params=params) as resp:
                j = await resp.json()
                if 'error' in j:
                    raise Exception(f'Error getting tx: {j["error"]}')
                return Transaction(**j)

    async def _api_get_balance(self, address: str):
        params = self._params()
        url = self.build_url(f'addrs/{address}/balance')

        async with self.session.get(url, params=params) as resp:
            j = await resp.json()
            if 'error' in j:
                raise Exception(f'Error getting balance: {j["error"]}')
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
        return list(r)

    def convert_utxos(self, address, utxos: List[Transaction]) -> List[UTXO]:
        utxos_out = []
        for utxo in utxos:
            for output in utxo.outputs:
                if output.addresses and output.addresses[0] == address:
                    value = Amount.from_base(output.value, self.asset_decimal).internal_amount
                    utxos_out.append(UTXO(
                        utxo.hash, utxo.index,
                        value,
                        witness_utxo=Witness(value, bytes.fromhex(output.script)),
                        tx_hex=utxo.hex
                    ))
        return utxos_out

    def convert_tx(self, tx: Transaction, our_address: str = '') -> Optional[XcTx]:
        if not tx:
            return None

        date = parse_iso_date(tx.confirmed)
        transfers = [
            TokenTransfer(inp.addresses[0], our_address,
                          Amount.from_base(inp.output_value, self.asset_decimal), self.asset, tx.hash,
                          outbound=False)
            for inp in tx.inputs
        ]
        transfers.extend([
            TokenTransfer(our_address, out.addresses[0],
                          Amount.from_base(out.value, self.asset_decimal), self.asset, tx.hash)
            for out in tx.outputs
            if out.script_type != 'null-data'  # filter out op_return outputs
        ])

        return XcTx(
            self.asset,
            transfers=transfers,
            date=date,
            type=TxType.TRANSFER,
            hash=tx.hash,
            height=tx.block_height,
        )

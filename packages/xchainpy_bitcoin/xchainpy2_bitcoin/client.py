import asyncio
from datetime import datetime
from typing import Optional, Union, List

from bitcoinlib.config.config import MAX_TRANSACTIONS
from bitcoinlib.keys import Key, deserialize_address
from bitcoinlib.services.services import Service
from bitcoinlib.transactions import Transaction, Output

from xchainpy2_client import Fees, XChainClient, XcTx, TxPage, TxType, TokenTransfer, FeeType, \
    FeeOption
from xchainpy2_client import RootDerivationPaths, FeeBounds
from xchainpy2_utils import Chain, NetworkType, CryptoAmount, Asset, AssetBTC
from .const import BTC_DECIMAL, BLOCKSTREAM_EXPLORERS, ROOT_DERIVATION_PATHS
from .utils import get_btc_address_prefix, try_get_memo_from_output, compile_memo


class BitcoinClient(XChainClient):
    DEFAULT_PROVIDER_NAME = 'mempool'

    async def get_balance(self, address: str = '') -> List[CryptoAmount]:
        address = address or self.get_address()
        result = await self._call_service(self.service.getbalance, address)
        return [self.gas_amount(result)]

    async def get_transactions(self, address: str, offset: int = 0, limit: int = 10,
                               start_time: Optional[datetime] = None, end_time: Optional[datetime] = None,
                               asset: Optional[Asset] = None,
                               height=None, detailed=False, after_tx_id='') -> TxPage:
        if asset:
            raise Exception(f'asset parameter is not supported')
        if start_time or end_time:
            raise Exception(f'start_time and end_time parameters are not supported')

        results = await self._call_service(self.service.gettransactions, address, after_tx_id, limit + offset)
        results = results[offset:]

        return TxPage(
            -1,
            [self._convert_lib_tx_to_our_tx(tx) for tx in results]
        )

    async def get_transaction_data(self, tx_id: str) -> Optional[XcTx]:
        result = await self._call_service(self.service.gettransaction, tx_id)
        return self._convert_lib_tx_to_our_tx(result)

    async def transfer(self, what: CryptoAmount, recipient: str, memo: Optional[str] = None,
                       fee_rate: Optional[int] = None, is_sync: bool = True, **kwargs) -> str:

        inputs = []

        # todo!

        # r = [
        #     {'address': 'blt1q74y0083lzwmhsdf336hl5ptwxlqqwthdsdws84',
        #      'txid': 'fe2acca01e507c4815984418ab6a5ab703b31a49daff6b3db17ea2f91a3de61c', 'confirmations': 10,
        #      'output_n': 0, 'index': 0, 'value': 100000000, 'script': ''},
        #     {'address': 'blt1q74y0083lzwmhsdf336hl5ptwxlqqwthdsdws84',
        #      'txid': '01ff110796c32a4ff9c7c3895a1809172630f5629e6b49e606ad483f0afd1c67', 'confirmations': 10,
        #      'output_n': 0, 'index': 0, 'value': 100000000, 'script': ''}
        # ]


        outputs = []

        if memo:
            outputs.append(self.make_output_with_memo(recipient, memo))

        t = Transaction(inputs, outputs)
        t.sign(self.get_private_key())
        tx_hex = t.raw_hex()
        return await self.broadcast_tx(tx_hex)

    @staticmethod
    def make_output_with_memo(recipient: str, memo: str):
        return Output(0, recipient, lock_script=compile_memo(memo))

    async def broadcast_tx(self, tx_hex: str) -> str:
        results = await self._call_service(self.service.sendrawtransaction, tx_hex)
        self.last_broadcast_response = results
        return results['txid']

    async def get_fees(self, average_blocks=10, fast_blocks=3, fastest_blocks=1) -> Fees:
        average, fast, fastest = await asyncio.gather(
            self._call_service(self.service.estimatefee, average_blocks),
            self._call_service(self.service.estimatefee, fast_blocks),
            self._call_service(self.service.estimatefee, fastest_blocks),
        )

        return Fees(
            type=FeeType.PER_BYTE,
            fees={
                FeeOption.AVERAGE: self.gas_amount(average).amount,
                FeeOption.FAST: self.gas_amount(fast).amount,
                FeeOption.FASTEST: self.gas_amount(fastest).amount,
            }
        )

    def get_address(self) -> str:
        return self.get_public_key().address(encoding='bech32')

    def get_public_key(self) -> Key:
        return self.get_private_key().public()

    def get_private_key(self) -> Key:
        pk = super().get_private_key()
        lib_pk = Key(pk, network=self._service_network, is_private=True)
        return lib_pk

    def __init__(self,
                 network=NetworkType.MAINNET,
                 phrase: Optional[str] = None,
                 private_key: Union[str, bytes, callable, None] = None,
                 fee_bound: Optional[FeeBounds] = None,
                 root_derivation_paths: Optional[RootDerivationPaths] = ROOT_DERIVATION_PATHS,
                 explorer_providers=BLOCKSTREAM_EXPLORERS,
                 wallet_index=0,
                 # provider: Optional[UtxoOnlineDataProvider] = None,
                 provider_names=None):
        """
        BitcoinClient constructor
        Uses bitcoinlib under the hood
        :param provider_names: a list of Blockchain info provider names of bitcoinlib.
        See https://github.com/1200wd/bitcoinlib/blob/master/bitcoinlib/data/providers.json
        :type provider_names: list[str]
        :param network: Network type
        :param phrase: your secret phrase
        :param private_key: or your private key
        :param fee_bound: fee bounds
        :param root_derivation_paths: HD wallet derivation paths
        :param wallet_index: int index of wallet
        # :param provider: UTXO online data provider (see xchainpy/xchainpy-utxo-providers)
        :param explorer_providers: explorer providers dictionary
        """
        super().__init__(
            Chain.Bitcoin,
            network, phrase,
            private_key, fee_bound,
            root_derivation_paths,
            wallet_index
        )

        self.explorers = explorer_providers

        self._prefix = get_btc_address_prefix(network)
        self._decimal = BTC_DECIMAL
        self.native_asset = AssetBTC

        # self.provider = provider

        if provider_names is None:
            provider_names = [self.DEFAULT_PROVIDER_NAME]
        elif isinstance(provider_names, str):
            provider_names = [provider_names]

        if network in (NetworkType.MAINNET, NetworkType.STAGENET):
            self._service_network = 'bitcoin'
        elif network == NetworkType.DEVNET:
            self._service_network = 'bitcoinlib_test'
        else:
            self._service_network = 'testnet'

        self.service = Service(
            network=self._service_network,
            providers=provider_names
        )

    def validate_address(self, address: str) -> bool:
        try:
            deserialize_address(address)
        except Exception:
            return False

    async def get_utxos(self, address='', limit=MAX_TRANSACTIONS):
        address = address or self.get_address()
        results = await self._call_service(self.service.getutxos, address, '', limit)

        return results

    def _convert_lib_tx_to_our_tx(self, tx: Transaction) -> XcTx:
        transfers = []

        for inp in tx.inputs:
            if inp.script_type == 'coinbase':
                continue
            transfers.append(TokenTransfer(
                from_address=inp.address,
                to_address='',
                amount=self.gas_amount(inp.value).amount,
                asset=self.native_asset,
                tx_hash=tx.txid,
                outbound=False,
            ))

        memo = ''
        for output in tx.outputs:
            if not memo:
                memo = try_get_memo_from_output(output) or ''

            if output.script_type == 'nulldata':
                continue

            transfers.append(TokenTransfer(
                from_address='',
                to_address=output.address,
                amount=self.gas_amount(output.value).amount,
                asset=self.native_asset,
                tx_hash=tx.txid,
                outbound=True,
            ))

        return XcTx(
            self._gas_asset,
            transfers=transfers,
            date=tx.date,
            type=TxType.TRANSFER,
            hash=tx.txid,
            height=tx.block_height,
            memo=memo,
            is_success=(tx.status == 'confirmed'),
            original=tx,
        )

    @staticmethod
    async def _call_service(method, *args):
        return await asyncio.get_event_loop().run_in_executor(
            None,
            method,
            *args
        )
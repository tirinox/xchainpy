import asyncio
from datetime import datetime
from typing import Optional, Union, List

from bitcoinlib.config.config import MAX_TRANSACTIONS
from bitcoinlib.encoding import EncodingError
from bitcoinlib.keys import Key, deserialize_address
from bitcoinlib.services.services import Service
from bitcoinlib.transactions import Transaction

from xchainpy2_client import Fees, XChainClient, XcTx, TxPage, TxType, TokenTransfer, FeeType, \
    FeeOption, UTXO, Witness
from xchainpy2_client import RootDerivationPaths, FeeBounds
from xchainpy2_utils import Chain, NetworkType, CryptoAmount, Asset, AssetBTC
from .const import BTC_DECIMAL, BLOCKSTREAM_EXPLORERS, ROOT_DERIVATION_PATHS, MAX_MEMO_LENGTH, \
    DEFAULT_PROVIDER_NAMES, AssetTestBTC
from .tx_prepare import UTXOPrepare, try_get_memo_from_output
from .utils import get_btc_address_prefix, UTXOException


class BitcoinClient(XChainClient):
    async def get_balance(self, address: str = '') -> List[CryptoAmount]:
        address = address or self.get_address()
        result = await self._call_service(self.service.getbalance, address)
        return [self.gas_base_amount(result)]

    async def get_transactions(self, address: str, offset: int = 0, limit: int = 10,
                               start_time: Optional[datetime] = None, end_time: Optional[datetime] = None,
                               asset: Optional[Asset] = None,
                               height=None, detailed=False, after_tx_id='') -> TxPage:
        if asset:
            raise UTXOException(f'asset parameter is not supported')
        if start_time or end_time:
            raise UTXOException(f'start_time and end_time parameters are not supported')

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
                       fee_rate: Optional[int] = None, is_sync: bool = True, min_confirmations=1, **kwargs) -> str:
        if what.asset != self._gas_asset:
            raise UTXOException(f'Asset {what.asset} is not supported')

        if (memo_len := len(memo)) > MAX_MEMO_LENGTH:
            raise UTXOException(f'Memo is too long ({memo_len} of {MAX_MEMO_LENGTH} max)')

        if not self.validate_address(recipient):
            raise UTXOException('Invalid recipient address.')

        sender = self.get_address()

        utxos = await self.get_utxos(sender)

        utxo_prepare = UTXOPrepare(utxos, self._service_network,
                                   fee_per_byte=fee_rate,
                                   min_confirmations=min_confirmations)

        tx = utxo_prepare.build(sender, recipient, what.amount, memo)

        tx.estimate_size()
        tx.fee_per_kb = fee_rate * 1000
        tx.calc_weight_units()
        tx.calculate_fee()

        tx.sign(self.get_private_key())
        tx_hex = tx.raw_hex()

        if not tx.verify():
            raise UTXOException('Transaction verification failed')

        if kwargs.get('dry_run'):
            print('---hex---')
            print(tx_hex)
            print('---dict---')
            print(tx.as_dict())
            print('---size---')
            print(f'{tx.size = } bytes, {tx.vsize = } bytes')

            return tx.txid

        result = await self.broadcast_tx(tx_hex)

        txid = tx.txid
        self._save_last_response(txid, result)

        return result

    async def broadcast_tx(self, tx_hex: str) -> str:
        results = await self._call_service(self.service.sendrawtransaction, tx_hex)
        tx_id = results.get('txid')
        self._save_last_response(tx_id, results)
        return tx_id

    async def get_fees(self, average_blocks=10, fast_blocks=3, fastest_blocks=1) -> Fees:
        average, fast, fastest = await asyncio.gather(
            self._call_service(self.service.estimatefee, average_blocks),
            self._call_service(self.service.estimatefee, fast_blocks),
            self._call_service(self.service.estimatefee, fastest_blocks),
        )

        return Fees(
            type=FeeType.PER_BYTE,
            fees={
                FeeOption.AVERAGE: self.gas_base_amount(average).amount,
                FeeOption.FAST: self.gas_base_amount(fast).amount,
                FeeOption.FASTEST: self.gas_base_amount(fastest).amount,
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

        self._gas_asset = AssetBTC

        self.explorers = explorer_providers

        self._prefix = get_btc_address_prefix(network)
        self._decimal = BTC_DECIMAL

        if provider_names is None:
            provider_names = DEFAULT_PROVIDER_NAMES
        elif isinstance(provider_names, str):
            provider_names = [provider_names]

        if network in (NetworkType.MAINNET, NetworkType.STAGENET):
            self._service_network = 'bitcoin'
            self._gas_asset = AssetBTC
        elif network == NetworkType.DEVNET:
            self._service_network = 'bitcoinlib_test'
            self._gas_asset = AssetBTC
        else:
            self._service_network = 'testnet'
            self._gas_asset = AssetTestBTC

        self.service = Service(
            network=self._service_network,
            providers=provider_names,
            min_providers=2,  # to prevent invalid cache operation when it is <=1
        )

    def validate_address(self, address: str) -> bool:
        try:
            deserialize_address(address)
            return True
        except (EncodingError, TypeError):
            return False

    async def get_utxos(self, address='', limit=MAX_TRANSACTIONS, full=False) -> List[UTXO]:
        address = address or self.get_address()
        results = await self._call_service(self.service.getutxos, address, '', limit)

        if full:
            transactions = await asyncio.gather(
                *[self._call_service(self.service.gettransaction, utxo['txid']) for utxo in results]
            )
            transactions = {t.txid: t for t in transactions}
        else:
            transactions = {}

        for utxo in results:
            full_tx = transactions.get(utxo['txid'])
            if full_tx:
                the_input = full_tx.outputs[utxo['input_n']]
                utxo['script'] = the_input.script

        return [
            UTXO(
                hash=utxo['txid'],
                index=utxo['output_n'],
                value=utxo['value'],
                witness_utxo=Witness(0, utxo['script']),
                confirmations=utxo['confirmations'],
            ) for utxo in results
        ]

    def _convert_lib_tx_to_our_tx(self, tx: Transaction) -> XcTx:
        transfers = []

        for inp in tx.inputs:
            if inp.script_type == 'coinbase':
                continue
            transfers.append(TokenTransfer(
                from_address=inp.address,
                to_address='',
                amount=self.gas_base_amount(inp.value).amount,
                asset=self._gas_asset,
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
                amount=self.gas_base_amount(output.value).amount,
                asset=self._gas_asset,
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

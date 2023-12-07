import asyncio
from datetime import datetime
from typing import Optional, Union, List

from bitcoinlib.keys import Key, deserialize_address
from bitcoinlib.services.services import Service
from bitcoinlib.transactions import Transaction

from xchainpy2_client import Fees, XChainClient, XcTx, TxPage, UtxoOnlineDataProvider, TxType, TokenTransfer
from xchainpy2_client import RootDerivationPaths, FeeBounds
from xchainpy2_utils import Chain, NetworkType, CryptoAmount, Asset, AssetBTC
from .const import BTC_DECIMAL, BLOCKSTREAM_EXPLORERS, ROOT_DERIVATION_PATHS
from .utils import get_btc_address_prefix, try_get_memo_from_output


class BitcoinClient(XChainClient):
    async def get_balance(self, address: str = '') -> List[CryptoAmount]:
        result = await asyncio.get_event_loop().run_in_executor(
            None,
            self.service.getbalance,
            self.get_address()
        )
        return [self.gas_amount(result)]

    async def get_transactions(self, address: str, offset: int = 0, limit: int = 10,
                               start_time: Optional[datetime] = None, end_time: Optional[datetime] = None,
                               asset: Optional[Asset] = None,
                               height=None, detailed=False) -> TxPage:
        ...

    async def get_transaction_data(self, tx_id: str) -> Optional[XcTx]:
        result = await asyncio.get_event_loop().run_in_executor(
            None,
            self.service.gettransaction,
            tx_id
        )
        return self._convert_lib_tx_to_our_tx(result)

    async def transfer(self, what: CryptoAmount, recipient: str, memo: Optional[str] = None,
                       fee_rate: Optional[int] = None, is_sync: bool = True, **kwargs) -> str:
        ...

    async def broadcast_tx(self, tx_hex: str, is_sync=True) -> str:
        ...

    async def get_fees(self) -> Fees:
        ...

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
                 provider: Optional[UtxoOnlineDataProvider] = None):
        """
        BitcoinClient constructor
        Uses bitcoinlib under the hood
        :param network: Network type
        :param phrase: your secret phrase
        :param private_key: or your private key
        :param fee_bound: fee bounds
        :param root_derivation_paths: HD wallet derivation paths
        :param wallet_index: int index of wallet
        :param provider: UTXO online data provider (see xchainpy/xchainpy-utxo-providers)
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

        self.provider = provider

        if network in (NetworkType.MAINNET, NetworkType.STAGENET):
            self._service_network = 'bitcoin'
        else:
            self._service_network = 'testnet'

        self.service = Service(
            network=self._service_network,
            providers=[
                'mempool'
            ]
        )

    def validate_address(self, address: str) -> bool:
        try:
            deserialize_address(address)
        except Exception:
            return False

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

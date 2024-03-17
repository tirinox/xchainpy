import asyncio
import hashlib
from datetime import datetime
from typing import Optional, Union, List

from bitcash import PrivateKeyTestnet, PrivateKey
from bitcash.cashaddress import Address
from bitcash.exceptions import InvalidAddress
from bitcash.network import NetworkAPI

from xchainpy2_client import FeeBounds, RootDerivationPaths, XChainClient, Fees, XcTx, TxPage, UTXO, TxType, \
    TokenTransfer
from xchainpy2_utils import NetworkType, Asset, AssetBCH, Chain, CryptoAmount, Amount
from .const import ROOT_DERIVATION_PATHS, BCH_DECIMAL, DEFAULT_PROVIDER_NAMES, DEFAULT_BCH_EXPLORERS, \
    BCH_DEFAULT_FEE_BOUNDS, AssetTestBCH, DEFAULT_BCH_FEES


class BitcoinCashClient(XChainClient):
    def __init__(self,
                 network=NetworkType.MAINNET,
                 phrase: Optional[str] = None,
                 private_key: Union[str, bytes, callable, None] = None,
                 fee_bound: Optional[FeeBounds] = BCH_DEFAULT_FEE_BOUNDS,
                 root_derivation_paths: Optional[RootDerivationPaths] = ROOT_DERIVATION_PATHS,
                 explorer_providers=DEFAULT_BCH_EXPLORERS,
                 wallet_index=0,
                 provider_names=DEFAULT_PROVIDER_NAMES,
                 concurrency=5):
        """
        BitcoinCashClient interface
        Constructor to create a new Do.

        :param network: The network type
        :param phrase: The seed phrase
        :param private_key: The private key
        :param fee_bound: The fee bound
        :param root_derivation_paths: The root derivation paths
        :param explorer_providers: The explorer providers
        :param wallet_index: The wallet index (default is 0)
        :param provider_names: The provider names
        :param concurrency: The concurrency for batch-processing transactions
        """

        super().__init__(
            network=network,
            phrase=phrase,
            private_key=private_key,
            fee_bound=fee_bound,
            root_derivation_paths=root_derivation_paths,
            wallet_index=wallet_index,
            chain=Chain.BitcoinCash,
        )

        self._prefix = "bitcoincash:"
        self._decimal = BCH_DECIMAL
        self.explorers = explorer_providers
        self._gas_asset = AssetBCH if network != NetworkType.TESTNET else AssetTestBCH

        if not provider_names:
            provider_names = DEFAULT_PROVIDER_NAMES
        self.provider_names = provider_names
        self.api = NetworkAPI()
        self._concurrency = concurrency
        self._semaphore = asyncio.Semaphore(concurrency)

    def validate_address(self, address: str) -> bool:
        try:
            Address.from_string(address)
            return True
        except InvalidAddress:
            return False

    def get_private_key_bitcash(self) -> Union[PrivateKey, PrivateKeyTestnet]:
        _class = PrivateKeyTestnet if self.network == NetworkType.TESTNET else PrivateKey
        return _class.from_hex(self.get_private_key())

    def get_public_key(self) -> bytes:
        return self.get_private_key_bitcash().public_key

    def get_address(self) -> str:
        return self.get_private_key_bitcash().address

    async def get_balance(self, address: str = '') -> List[CryptoAmount]:
        result = await self._call_service(self.api.get_balance, address or self.get_address())
        return [self.gas_base_amount(result)]

    async def get_transactions(self, address: str = '', offset: int = 0, limit: int = 10,
                               start_time: Optional[datetime] = None, end_time: Optional[datetime] = None,
                               asset: Optional[Asset] = None) -> TxPage:
        """
        Get transactions of the wallet
        :param address: The address (default is the address of the wallet)
        :param offset: The offset (ignored)
        :param limit: The limit (ignored)
        :param start_time: The start time (ignored)
        :param end_time: The end time (ignored)
        :param asset: The asset (ignored)
        :return: The transaction page
        """
        if not address:
            address = self.get_address()
        data = await self._call_service(self.api.get_transactions, address, self._underlying_network)
        hashes = data[offset:limit]

        transactions = await asyncio.gather(*[self.get_transaction_data(tx_id) for tx_id in hashes])
        return TxPage(
            total=len(data),
            txs=list(transactions),
        )

    async def get_transaction_data(self, tx_id: str) -> Optional[XcTx]:
        data = await self._call_service(self.api.get_transaction, tx_id, self._underlying_network)
        # todo: parse data to XcTx
        transfers = []
        for input in data.inputs:
            transfers.append(TokenTransfer(
                input.address,
                to_address='',
                amount=Amount.automatic(input.amount),
                asset=self.gas_asset,
                tx_hash=data.txid,
                outbound=False,
            ))

        for output in data.outputs:
            if output.amount:
                transfers.append(TokenTransfer(
                    output.address,
                    to_address='',
                    amount=Amount.automatic(output.amount),
                    asset=self.gas_asset,
                    tx_hash=data.txid,
                    outbound=True,
                ))

        # detect memo
        memo = ''
        for output in data.outputs:
            if output.op_return:
                # convert hex to string
                memo = bytes.fromhex(output.op_return).decode('utf-8')
                break

        return XcTx(
            transfers=transfers,
            asset=self.gas_asset,
            type=TxType.TRANSFER,
            hash=data.txid,
            date=None,
            height=data.block or 0,
            is_success=True,
            original=data,
            memo=memo,
        )

    @property
    def _underlying_network(self):
        return 'testnet' if self.network == NetworkType.TESTNET else 'mainnet'

    async def get_fees(self) -> Fees:
        """
        Get default fees
        No API call is performed.
        :return: The fee
        """
        return DEFAULT_BCH_FEES

    async def transfer(self, what: CryptoAmount, recipient: str, memo: Optional[str] = None,
                       fee_rate: Optional[int] = None, **kwargs) -> str:
        """
        Transfer the asset to the recipient address
        :param what: The amount to transfer
        :param recipient: The recipient address
        :param memo: The memo (optional)
        :param fee_rate: The fee rate (optional, but recommended)
        :param kwargs: The additional parameters
        :return: The transaction hash
        """
        if not fee_rate:
            fee_rates = await self.get_fees()
            fee_rate = fee_rates.fast

        return await self._call_service(self._transfer_sync, what, recipient, memo, fee_rate, kwargs)

    def _transfer_sync(self, what: CryptoAmount, recipient: str, memo: Optional[str] = None,
                       fee_rate: Optional[int] = None, kwargs=None) -> str:
        kwargs = kwargs or {}
        return self.get_private_key_bitcash().send(
            [(recipient, what.amount.internal_amount, 'satoshi')],
            fee=fee_rate,
            message=memo or None,
            **kwargs
        )

    async def get_utxos(self, address='') -> List[UTXO]:
        """
        Get UTXOs of the wallet
        UTxO is an unspent transaction output
        :param address: address (default is the address of the wallet)
        :return: list of UTXOs
        """
        address = address or self.get_address()
        raw_data = await self._call_service(self.api.get_unspent, address, self._underlying_network)
        # todo: parse raw_data to UTXO
        return raw_data

    async def broadcast_tx(self, tx_hex: str) -> str:
        """
        Broadcast pre-signed transaction to the network
        :param tx_hex: The transaction hex string
        :return: The transaction hash
        """
        await self._call_service(self.api.broadcast_tx, tx_hex, self._underlying_network)

        # todo: the method above does not return the tx hash!
        hash_object = hashlib.sha256(bytes.fromhex(tx_hex))
        tx_hash = hash_object.hexdigest()
        return tx_hash

    async def _call_service(self, method, *args):
        async with self._semaphore:
            return await asyncio.get_event_loop().run_in_executor(
                None,
                method,
                *args
            )

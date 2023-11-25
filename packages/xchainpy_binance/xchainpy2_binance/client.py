from datetime import datetime
from typing import Optional, Union, List

from bip_utils import Bech32ChecksumError

from xchainpy2_client import AssetInfo, Fees, FeeType, XChainClient, XcTx, TxPage, TokenTransfer, TxType
from xchainpy2_client import RootDerivationPaths, FeeBounds
from xchainpy2_client.fees import single_fee
from xchainpy2_crypto import decode_address
from xchainpy2_utils import Chain, NetworkType, CryptoAmount, AssetBNB, Asset, Amount, parse_iso_date
from .const import DEFAULT_CLIENT_URLS, DEFAULT_ROOT_DERIVATION_PATHS, FALLBACK_CLIENT_URLS, BNB_EXPLORERS, BNB_DECIMAL
from .sdk.environment import BinanceEnvironment
from .sdk.http_cli import AsyncHttpApiClient
from .utils import get_bnb_address_prefix


class BinanceChainClient(XChainClient):
    def get_explorer_url(self) -> str:
        return self.explorer.explorer_url

    def get_explorer_address_url(self, address: str) -> str:
        return self.explorer.get_explorer_address_url(address)

    def get_explorer_tx_url(self, tx_id: str) -> str:
        return self.explorer.get_explorer_tx_url(tx_id)

    def get_address(self) -> str:
        pass

    async def get_balance(self, address: str = '') -> List[CryptoAmount]:
        if not address:
            address = self.get_address()

        balances = await self._cli.get_account(address)
        return [
            CryptoAmount(Amount.from_asset(b['free'], self._decimal), self._make_asset(b['symbol']))
            for b in balances['balances']
        ]

    async def get_transactions(self, address: str, offset: int = 0, limit: int = 10,
                               start_time: Optional[datetime] = None, end_time: Optional[datetime] = None,
                               asset: Optional[Asset] = None,
                               height=None) -> TxPage:
        raw = await self._cli.get_transactions(
            address,
            offset=offset, limit=limit,
            start_time=(start_time.timestamp() if start_time else None),
            end_time=(end_time.timestamp() if end_time else None),
            symbol=asset.symbol if asset else None,
            height=height
        )
        return TxPage(
            total=raw['total'],
            txs=[self.parse_tx_data_simplified(tx, address) for tx in raw['tx']],
        )

    async def get_transaction_data(self, tx_id: str) -> Optional[XcTx]:
        raw = await self._cli.get_transaction(tx_id)
        return self.parse_tx_data(raw, self.get_address())

    async def transfer(self, what: CryptoAmount, recipient: str, memo: Optional[str] = None,
                       fee_rate: Optional[int] = None, **kwargs) -> str:
        pass

    async def broadcast_tx(self, tx_hex: str, is_sync=True) -> str:
        result = await self._cli.broadcast_hex_msg(tx_hex, sync=is_sync)
        return result['transaction']['hash']

    async def get_fees(self) -> Fees:
        fees = await self.load_fees()
        send_fee_rate = self._find_send_fee(fees)
        return single_fee(FeeType.FLAT_FEE, send_fee_rate)

    def __init__(self,
                 network=NetworkType.MAINNET,
                 phrase: Optional[str] = None,
                 private_key: Union[str, bytes, callable, None] = None,
                 fee_bound: Optional[FeeBounds] = None,
                 root_derivation_paths: Optional[RootDerivationPaths] = None,
                 client_urls=DEFAULT_CLIENT_URLS,
                 fallback_client_urls=FALLBACK_CLIENT_URLS,
                 explorer_providers=BNB_EXPLORERS,
                 wallet_index=0,
                 ):
        """
        Initialize THORChainClient.
        :param network: Network type. Default is `NetworkType.MAINNET`
        :param phrase: Mnemonic phrase
        :param private_key: Private key (if you want to use a private key instead of a mnemonic phrase)
        :param fee_bound: Fee bound structure. See: FeeBounds
        :param root_derivation_paths: Dictionary of derivation paths for each network type. See: ROOT_DERIVATION_PATHS
        :param client_urls: Dictionary of client urls for each network type. See: DEFAULT_CLIENT_URLS
        :param explorer_providers: Dictionary of explorer providers for each network type. See: THOR_EXPLORERS
        :param wallet_index: int (wallet index, default 0) We can derive any number of addresses from a single seed
        """
        self.explorer_providers = explorer_providers.copy() if explorer_providers else BNB_EXPLORERS.copy()

        if isinstance(client_urls, str):
            client_urls = {network: client_urls}

        self.client_urls = client_urls.copy() if client_urls else DEFAULT_CLIENT_URLS.copy()
        self.fallback_client_urls = fallback_client_urls.copy() if fallback_client_urls else None

        root_derivation_paths = root_derivation_paths.copy() \
            if root_derivation_paths else DEFAULT_ROOT_DERIVATION_PATHS.copy()

        super().__init__(
            Chain.Binance,
            network, phrase,
            private_key, fee_bound,
            root_derivation_paths,
            wallet_index
        )

        self._prefix = get_bnb_address_prefix(network)
        self.native_asset = AssetBNB
        self._denom = 'bnb'
        self._decimal = BNB_DECIMAL

        self.cache_fees = True
        self._cached_fees = None

        # todo: use clientUrls
        env = BinanceEnvironment.get_production_env() if network != NetworkType.TESTNET \
            else BinanceEnvironment.get_testnet_env()
        self._cli = AsyncHttpApiClient(env=env)

    @property
    def explorer(self):
        return self.explorer_providers[self.network]

    @property
    def client(self):
        return self._cli

    @property
    def server_url(self) -> str:
        return self.client_urls[self.network]

    def validate_address(self, address: str) -> bool:
        try:
            decode_address(address, self._prefix)
            return True
        except (ValueError, Bech32ChecksumError):
            return False

    def get_asset_info(self) -> AssetInfo:
        return AssetInfo(
            AssetBNB, BNB_DECIMAL
        )

    async def load_fees(self):
        if self._cached_fees:
            return self._cached_fees
        else:
            fees = await self._cli.get_fees()
            if self.cache_fees:
                self._cached_fees = fees
            return fees

    @staticmethod
    def _find_send_fee(fees) -> Optional[Amount]:
        for item in fees:
            fixed_fees = item.get('fixed_fee_params')
            if fixed_fees and fixed_fees['msg_type'] == 'send':
                fee = Amount.from_base(int(fixed_fees['fee']), BNB_DECIMAL)
                return fee

    def _make_asset(self, symbol: str) -> Asset:
        return Asset.from_string(f"{self.chain.value}.{symbol}")

    async def close_session(self):
        await self.client.session.close()

    def parse_tx_data(self, raw: dict, my_address: str = '') -> XcTx:
        """
        Parses only send transactions
        :param my_address: My address to detect if the transaction is outbound or not
        :param raw: Raw data dict loaded from JSON received from API
        :return: XcTx (parsed transaction)
        """
        tx_hash = raw['hash']
        transfers = []
        messages = raw['tx']['value']['msg']
        for message in messages:
            if message['type'] == 'cosmos-sdk/Send':
                inputs, outputs = message['value']['inputs'], message['value']['outputs']
                for input_part in inputs:
                    for output in outputs:
                        for input_coin in input_part['coins']:
                            for output_coin in output['coins']:
                                in_denom = input_coin['denom']
                                out_denom = output_coin['denom']
                                in_amount = int(input_coin['amount'])
                                out_amount = int(output_coin['amount'])
                                if in_denom != out_denom or in_amount != out_amount:
                                    continue
                                from_address = input_part['address']
                                transfers.append(
                                    TokenTransfer(
                                        from_address=from_address,
                                        to_address=output['address'],
                                        amount=Amount.automatic(in_amount, self._decimal),
                                        asset=self._make_asset(in_denom),
                                        tx_hash=tx_hash,
                                        outbound=(from_address == my_address)
                                    )
                                )

        asset = self.native_asset

        return XcTx(
            asset=asset,
            date=None,
            transfers=transfers,
            hash=tx_hash,
            height=int(raw['height']),
            is_success=raw['ok'],
            memo=raw['tx']['value'].get('memo', ''),
            type=TxType.TRANSFER if transfers else TxType.UNKNOWN
        )

    def parse_tx_data_simplified(self, raw: dict, my_address=None) -> XcTx:
        tx_date = parse_iso_date(raw['timeStamp'])
        tx_hash = raw['txHash']
        symbol = raw['txAsset']
        asset = self._make_asset(symbol)
        tx_type = raw['txType']
        return XcTx(
            hash=tx_hash,
            asset=asset,
            type=TxType.TRANSFER if tx_type == 'TRANSFER' else TxType.UNKNOWN,
            date=tx_date,
            height=raw['blockHeight'],
            is_success=(raw['code'] == 0),
            memo=raw['memo'],
            transfers=[
                TokenTransfer(
                    raw['fromAddr'],
                    raw['toAddr'],
                    amount=Amount.automatic(raw['value'], self._decimal),
                    asset=self._make_asset(raw['txAsset']),
                    tx_hash=tx_hash,
                    outbound=(raw['fromAddr'] == my_address),
                )
            ],
        )

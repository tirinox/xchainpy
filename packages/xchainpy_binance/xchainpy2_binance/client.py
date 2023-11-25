from datetime import datetime
from typing import Optional, Union, List

from bip_utils import Bech32ChecksumError

from xchainpy2_client import AssetInfo, Fees, FeeType, XChainClient, XcTx, TxPage
from xchainpy2_client import RootDerivationPaths, FeeBounds
from xchainpy2_client.fees import single_fee
from xchainpy2_crypto import decode_address
from xchainpy2_utils import Chain, NetworkType, CryptoAmount, AssetBNB, Asset, Amount
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

    async def get_transactions(self, address: str, offset: int = 0, limit: int = 0,
                               start_time: Optional[datetime] = None, end_time: Optional[datetime] = None,
                               asset: Optional[Asset] = None) -> TxPage:
        pass

    async def get_transaction_data(self, tx_id: str) -> Optional[XcTx]:
        pass

    async def transfer(self, what: CryptoAmount, recipient: str, memo: Optional[str] = None,
                       fee_rate: Optional[int] = None, **kwargs) -> str:
        pass

    async def broadcast_tx(self, tx_hex: str) -> str:
        pass

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

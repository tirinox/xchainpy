from typing import Optional, Union

from bip_utils import Bech32ChecksumError

from packages.xchainpy_client.xchainpy2_client import RootDerivationPaths, FeeBounds
from xchainpy2_client import AssetInfo
from xchainpy2_cosmos import CosmosGaiaClient
from xchainpy2_crypto import decode_address
from xchainpy2_utils import Chain, NetworkType, AssetRUNE, RUNE_DECIMAL, CryptoAmount, Amount
from .const import NodeURL, DEFAULT_CHAIN_IDS, DEFAULT_CLIENT_URLS, DENOM_RUNE_NATIVE, ROOT_DERIVATION_PATHS, \
    THOR_EXPLORERS, DEFAULT_GAS_LIMIT_VALUE, DEPOSIT_GAS_LIMIT_VALUE
from .utils import get_thor_address_prefix


class THORChainClient(CosmosGaiaClient):
    def __init__(self,
                 network=NetworkType.MAINNET,
                 phrase: Optional[str] = None,
                 fee_bound: Optional[FeeBounds] = None,
                 root_derivation_paths: Optional[RootDerivationPaths] = None,
                 client_urls=DEFAULT_CLIENT_URLS,
                 chain_ids=DEFAULT_CHAIN_IDS,
                 explorer_providers=THOR_EXPLORERS,
                 ):
        """
        Initialize THORChainClient.
        :param network: Network type. Default is `NetworkType.MAINNET`
        :param phrase: Mnenomic phrase
        :param fee_bound: Fee bound structure. See: FeeBounds
        :param root_derivation_paths: Dictionary of derivation paths for each network type. See: ROOT_DERIVATION_PATHS
        :param client_urls: Dictionary of client urls for each network type. See: DEFAULT_CLIENT_URLS
        :param chain_ids: Dictionary of chain ids for each network type. See: DEFAULT_CHAIN_IDS
        :param explorer_providers: Dictionary of explorer providers for each network type. See: THOR_EXPLORERS
        """
        root_derivation_paths = root_derivation_paths.copy() if root_derivation_paths else ROOT_DERIVATION_PATHS.copy()
        super().__init__(
            network, phrase, fee_bound, root_derivation_paths
        )

        # Tune for THORChain
        self.chain = Chain.THORChain
        self._prefix = get_thor_address_prefix(network)
        self.native_asset = AssetRUNE
        self._denom = DENOM_RUNE_NATIVE
        self._decimal = RUNE_DECIMAL
        self._gas_limit = DEFAULT_GAS_LIMIT_VALUE
        self._deposit_gas_limit = DEPOSIT_GAS_LIMIT_VALUE

        if isinstance(client_urls, NodeURL):
            client_urls = {network: client_urls}

        self.explorer_providers = explorer_providers.copy() if explorer_providers else THOR_EXPLORERS.copy()
        self.client_urls = client_urls.copy() if client_urls else DEFAULT_CLIENT_URLS.copy()
        self.chain_ids = chain_ids.copy() if chain_ids else DEFAULT_CHAIN_IDS.copy()

    @property
    def server_url(self):
        return self.client_urls[self.network].node

    def validate_address(self, address: str) -> bool:
        if super().validate_address(address):
            try:
                decode_address(address, self._prefix)
            except (ValueError, Bech32ChecksumError):
                return False
        return True

    def get_asset_info(self) -> AssetInfo:
        return AssetInfo(
            AssetRUNE, RUNE_DECIMAL
        )

    # todo: use fallback urls to fetch the transaction?

    # todo: getTransactionDataThornode
    # todo: getDepositTransaction (`${this.getClientUrl().node}/thorchain/tx/${txId}`))

    async def deposit(self,
                      what: Union[CryptoAmount, Amount, int, float],
                      memo: str,
                      gas_limit: Optional[int] = None,
                      sequence: int = None,
                      check_balance: bool = True,
                      wallet_index: int = 0) -> str:
        """
        Send deposit transaction
        :param what: Amount and Asset
        :param memo: Memo string (usually a command to the AMM)
        :param gas_limit: if not specified, we'll use the default value
        :param sequence: sequence number. If it is None, it will be fetched automatically
        :param check_balance: Flag to check the balance before sending Tx
        :param wallet_index: Wallet index, default 0
        :return:
        """
        if isinstance(what, Amount):
            what = CryptoAmount(what, self.native_asset)
        elif isinstance(what, (int, float)):
            what = CryptoAmount(Amount.automatic(what, self._decimal), self.native_asset)

        address = self.get_address(wallet_index)

        if check_balance:
            await self.check_balance(address, what)

        if gas_limit is None:
            gas_limit = self._deposit_gas_limit

        if sequence is None:
            account = await self.get_account(address)
            sequence = account.sequence



        return 'todo!'

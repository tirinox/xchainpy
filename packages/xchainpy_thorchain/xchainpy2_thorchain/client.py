import asyncio
from typing import Optional, Union

from bip_utils import Bech32ChecksumError
from cosmpy.aerial.tx_helpers import SubmittedTx

from packages.xchainpy_client.xchainpy2_client import RootDerivationPaths, FeeBounds
from xchainpy2_client import AssetInfo
from xchainpy2_cosmos import CosmosGaiaClient
from xchainpy2_crypto import decode_address
from xchainpy2_utils import Chain, NetworkType, AssetRUNE, RUNE_DECIMAL, CryptoAmount, Amount
from .const import NodeURL, DEFAULT_CHAIN_IDS, DEFAULT_CLIENT_URLS, DENOM_RUNE_NATIVE, ROOT_DERIVATION_PATHS, \
    THOR_EXPLORERS, DEFAULT_GAS_LIMIT_VALUE, DEPOSIT_GAS_LIMIT_VALUE, FALLBACK_CLIENT_URLS
from .utils import get_thor_address_prefix, build_deposit_tx_unsigned


class THORChainClient(CosmosGaiaClient):
    def __init__(self,
                 network=NetworkType.MAINNET,
                 phrase: Optional[str] = None,
                 fee_bound: Optional[FeeBounds] = None,
                 root_derivation_paths: Optional[RootDerivationPaths] = None,
                 client_urls=DEFAULT_CLIENT_URLS,
                 fallback_client_urls=FALLBACK_CLIENT_URLS,
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
        self.explorer_providers = explorer_providers.copy() if explorer_providers else THOR_EXPLORERS.copy()

        if isinstance(client_urls, NodeURL):
            client_urls = {network: client_urls}

        self.client_urls = client_urls.copy() if client_urls else DEFAULT_CLIENT_URLS.copy()
        self.fallback_client_urls = fallback_client_urls.copy() if fallback_client_urls else None

        self.chain_ids = chain_ids.copy() if chain_ids else DEFAULT_CHAIN_IDS.copy()

        root_derivation_paths = root_derivation_paths.copy() if root_derivation_paths else ROOT_DERIVATION_PATHS.copy()
        super().__init__(
            network, phrase, fee_bound, root_derivation_paths,
            self.client_urls, self.chain_ids, self.explorer_providers
        )

        # Tune for THORChain
        self.chain = Chain.THORChain
        self._prefix = get_thor_address_prefix(network)
        self.native_asset = AssetRUNE
        self._denom = DENOM_RUNE_NATIVE
        self._decimal = RUNE_DECIMAL
        self._gas_limit = DEFAULT_GAS_LIMIT_VALUE
        self._deposit_gas_limit = DEPOSIT_GAS_LIMIT_VALUE

        self._recreate_client()

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

    async def deposit(self,
                      what: Union[CryptoAmount, Amount, int, float],
                      memo: str,
                      second_asset: Optional[CryptoAmount] = None,
                      gas_limit: Optional[int] = None,
                      sequence: int = None,
                      account_number: int = None,
                      check_balance: bool = True,
                      fee=None,
                      wallet_index: int = 0,
                      return_full_response=False) -> Union[SubmittedTx, str]:
        """
        Send deposit transaction
        :param what: Amount and Asset
        :param second_asset: optional second asset if needed
        :param memo: Memo string (usually a command to the AMM)
        :param gas_limit: if not specified, we'll use the default value
        :param sequence: sequence number. If it is None, it will be fetched automatically
        :param check_balance: Flag to check the balance before sending Tx
        :param wallet_index: Wallet index, default is 0
        :param fee: string like "0rune", default is 0
        :param account_number: Your account number. If it is none, we will fetch it
        :param return_full_response: when it is not enough to have just tx hash

        :return: submitted tx hash or full response (SubmittedTt object) if requested
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

        if sequence is None or account_number is None:
            account = await self.get_account(address)
            sequence = account.sequence
            account_number = account.number

        public_key = self.get_public_key(wallet_index)

        tx = build_deposit_tx_unsigned(
            what, memo,
            public_key,
            fee=fee or self.get_amount_string(0),
            prefix=self.prefix,
            sequence_num=sequence,
            gas_limit=gas_limit,
            second_asset=second_asset,
        )

        tx.sign(
            self.get_private_key_cosmos(wallet_index),
            self.get_chain_id(),
            account_number=account_number
        )

        tx.complete()

        result = await asyncio.get_event_loop().run_in_executor(
            None,
            self._client.broadcast_tx,
            tx
        )

        return result if return_full_response else result.tx_hash

    async def fetch_transaction_from_thornode(self, tx_hash: str) -> dict:
        """
        Fetch transaction from THORNode, try to use fallback client if main client is not available
        :param tx_hash:
        :return:
        """
        clients = [self.client_urls[self.network]]
        if self.fallback_client_urls:
            clients.append(self.fallback_client_urls[self.network])

        e = None
        for client in clients:
            try:
                url = self.url_to_fetch_tx_data(tx_hash, server_url=client.node)
                j = await self._get_json(url)
                return j
            except Exception as e:
                continue
        if e:
            raise e

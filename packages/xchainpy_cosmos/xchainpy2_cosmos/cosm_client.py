import asyncio
import logging
from datetime import datetime
from math import ceil
from operator import itemgetter
from typing import Optional, List, Union
from urllib.parse import urlencode

from aiohttp import ClientSession
from cosmpy.aerial.client import LedgerClient, Account, create_bank_send_msg, prepare_and_broadcast_basic_transaction, \
    Coin
from cosmpy.aerial.config import NetworkConfig
from cosmpy.aerial.tx import Transaction
from cosmpy.aerial.wallet import LocalWallet
from cosmpy.crypto.address import Address
from cosmpy.crypto.keypairs import PrivateKey, PublicKey
from cosmpy.protos.cosmos.tx.v1beta1.service_pb2 import BroadcastTxRequest, BroadcastMode

from xchainpy2_client import XChainClient, RootDerivationPaths, FeeBounds, XcTx, \
    Fees, TxPage, FeeType, FeeOption
from xchainpy2_client.fees import single_fee
from xchainpy2_crypto import derive_private_key, create_address
from xchainpy2_utils import Chain, NetworkType, CryptoAmount, Asset, Amount, AssetATOM, \
    unique_by_key, batched, NINE_REALMS_CLIENT_HEADER, XCHAINPY_IDENTIFIER, flatten
from .const import DEFAULT_CLIENT_URLS, DEFAULT_EXPLORER_PROVIDER, COSMOS_ROOT_DERIVATION_PATHS, COSMOS_ADDR_PREFIX, \
    COSMOS_CHAIN_IDS, COSMOS_DECIMAL, TxFilterFunc, MAX_PAGES_PER_FUNCTION_CALL, MAX_TX_COUNT_PER_PAGE, \
    MAX_TX_COUNT_PER_FUNCTION_CALL, COSMOS_DENOM, DEFAULT_FEE, DEFAULT_GAS_LIMIT, DEFAULT_REST_USER_AGENT, \
    FEE_MINIMUM_GAS_PRICE
from .models import TxHistoryResponse, TxLoadException
from .utils import parse_tx_response_json

logger = logging.getLogger(__name__)


class CosmosGaiaClient(XChainClient):
    def __init__(self,
                 network=NetworkType.MAINNET,
                 phrase: Optional[str] = None,
                 private_key: Union[str, bytes, callable, None] = None,
                 fee_bound: Optional[FeeBounds] = None,
                 root_derivation_paths: Optional[RootDerivationPaths] = None,
                 client_urls=DEFAULT_CLIENT_URLS,
                 chain_ids=COSMOS_CHAIN_IDS,
                 explorer_providers=DEFAULT_EXPLORER_PROVIDER,
                 wallet_index=0,
                 ):
        """
        Initialize CosmosClient
        :param network: Network type. Default is `NetworkType.MAINNET`
        :param phrase: Mnemonic phrase
        :param private_key: Private key (if you want to use a private key instead of a mnemonic phrase)
        :param fee_bound: Fee bound structure. See: FeeBounds
        :param root_derivation_paths: Dictionary of derivation paths for each network type. See: ROOT_DERIVATION_PATHS
        :param client_urls: Dictionary of client urls for each network type.
        :param chain_ids: Dictionary of chain ids for each network type.
        :param explorer_providers: Dictionary of explorer providers for each network type.
        :param wallet_index: int (default 0)
        """
        root_derivation_paths = root_derivation_paths.copy() \
            if root_derivation_paths else COSMOS_ROOT_DERIVATION_PATHS.copy()
        super().__init__(Chain.Cosmos, network, phrase, private_key, fee_bound, root_derivation_paths, wallet_index)

        self.explorers = explorer_providers

        if isinstance(client_urls, str):
            client_urls = {NetworkType.MAINNET: client_urls}

        self._client_urls = client_urls.copy() if client_urls else DEFAULT_CLIENT_URLS.copy()
        self.chain_ids = chain_ids.copy() if chain_ids else COSMOS_CHAIN_IDS.copy()

        self._gas_asset = AssetATOM
        self._prefix = COSMOS_ADDR_PREFIX

        self._denom = COSMOS_DENOM
        self._decimal = COSMOS_DECIMAL
        self._gas_limit = DEFAULT_GAS_LIMIT

        self._fee_minimum_gas_price = FEE_MINIMUM_GAS_PRICE

        self._client: Optional[LedgerClient] = None
        self._recreate_client()

        self._wallet: Optional[LocalWallet] = None
        self._make_wallet()

        self.cache = None
        self.tx_responses = {}

        self.standard_tx_fee = DEFAULT_FEE

        self.cache_fee_period = 600  # sec = 10 min

    @property
    def get_client_urls(self):
        return self._client_urls

    def get_client(self) -> LedgerClient:
        """
        Please use this getter to obtain LedgerClient for specific Cosmos calls like delegation, staking etc.
        Underlying library is cosmpy (https://github.com/fetchai/cosmpy)
        :return: LedgerClient
        """
        if not self._client:
            self._recreate_client()
        return self._client

    @property
    def server_url(self):
        return self._client_urls[self.network]

    @property
    def rpc_url(self):
        return self.server_url

    @property
    def rest_session(self) -> ClientSession:
        # noinspection PyProtectedMember
        return self._client.auth._rest_api._session

    def patch_client(self, user_agent=DEFAULT_REST_USER_AGENT, identifier9r=XCHAINPY_IDENTIFIER):
        headers = self.rest_session.headers
        headers['User-Agent'] = user_agent
        headers[NINE_REALMS_CLIENT_HEADER] = identifier9r

    def _recreate_client(self):
        # Guard for preventing early client creation before all necessary fields are set.
        if not hasattr(self, '_denom'):
            return

        rest_url = f'rest+{self.server_url}'
        self._client = LedgerClient(NetworkConfig(
            chain_id=self.chain_ids[self.network],
            url=rest_url,
            fee_denomination=self._denom,
            staking_denomination=self._denom,
            fee_minimum_gas_price=self._fee_minimum_gas_price,
        ))

    def set_chain_id(self, chain_id: str):
        """
        Set/update the current chain id.
        :param chain_id:
        :return: None
        """
        # dirty check to avoid using and re-creation of same data
        if chain_id == self.chain_ids[self.network]:
            return
        self.chain_ids[self.network] = chain_id
        self._recreate_client()

    def get_chain_id(self):
        return self.chain_ids[self.network]

    def set_network(self, network: NetworkType):
        """
        Set/update the current network.
        :param network:
        :return: None
        """
        # dirty check to avoid using and re-creation of same data
        if network == self.network:
            return
        super().set_network(network)
        self._recreate_client()
        self._make_wallet()

    def get_network(self):
        return self.network

    def purge_client(self):
        super().purge_client()

    def set_phrase(self, phrase: str, wallet_index: int = 0):
        super().set_phrase(phrase, wallet_index)
        self._make_wallet()

    def validate_address(self, address: str) -> bool:
        """
        Validates a Cosmos address.
        :param address: Address string
        :return: True if valid, False otherwise.
        """

        if not address:
            return False

        address = str(address).lower()

        if not address.startswith(self._prefix):
            return False

        try:
            Address(address)
            return True
        except Exception:
            return False

    def get_address(self) -> str:
        """
        Get the address for the given wallet index.
        :return: string address
        """
        pub_key = self.get_public_key().public_key_bytes
        return create_address(pub_key, self._prefix)

    def get_private_key(self) -> str:
        """
        Get the private key for the given wallet index.
        :return:
        """
        if self.pk_hex:
            return self.pk_hex
        else:
            return derive_private_key(
                self.phrase,
                self.get_full_derivation_path(self.wallet_index)
            ).hex()

    def get_public_key(self) -> PublicKey:
        return self.get_private_key_cosmos().public_key

    def get_private_key_cosmos(self) -> PrivateKey:
        pk = self.get_private_key()
        return PrivateKey(bytes.fromhex(pk))

    async def get_balance(self, address: str = '') -> List[CryptoAmount]:
        """
        Get the balance of a given address.
        :param address: By default, it will return the balance of the current wallet. (optional)
        :return:
        """
        if not address:
            address = self.get_address()

        address = Address(address, prefix=self.prefix)

        balances = await asyncio.get_event_loop().run_in_executor(
            None,
            self._client.query_bank_all_balances,
            address
        )

        our_balances = [self.convert_coin_to_amount(balance) for balance in balances]

        return our_balances

    def convert_coin_to_amount(self, c: Coin):
        asset = self.parse_denom_to_asset(c.denom)
        return CryptoAmount(
            Amount.from_base(c.amount, self._decimal),
            asset
        )

    def parse_denom_to_asset(self, denom: str) -> Asset:
        if denom == self._denom:
            return self._gas_asset
        else:
            return Asset(self.chain.value, denom.upper())

    async def get_account(self, address: str = None) -> Optional[Account]:
        """
        Get the account information for the given address: number and sequence.
        It there is no account, it will return None.
        It will throw an exception for special addresses (like Reserve)
        :param address: By default, it will return the account of the current wallet. (optional)
        :return:
        """
        if address is None:
            address = self.get_address()

        address = Address(address)

        try:
            account = await asyncio.get_event_loop().run_in_executor(
                None,
                self._client.query_account,
                address
            )
            return account
        except RuntimeError as e:
            if 'NotFound' in str(e):
                return
            raise e

    async def get_transactions(self, address: str = '',
                               offset: int = 0,
                               limit: int = 10,
                               start_time: Optional[datetime] = None,
                               end_time: Optional[datetime] = None,
                               asset: Optional[Asset] = None,
                               filter_function: TxFilterFunc = None,
                               batch_size=10,
                               batch_delay_sec=2) -> TxPage:

        address = address or self.get_address()

        message_action = None

        address = address if address else self.get_address()
        tx_min_height = None
        tx_max_height = None

        if limit + offset > MAX_PAGES_PER_FUNCTION_CALL * MAX_TX_COUNT_PER_PAGE:
            raise ValueError(
                f"limit plus offset can not be grater than {MAX_PAGES_PER_FUNCTION_CALL * MAX_TX_COUNT_PER_PAGE}")

        if limit > MAX_TX_COUNT_PER_FUNCTION_CALL:
            raise ValueError(f"Maximum number of transaction per call is {MAX_TX_COUNT_PER_FUNCTION_CALL}")

        pages_number = int(ceil((limit + offset) / MAX_TX_COUNT_PER_PAGE))

        all_tx_incoming_history = []
        all_tx_outgoing_history = []

        for page in range(1, pages_number + 1):
            call = self.search_tx_from_rpc(
                message_action=message_action,
                transfer_recipient=address,
                page=page,
                limit=limit,
                tx_max_height=tx_max_height,
                tx_min_height=tx_min_height,
                rpc_endpoint=self.rpc_url,
            )
            all_tx_incoming_history.append(call)

            call = self.search_tx_from_rpc(
                message_action=message_action,
                transfer_sender=address,
                page=page,
                limit=limit,
                tx_max_height=tx_max_height,
                tx_min_height=tx_min_height,
                rpc_endpoint=self.rpc_url,
            )
            all_tx_outgoing_history.append(call)

        # todo: add semaphore to limit the number of concurrent requests
        incoming_results = await asyncio.gather(*all_tx_incoming_history)
        outgoing_results = await asyncio.gather(*all_tx_outgoing_history)

        total_count = 0
        if incoming_results:
            total_count += int(incoming_results[0]['result']['total_count'])

        if outgoing_results:
            total_count += int(outgoing_results[0]['result']['total_count'])

        results = [results['result']['txs'] for results in incoming_results + outgoing_results]
        results = flatten(results)

        results = unique_by_key(results, itemgetter('hash'))

        results.sort(key=lambda x: int(x['height']), reverse=True)

        if filter_function:
            results = filter(filter_function, results)

        all_txs = []
        for batch in batched(results, batch_size):
            txs = await asyncio.gather(*[self.get_transaction_data(tx['hash']) for tx in batch])
            all_txs.extend(txs)
            await asyncio.sleep(batch_delay_sec)

        return TxPage(
            txs=all_txs,
            total=total_count,
        )

    async def search_tx(self, message_action=None, message_sender=None, offset=0, limit=50):
        if not message_action and not message_sender:
            raise ValueError('One of message_action or message_sender must be specified')

        events_param = []
        if message_action is not None:
            events_param.append(f"message.action='{message_action}'")
        if message_sender is not None:
            events_param.append(f"message.sender='{message_sender}'")

        query_parameter = {'events': ','.join(events_param)}

        if offset is not None:
            query_parameter['pagination.offset'] = offset
        if limit is not None:
            query_parameter['pagination.limit'] = limit

        url = f"{self.server_url}/cosmos/tx/v1beta1/txs?{urlencode(query_parameter)}"
        j = await self._get_json(url)
        return TxHistoryResponse.from_rpc_json(j)

    async def search_tx_from_rpc(
            self,
            message_action=None,
            message_sender=None,
            transfer_sender=None,
            transfer_recipient=None,
            page=None,
            limit=None,
            tx_min_height=None,
            tx_max_height=None,
            rpc_endpoint=None
    ):
        query_parameter = []
        if message_action is not None:
            query_parameter.append(f"message.action='{message_action}'")
        if message_sender is not None:
            query_parameter.append(f"message.sender='{message_sender}'")
        if transfer_sender is not None:
            query_parameter.append(f"transfer.sender='{transfer_sender}'")
        if transfer_recipient is not None:
            query_parameter.append(f"transfer.recipient='{transfer_recipient}'")
        if tx_min_height is not None:
            query_parameter.append(f"tx.height>='{tx_min_height}'")
        if tx_max_height is not None:
            query_parameter.append(f"tx.height<='{tx_max_height}'")

        search_parameters = {}
        if query_parameter:
            query = ' AND '.join(query_parameter)
            search_parameters['query'] = f'"{query}"'

        if page is not None:
            search_parameters['page'] = page
        if limit is not None:
            search_parameters['per_page'] = limit
        search_parameters['order_by'] = '"desc"'

        params_joined = '&'.join(f'{k}={v}' for k, v in search_parameters.items())

        url = f"{rpc_endpoint}/tx_search?{params_joined}"

        return await self._get_json(url)

    def url_to_fetch_tx_data(self, tx_id, server_url=None):
        server_url = server_url or self.server_url
        return f"{server_url}/cosmos/tx/v1beta1/txs/{tx_id}"

    async def get_transaction_data_cosmos(self, tx_id: str) -> dict:
        """
        Get the transaction data for the given transaction id.
        :param tx_id:
        :return: raw dict object
        """
        url = self.url_to_fetch_tx_data(tx_id)
        return await self._get_json(url)

    async def get_transaction_data(self, tx_id: str, our_address: str = '') -> Optional[XcTx]:
        """
        Get the transaction data for the given transaction id.
        :param tx_id:
        :return:
        """
        j = await self.get_transaction_data_cosmos(tx_id)

        return parse_tx_response_json(
            j, tx_id, our_address, self._decimal, self._denom, self._gas_asset
        )

    async def get_transaction_data_raw(self, tx_id: str) -> dict:
        url = self.url_to_fetch_tx_data(tx_id)
        return await self._get_json(url)

    async def get_fees(self) -> Fees:
        return single_fee(FeeType.FLAT_FEE, self.standard_tx_fee)

    async def transfer(self, what: CryptoAmount,
                       recipient: str,
                       memo: Optional[str] = None,
                       fee_rate: Optional[int] = None,
                       check_balance: bool = True) -> str:
        """
        Transfer coins.
        :param check_balance: Check balance before transfer. Default is True.
        :param what: CryptoAmount (amount and asset to transfer)
        :param recipient: str recipient address
        :param memo: str
        :param fee_rate: int
        :return: str tx hash
        """
        self._throw_if_empty_phrase()

        if check_balance:
            await self.check_balance(str(self._wallet.address()), what)

        tx = self.build_transfer_tx(what, recipient)

        response = await asyncio.get_event_loop().run_in_executor(
            None,
            prepare_and_broadcast_basic_transaction,
            self._client,
            tx,
            self._wallet,
            None,  # account
            self._gas_limit,
            memo
        )

        self._save_last_response(response.tx_hash, response)

        return response.tx_hash

    def build_transfer_tx(self, what: CryptoAmount, recipient: str) -> Transaction:
        tx = Transaction()
        tx.add_message(
            create_bank_send_msg(self._wallet.address(), Address(recipient),
                                 what.amount.internal_amount, self.get_denom(what.asset))
        )
        return tx

    async def broadcast_tx(self, tx_hex: str) -> str:
        broadcast_req = BroadcastTxRequest(
            tx_bytes=tx_hex.encode('utf-8'), mode=BroadcastMode.BROADCAST_MODE_SYNC
        )

        # broadcast the transaction
        resp = await asyncio.get_event_loop().run_in_executor(
            None,
            self._client.txs.BroadcastTx,
            broadcast_req)
        tx_digest = resp.tx_response.txhash

        # check that the response is successful
        initial_tx_response = self._client._parse_tx_response(resp.tx_response)
        initial_tx_response.ensure_successful()

        self._save_last_response(tx_digest, initial_tx_response)

        return tx_digest

    async def fetch_chain_id(self, server='') -> str:
        """
        Helper to get Cosmos' chain id
        :return:
        """
        url = f"{server or self.server_url}/node_info"
        j = await self._get_json(url)
        return j['node_info']['network']

    async def _get_json(self, url):
        logger.debug(f"GET {url}")
        response = await asyncio.get_event_loop().run_in_executor(
            None,
            self._client.txs.rest_client._session.get,
            url,
        )

        if response.status_code != 200:
            raise TxLoadException(f"Error getting {url!r}: code={response.status_code}; {response.text!r}")
        return response.json()

    @property
    def sdk_client(self) -> LedgerClient:
        return self._client

    @property
    def prefix(self) -> str:
        return self._prefix

    async def check_balance(self, address, amount: CryptoAmount):
        fees = await self.get_fees()
        fee = fees.fees[FeeOption.AVERAGE]

        balances = await self.get_balance(address)

        asset_balance = None
        native_balance = None

        for balance in balances:
            if balance.asset == amount.asset:
                asset_balance = balance
            if balance.asset == self._gas_asset:
                native_balance = balance

        is_native = amount.asset == self._gas_asset
        extra_fee = fee if is_native else Amount.from_base(0, self._decimal)

        if (asset_balance is None
                or asset_balance.amount.as_base < (required := amount.amount.as_base + extra_fee.as_base)):
            raise ValueError(f"Insufficient funds: {required} is required. Balance is {asset_balance}")

        if native_balance is None or native_balance.amount < fee:
            raise ValueError(f"Insufficient funds to pay fee: {fee.amount} {self._gas_asset}")

    def _make_wallet(self) -> LocalWallet:
        if self.phrase or self._private_key:
            pk = PrivateKey(bytes.fromhex(self.get_private_key()))
            self._wallet = LocalWallet(pk, self._prefix)
            return self._wallet

    def get_amount_string(self, amount):
        return f"{int(amount)}{self._denom}"

    def get_denom(self, asset: Asset) -> str:
        if asset == AssetATOM:
            return COSMOS_DENOM
        else:
            return str(asset).lower()

import asyncio
import logging
import time
from decimal import Decimal
from itertools import chain as chain_seq
from typing import Dict, List, Optional, Set, Union

from xchainpy2_mayanode import PoolsApi as PoolsApiMaya, MimirApi as MimirApiMaya, NetworkApi as NetworkApiMaya, \
    TransactionsApi as TransactionsApiMaya, LiquidityProvidersApi as LiquidityProvidersApiMaya, \
    QueueApi as QueueApiMaya, QuoteApi as QuoteApiMaya, SaversApi as SaversApiMaya
from xchainpy2_midgard import PoolDetail, THORNameDetails
from xchainpy2_midgard.api import DefaultApi as MidgardAPI
from xchainpy2_midgard.rest import ApiException
from xchainpy2_thorchain import THOR_BLOCK_TIME_SEC
from xchainpy2_thornode import PoolsApi, MimirApi, NetworkApi, InboundAddress, TransactionsApi, LiquidityProvidersApi, \
    SaversApi, QueueApi, QuoteApi, LastBlock, LiquidityProviderSummary
from xchainpy2_utils import Asset, AssetRUNE, AssetCACAO, Chain, CryptoAmount, RUNE_DECIMAL, CACAO_DECIMAL, Amount, \
    NetworkType
from .const import Mimir, TEN_MINUTES, SAME_ASSET_EXCHANGE_RATE, USD_ASSETS
from .env import URLs
from .midgard import MidgardAPIClient
from .models import PoolCache, InboundDetailCache, NetworkValuesCache, LiquidityPool, InboundDetail, SwapOutput, \
    InboundDetails, NameCache, LastBlockCache, QueryError
from .patch_clients import request_api_with_backup_hosts
from .swap import get_swap_fee, get_swap_output, get_single_swap, get_double_swap_output, \
    get_double_swap_slip
from .thornode import THORNodeAPIClient

logger = logging.getLogger('THORChainCache')

DEFAULT_MIDGARD = MidgardAPIClient()
DEFAULT_MIDGARD.configuration.host = URLs.Midgard.MAINNET

DEFAULT_THORNODE = THORNodeAPIClient()
DEFAULT_THORNODE.configuration.host = URLs.THORNode.MAINNET


class THORChainCache:
    """
    THORChainCache is a class that provides a cache for THORChain data.
    This class provides caching for data related to liquidity pools, network constants (Mimir),
    and incoming addresses and their attributes.

    """

    def __init__(self, midgard_client: MidgardAPIClient = None,
                 thornode_client: THORNodeAPIClient = None,
                 expire_pool: float = TEN_MINUTES,
                 expire_inbound: float = TEN_MINUTES,
                 expire_network: float = TEN_MINUTES,
                 native_asset: Asset = AssetRUNE,
                 network: NetworkType = NetworkType.MAINNET,
                 stable_coins: List[Asset] = None):
        """
        Constructor for THORChainCache.
        If Midgard or THORNode clients are not provided, default clients will be used.

        :param midgard_client: Тhe Midgard API client (optional)
        :param thornode_client: THORNode API client (optional)
        :param expire_pool: Expiration time for the pool cache in seconds
        :param expire_inbound: Expiration time for the inbound details cache in seconds
        :param expire_network: Expiration time for the network values cache in seconds
        :param native_asset: Native asset for the chain (RUNE or CACAO)
        :param network: Network type (MAINNET or STAGENET)
        :param stable_coins: Stable coins for the network (optional)
        """

        if not midgard_client:
            midgard_client = MidgardAPIClient()
            midgard_client.configuration.host = (
                URLs.Midgard.MAINNET if network == NetworkType.MAINNET else URLs.Midgard.STAGENET)
        else:
            assert midgard_client.configuration.host

        if not thornode_client:
            thornode_client = THORNodeAPIClient()
            thornode_client.configuration.host = (
                URLs.THORNode.MAINNET if network == NetworkType.MAINNET else URLs.THORNode.STAGENET)
        else:
            assert thornode_client.configuration.host

        self._midgard_client = midgard_client
        self._thornode_client = thornode_client
        self._pool_cache = PoolCache(0, {})
        self._inbound_cache = InboundDetailCache(0, {})
        self._network_cache = NetworkValuesCache(0, {})
        self._name_cache = NameCache({}, {}, {})
        self.expire_pool = expire_pool
        self.expire_inbound = expire_inbound
        self.expire_network = expire_network

        self.native_asset = native_asset
        self.network = network

        self.usd_stable_coins = stable_coins or USD_ASSETS[network]

        self.midgard_api = MidgardAPI(midgard_client)

        if native_asset == AssetRUNE:
            self.t_pool_api = PoolsApi(thornode_client)
            self.mimir_api = MimirApi(thornode_client)
            self.network_api = NetworkApi(thornode_client)
            self.tx_api = TransactionsApi(thornode_client)
            self.lp_api = LiquidityProvidersApi(thornode_client)
            self.queue_api = QueueApi(thornode_client)
            self.saver_api = SaversApi(thornode_client)
            self.quote_api = QuoteApi(thornode_client)
            self.chain = Chain.THORChain
            self.native_decimals = RUNE_DECIMAL
        elif native_asset == AssetCACAO:
            self.t_pool_api = PoolsApiMaya(thornode_client)
            self.mimir_api = MimirApiMaya(thornode_client)
            self.network_api = NetworkApiMaya(thornode_client)
            self.tx_api = TransactionsApiMaya(thornode_client)
            self.lp_api = LiquidityProvidersApiMaya(thornode_client)
            self.queue_api = QueueApiMaya(thornode_client)
            self.saver_api = SaversApiMaya(thornode_client)
            self.quote_api = QuoteApiMaya(thornode_client)
            self.chain = Chain.Maya
            self.native_decimals = CACAO_DECIMAL
        else:
            raise ValueError('Invalid native asset. Must be RUNE or CACAO')

        self._last_block_cache = LastBlockCache([], 0)

    @property
    def midgard_client(self) -> MidgardAPIClient:
        """
        Returns the Midgard API client.
        """
        return self._midgard_client

    @property
    def thornode_client(self) -> THORNodeAPIClient:
        """
        Returns the THORNode API client.
        """
        return self._thornode_client

    async def close(self):
        """
        Closes
        the
        Midgard and THORNode
        clients.
        It is recommended
        to
        call
        this
        method
        before
        the
        application
        exits.

        :return: None
        """
        if self._midgard_client:
            await self._midgard_client.close()
        if self._thornode_client:
            await self._thornode_client.close()

    def is_native_asset(self, a: Asset):
        """
        Checks if the
        asset is the
        native
        asset
        of
        the
        chain.

        :param
        a: Any
        Asset
        :return: True if the
        asset is the
        native
        asset, False
        otherwise
        :rtype: bool
        """
        return a == self.native_asset

    async def get_exchange_rate(self, a_from: Asset, a_to: Asset) -> Decimal:
        """
        Returns
        the
        exchange
        rate
        between
        two
        assets
        when
        using
        selected
        AMM
        protocol.
        Attention: slippage is not taken
        into
        account! Use
        THORChainQuery.quote_swap
        for more accurate simulation.

        :param
        a_from: Source
        Asset
        :param
        a_to: Destination
        Asset
        :return: Decimal
        """
        if a_from == a_to:
            return SAME_ASSET_EXCHANGE_RATE
        elif self.is_native_asset(a_from):
            lp_to = await self.get_pool_for_asset(a_to)
            return lp_to.asset_to_rune_ratio
        elif self.is_native_asset(a_to):
            lp_from = await self.get_pool_for_asset(a_from)
            return lp_from.rune_to_asset_ratio
        else:
            lp_from = await self.get_pool_for_asset(a_from)
            lp_to = await self.get_pool_for_asset(a_to)
            return lp_from.rune_to_asset_ratio * lp_to.asset_to_rune_ratio

    async def get_pool_for_asset(self, asset: Asset) -> LiquidityPool:
        """
        Returns
        the
        liquidity
        pool
        for the given asset.
        Rune
        does
        not have
        a
        pool, because
        it is the
        collateral
        for any other asset.

        :raises
        ValueError:
        if the asset is native
        :raises
        LookupError:
        if the pool is not found
        :param
        asset: Asset
        to
        find
        pool
        with
            :return: LiquidityPool
        """
        if self.is_native_asset(asset):
            raise ValueError('Native Rune does not have a pool')
        pool = self._pool_cache.pools.get(str(asset))
        if not pool:
            raise LookupError(f'Pool for {asset} not found')
        return pool

    async def get_pools(self, forced=False) -> Dict[str, LiquidityPool]:
        """
        Returns
        cached
        liquidity
        pools
        state as a
        Dict.

        :param
        forced: Force
        reload
        data
        from the API
        bypassing
        the
        cache
        :return: Dict[str, LiquidityPool]
        """

        time_elapsed = time.monotonic() - self._pool_cache.last_refreshed
        if forced or time_elapsed > self.expire_pool:
            await self.refresh_pool_cache()
        if self._pool_cache.pools:
            return self._pool_cache.pools
        raise QueryError('Could not refresh pools')

    async def refresh_pool_cache(self) -> Dict[str, LiquidityPool]:
        """
        This
        will
        reload
        the
        pool
        details
        from both THORNode and Midgard and store
        them
        into
        the
        cache.

        :return: Dict[str, LiquidityPool]
        """

        thornode_pools, midgard_pools = await asyncio.gather(
            request_api_with_backup_hosts(self.t_pool_api, self.t_pool_api.pools),
            request_api_with_backup_hosts(self._midgard_client, self.midgard_api.get_pools)
        )

        if not thornode_pools or not midgard_pools:
            raise QueryError('Could not refresh pools')

        thornode_pools_map = {str(p.asset): p for p in thornode_pools}
        midgard_pools_map = {str(p.asset): p for p in midgard_pools}
        all_assets = set(thornode_pools_map.keys()).union(set(midgard_pools_map.keys()))

        pool_map = {}
        midgard_pools: List[PoolDetail]

        for asset in all_assets:
            thornode_pool = thornode_pools_map.get(asset)
            midgard_pool = midgard_pools_map.get(asset)
            pool = LiquidityPool.from_pool_details(midgard_pool, thornode_pool)
            pool_map[str(pool.asset)] = pool

        self._pool_cache = PoolCache(time.monotonic(), pool_map)
        return self._pool_cache.pools

    async def refresh_inbound_cache(self) -> InboundDetails:
        """
        Refreshes the Inbound Details Cache which includes inbound address for each chain,
        current fee rate, halt state and more.
        It might be a better idea to call get_inbound_details() method that provides caching.

        :return InboundDetails
        """
        mimir, inbound_addresses = await asyncio.gather(
            request_api_with_backup_hosts(self.mimir_api, self.mimir_api.mimir),
            request_api_with_backup_hosts(self.network_api, self.network_api.inbound_addresses)
        )

        inbound_map = {}
        for inbound in inbound_addresses:
            inbound: InboundAddress

            if (
                    not inbound.chain or
                    not inbound.gas_rate or
                    not inbound.gas_rate_units or
                    not inbound.address or
                    not inbound.outbound_fee or
                    not inbound.outbound_tx_size
            ):
                raise QueryError('Missing required inbound info')

            halted = bool(
                inbound.halted or
                # is it necessary?
                mimir.get(Mimir.HALT_CHAIN_GLOBAL, False) or
                mimir.get(Mimir.halt_trading(inbound.chain), False)
            )

            halted_trading = bool(
                inbound.global_trading_paused or
                inbound.chain_trading_paused or
                # is it necessary?
                mimir.get(Mimir.HALT_TRADING, False) or
                mimir.get(Mimir.halt_trading(inbound.chain), False)
            )

            halted_lp = bool(
                inbound.chain_lp_actions_paused or
                # is it necessary?
                mimir.get(Mimir.PAUSE_LP, False) or
                mimir.get(Mimir.pause_lp(inbound.chain))
            )

            inbound_map[inbound.chain] = InboundDetail(
                chain=Chain(inbound.chain),
                address=inbound.address,
                gas_rate=int(inbound.gas_rate),
                gas_rate_units=inbound.gas_rate_units,
                outbound_fee=int(inbound.outbound_fee),
                outbound_tx_size=int(inbound.outbound_tx_size),
                halted_chain=halted,
                halted_trading=halted_trading,
                halted_lp=halted_lp,
                router=inbound.router,
                dust_threshold=int(inbound.dust_threshold),
            )

        inbound_map[Chain.THORChain.value] = InboundDetail(
            chain=Chain.THORChain,
            address='',
            router='',
            gas_rate=0,
            gas_rate_units='',
            outbound_fee=0,
            outbound_tx_size=0,
            halted_chain=False,
            halted_trading=not (mimir.get(Mimir.HALT_TRADING, False)),
            halted_lp=False,
            dust_threshold=0,
        )

        self._inbound_cache = InboundDetailCache(time.monotonic(), inbound_map)
        return self._inbound_cache.inbound_details

    async def refresh_network_values(self) -> Dict[str, int]:
        """
        Refreshes the NetworkValues Cache (Mimir and Constants combined).

        :return: Dict[str, int]
        """
        constants, mimir = await asyncio.gather(
            request_api_with_backup_hosts(self.network_api, self.network_api.constants),
            request_api_with_backup_hosts(self.mimir_api, self.mimir_api.mimir)
        )

        network_values = {}
        scope = chain_seq(constants.int_64_values.items(), mimir.items())
        for k, v in scope:
            network_values[k.upper()] = int(v)

        for k, v in constants.bool_values.items():
            network_values[k.upper()] = v == 'True'

        for k, v in constants.string_values.items():
            network_values[k.upper()] = v

        self._network_cache = NetworkValuesCache(time.monotonic(), network_values)
        return self._network_cache.network_values

    async def get_network_values(self, forced=False) -> Dict[str, int]:
        """
        Loads, caches and returns the Network values (Mimir and Constants combined).

        :param forced: force refresh
        :return:
        """
        sec_since_last_refresh = time.monotonic() - self._network_cache.last_refreshed
        if forced or sec_since_last_refresh > self.expire_network:
            await self.refresh_network_values()

        if not self._network_cache.network_values:
            raise QueryError('Could not refresh network values')

        return self._network_cache.network_values

    async def get_expected_swap_output(self, input_amount: CryptoAmount, dest_asset: Asset) -> SwapOutput:
        """
        This method does an approximate calculation of the swap output using known pool ratios and math.
        It takes into account only slippage but not the network fees.
        For a more accurate simulation, use THORChainQuery.quote_swap.

        :param input_amount: amount/asset to swap
        :param dest_asset: destination asset
        :return: SwapOutput structure
        """
        swap_output: SwapOutput
        if self.is_native_asset(input_amount.asset):
            # single swap from Rune -> asset
            pool = await self.get_pool_for_asset(dest_asset)
            swap_output = get_single_swap(input_amount, pool, False, self.native_asset)
        elif self.is_native_asset(dest_asset):
            # single swap from asset -> Rune
            pool = await self.get_pool_for_asset(input_amount.asset)
            swap_output = get_single_swap(input_amount, pool, True, self.native_asset)
        else:
            # double swap asset -> asset
            in_pool, out_pool = await asyncio.gather(
                self.get_pool_for_asset(input_amount.asset),
                self.get_pool_for_asset(dest_asset)
            )
            swap_output = await self._get_double_swap(input_amount, in_pool, out_pool)
        # Note this is needed to return a synth vs. a  native asset on swap out
        swap_output.output = CryptoAmount(swap_output.output.amount, dest_asset)
        return swap_output

    async def _get_double_swap(self, input_amount, in_pool, out_pool) -> SwapOutput:
        double_output = get_double_swap_output(input_amount, in_pool, out_pool)
        double_fee = await self._get_double_swap_fee(input_amount, in_pool, out_pool)
        double_slip = get_double_swap_slip(input_amount, in_pool, out_pool)
        return SwapOutput(
            output=double_output,
            swap_fee=double_fee,
            slip=double_slip,
        )

    async def _get_double_swap_fee(self, input_amount: CryptoAmount,
                                   pool1: LiquidityPool, pool2: LiquidityPool) -> CryptoAmount:
        """
        formula: getSwapFee1 + getSwapFee2
        """
        fee1_in_rune = get_swap_fee(input_amount, pool1, True)
        swap_output = get_swap_output(input_amount, pool1, True)
        fee2_in_asset = get_swap_fee(swap_output, pool2, False)
        fee2_in_rune = await self.convert(fee2_in_asset, self.native_asset)
        return fee1_in_rune + fee2_in_rune

    async def get_decimal_for_asset(self, asset: Asset) -> int:
        if asset == self.native_asset:
            return self.native_decimals
        else:
            pool = await self.get_pool_for_asset(asset)
            decimal = int(pool.thornode_details.decimals)
            return decimal if decimal > 0 else self.native_decimals

    async def convert(self, input_amount: CryptoAmount, out_asset: Asset) -> CryptoAmount:
        """
        Returns the exchange of a CryptoAmount to a different Asset
        Ex. convert(input:100 BUSD, outAsset: BTC) -> 0.0001234 BTC
        :param input_amount: amount/asset to convert to outAsset
        :param out_asset: the Asset you want to convert to
        :return: CryptoAmount of input
        """
        if input_amount.asset == out_asset:
            return input_amount

        exchange_rate = await self.get_exchange_rate(input_amount.asset, out_asset)
        out_decimals = await self.get_decimal_for_asset(out_asset)
        in_decimals = input_amount.amount.decimals
        base_amount_out = input_amount.amount * exchange_rate
        adjust_decimals = out_decimals - in_decimals
        base_amount_out *= Decimal(10 ** adjust_decimals)
        # noinspection PyTypeChecker
        amt = Amount.from_base(int(base_amount_out), out_decimals)
        return CryptoAmount(amt, out_asset)

    async def get_details_for_chain(self, chain: Union[str, Chain]) -> InboundDetail:
        """
        Returns the inbound details for a given chain. Results are cached.

        :param chain: Chain (enum or str)
        :return:
        """

        if isinstance(chain, Chain):
            chain = chain.value

        inbound = await self.get_inbound_details()
        if not inbound:
            raise QueryError('Could not get inbound details')
        if not inbound.get(chain.upper()):
            raise QueryError(f'Could not get inbound details for {chain}')
        return inbound[chain]

    async def get_inbound_details(self, forced=False) -> InboundDetails:
        """
        Returns the inbound details such as inbound vault address, fee rate and so on. Results are cached.

        :param forced: force refresh
        :return: inbound details (dict)
        """
        time_elapsed = time.monotonic() - self._inbound_cache.last_refreshed
        if forced or time_elapsed > self.expire_inbound:
            await self.refresh_inbound_cache()

        if self._inbound_cache:
            return self._inbound_cache.inbound_details
        else:
            raise QueryError('Could not refresh inbound cache')

    async def get_deepest_usd_pool(self) -> LiquidityPool:
        deepest_rune_depth = 0
        deepest_pool = None
        for usd_asset in self.usd_stable_coins:
            usd_pool = await self.get_pool_for_asset(usd_asset)
            if usd_pool.rune_balance.amount > deepest_rune_depth:
                deepest_rune_depth = usd_pool.rune_balance.amount
                deepest_pool = usd_pool
        if not deepest_pool:
            raise QueryError('no USD Pool found')
        return deepest_pool

    @property
    def is_thorchain(self):
        """
        Returns True if this class is configured for THORChain protocol.

        :return:
        """
        return self.native_asset == AssetRUNE

    @property
    def is_maya(self):
        """
        Returns True if this class is configured for Maya protocol.

        :return:
        """
        return self.native_asset == AssetCACAO

    def pluck_native_block_height(self, data: LastBlock) -> int:
        """
        Extracts the native block height from the LastBlock object.

        :param data: LastBlock object
        :return: int block height
        """
        key = 'thorchain' if self.is_thorchain else 'mayachain'
        return getattr(data, key)

    async def get_native_block_height(self) -> int:
        """
        Loads the native block height from the THORNode/MayaNode API.

        :return: int block height
        """
        data = await self.get_last_block()
        return self.pluck_native_block_height(data[0])

    async def get_last_block(self) -> List[LastBlock]:
        """
        Loads the last block information from the THORNode/MayaNode API.
        From LastBlock you can get the block height of the protocol and last observed height of the connected chains.

        :return: List[LastBlock]
        """
        t = time.monotonic()
        if t - self._last_block_cache.last_refreshed > THOR_BLOCK_TIME_SEC:
            last_block_obj = await self.network_api.lastblock()
            if not last_block_obj:
                raise QueryError("No last block")
            self._last_block_cache.last_refreshed = t
            self._last_block_cache.last_blocks = last_block_obj
            return last_block_obj
        else:
            return self._last_block_cache.last_blocks

    def get_rune_address(self, lp: LiquidityProviderSummary) -> str:
        """
        Plucks the RUNE address from the LiquidityProviderSummary object depending on the protocol.
        It is either 'rune_address' for THORChain or 'cacao_address' for MayaChain.

        :param lp: LiquidityProviderSummary
        :return: str
        """
        key = 'rune_address' if self.is_thorchain else 'cacao_address'
        return getattr(lp, key)

    async def get_liquidity_provider(self, asset: Union[str, Asset], address: str,
                                     height: int = 0) -> LiquidityProviderSummary:
        """
        Get the liquidity provider details for a given asset and address. Results are not cached.
        If height is not provided, the latest block height will be used.

        :param asset: Asset or str name of the pool
        :param address: Address of the liquidity provider
        :param height: Height of the block to query, if 0 then the latest block height will be used
        :return: LiquidityProviderSummary
        """

        if isinstance(asset, Asset):
            asset = str(asset)

        lps = await self.lp_api.liquidity_providers(asset, height=height)
        return next((lp for lp in lps
                     if lp.asset_address == address or
                     self.get_rune_address(lp) == address),
                    None)

    async def get_fee_rate(self, chain: Union[str, Chain]) -> int:
        """
        Returns the fee rate for a given chain from the inbound details. Results are cached.

        :param chain: Chain
        :return: Typical fee rate for the chain. sat/byte for Bitcoin, gas for Ethereum, etc.
        """

        inbound = await self.get_details_for_chain(chain)
        return int(inbound.gas_rate)

    async def get_names_by_address(self, address: str) -> Set[str]:
        """
        Look up THORNames that are associated with a wallet address. Names are cached.

        :raises ValueError: if address is not provided
        :param address: Address to look up
        :return: Set[str] - just the set of names without details (see: load_names_by_address)
        """

        if not address:
            raise ValueError('address is required')

        last_block = await self.get_native_block_height()
        self._name_cache.invalidate(last_block)

        if names := self._name_cache.address_to_name.get(address):
            return names

        try:
            thor_names = await self.midgard_api.get_thor_names_by_address(address)
            self._name_cache.address_to_name[address] = thor_names
            return thor_names
        except ApiException as e:
            if getattr(e, 'status', 0) == 404:
                self._name_cache.address_to_name[address] = set()
                return set()
            else:
                raise

    async def get_names_with_details(self, address: str) -> List[THORNameDetails]:
        """
        Look up THORNames with their details by a wallet address. Names are cached.
        But details are not cached yet.

        :param address: Address to look up
        :return: List[THORNameDetails]
        """

        names = await self.get_names_by_address(address)
        if not names:
            return []
        details = await asyncio.gather(*[self.get_name_details(name) for name in names])
        return list(details)

    async def get_name_details(self, name: str) -> Optional[THORNameDetails]:
        """
        Look up THORName details by a THORName. Details are cached.

        :param name: THORName to look up
        :return: Optional[THORNameDetails]
        """
        if not name:
            raise ValueError('name is required')
        name = name.lower()

        last_block = await self.get_native_block_height()
        self._name_cache.invalidate(last_block)

        if details := self._name_cache.name_details.get(name):
            return details

        try:
            thor_name = await self.midgard_api.get_thor_name_detail(name)
            self._name_cache.put(name, thor_name)
            return thor_name
        except ApiException as e:
            if e.status == 404:
                self._name_cache.put(name, None)
                return None
            else:
                raise

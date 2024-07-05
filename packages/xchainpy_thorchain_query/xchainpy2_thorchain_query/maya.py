from xchainpy2_utils import DEFAULT_CHAIN_ATTRS, CACAO_DECIMAL, NetworkType
from . import URLs
from .midgard import MidgardAPIClient
from .cache import THORChainCache
from .const import DEFAULT_INTERFACE_ID
from .query import THORChainQuery
from .thornode import THORNodeAPIClient


class MayaChainQuery(THORChainQuery):
    def __init__(self,
                 cache: THORChainCache = None,
                 chain_attributes=DEFAULT_CHAIN_ATTRS,
                 interface_id=DEFAULT_INTERFACE_ID,
                 native_decimal=CACAO_DECIMAL):
        if not cache:
            network = NetworkType.MAINNET
            midgard_client = MidgardAPIClient()
            midgard_client.configuration.host = (
                URLs.Midgard.MAINNET if network == NetworkType.MAINNET else URLs.Midgard.STAGENET)
            thornode_client = THORNodeAPIClient()
            thornode_client.configuration.host = (
                URLs.THORNode.MAINNET if network == NetworkType.MAINNET else URLs.THORNode.STAGENET)

            cache = THORChainCache(

            )

        super().__init__(cache, chain_attributes, interface_id, native_decimal)

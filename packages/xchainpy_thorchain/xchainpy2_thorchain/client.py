from typing import Optional

from packages.xchainpy_client.xchainpy2_client import XChainClient, RootDerivationPaths, FeeBounds
from xchainpy2_utils import Chain, NetworkType
from .const import NodeURL, DEFAULT_CHAIN_IDS, DEFAULT_CLIENT_URLS


class THORChainClient(XChainClient):
    """
    network: Optional[NetworkType] = None
    phrase: Optional[str] = None
    fee_bound: Optional[FeeBounds] = None
    root_derivation_paths: Optional[RootDerivationPaths] = None

    """

    def __init__(self,
                 network: Optional[NetworkType] = None,
                 phrase: Optional[str] = None,
                 fee_bound: Optional[FeeBounds] = None,
                 root_derivation_paths: Optional[RootDerivationPaths] = None,
                 client_urls=DEFAULT_CLIENT_URLS,
                 chain_ids=DEFAULT_CHAIN_IDS
                 ):

        super().__init__(Chain.THORChain, params)

    if isinstance(client_urls, NodeURL):
        client_urls = {NetworkType.MAINNET: client_urls}

    self.client_urls = client_urls
    # self._client = None

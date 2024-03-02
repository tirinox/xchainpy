from typing import Optional, Union

from . import get_ltc_address_prefix
from .const import ROOT_DERIVATION_PATHS, AssetTestLTC, LTC_DECIMAL
from xchainpy2_bitcoin import BitcoinClient, BLOCKSTREAM_EXPLORERS
from xchainpy2_client import FeeBounds, RootDerivationPaths
from xchainpy2_utils import NetworkType, AssetLTC


class LitecoinClient(BitcoinClient):
    def __init__(self,
                 network=NetworkType.MAINNET,
                 phrase: Optional[str] = None,
                 private_key: Union[str, bytes, callable, None] = None,
                 fee_bound: Optional[FeeBounds] = None,
                 root_derivation_paths: Optional[RootDerivationPaths] = ROOT_DERIVATION_PATHS,
                 explorer_providers=BLOCKSTREAM_EXPLORERS,
                 wallet_index=0,
                 # provider: Optional[UtxoOnlineDataProvider] = None,
                 provider_names=None):
        super().__init__(network, phrase, private_key, fee_bound, root_derivation_paths, explorer_providers,
                         wallet_index, provider_names)

        self._prefix = get_ltc_address_prefix(network)
        self._decimal = LTC_DECIMAL

        if network in (NetworkType.MAINNET, NetworkType.STAGENET):
            self._service_network = 'bitcoin'
            self._gas_asset = AssetLTC
        elif network == NetworkType.DEVNET:
            self._service_network = 'bitcoinlib_test'
            self._gas_asset = AssetLTC
        else:
            self._service_network = 'testnet'
            self._gas_asset = AssetTestLTC

        self.service = self._make_service()

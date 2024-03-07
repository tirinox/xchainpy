from typing import Optional, Union

from xchainpy2_bitcoin import BitcoinClient
from xchainpy2_client import FeeBounds, RootDerivationPaths
from xchainpy2_utils import NetworkType, AssetLTC, Asset
from . import get_ltc_address_prefix
from .const import ROOT_DERIVATION_PATHS, AssetTestLTC, LTC_DECIMAL, DEFAULT_PROVIDER_NAMES, DEFAULT_LTC_EXPLORERS


class LitecoinClient(BitcoinClient):
    def __init__(self,
                 network=NetworkType.MAINNET,
                 phrase: Optional[str] = None,
                 private_key: Union[str, bytes, callable, None] = None,
                 fee_bound: Optional[FeeBounds] = None,
                 root_derivation_paths: Optional[RootDerivationPaths] = ROOT_DERIVATION_PATHS,
                 explorer_providers=DEFAULT_LTC_EXPLORERS,
                 wallet_index=0,
                 # provider: Optional[UtxoOnlineDataProvider] = None,
                 provider_names=DEFAULT_PROVIDER_NAMES):
        if not provider_names:
            provider_names = DEFAULT_PROVIDER_NAMES

        super().__init__(network, phrase, private_key, fee_bound, root_derivation_paths, explorer_providers,
                         wallet_index, provider_names)

        self._prefix = get_ltc_address_prefix(network)
        self._decimal = LTC_DECIMAL

    @staticmethod
    def _detect_network_and_gas_asset(network: NetworkType) -> (str, Asset):
        if network in (NetworkType.MAINNET, NetworkType.STAGENET):
            return 'litecoin', AssetLTC
        elif network == NetworkType.DEVNET:
            return 'litecoin_testnet', AssetTestLTC
        else:
            return 'litecoin_testnet', AssetTestLTC

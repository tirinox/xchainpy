from typing import Optional, Union

from bitcoinlib.services.litecoind import LitecoindClient

from xchainpy2_bitcoin import BitcoinClient
from xchainpy2_client import FeeBounds, RootDerivationPaths
from xchainpy2_utils import NetworkType, AssetLTC, Asset, Chain
from . import get_ltc_address_prefix
from .const import ROOT_DERIVATION_PATHS, AssetTestLTC, LTC_DECIMAL, DEFAULT_PROVIDER_NAMES, DEFAULT_LTC_EXPLORERS, \
    LTC_DEFAULT_FEE_BOUNDS


class LitecoinClient(BitcoinClient):
    def __init__(self,
                 network=NetworkType.MAINNET,
                 phrase: Optional[str] = None,
                 private_key: Union[str, bytes, callable, None] = None,
                 fee_bound: Optional[FeeBounds] = LTC_DEFAULT_FEE_BOUNDS,
                 root_derivation_paths: Optional[RootDerivationPaths] = ROOT_DERIVATION_PATHS,
                 explorer_providers=DEFAULT_LTC_EXPLORERS,
                 wallet_index=0,
                 provider_names=DEFAULT_PROVIDER_NAMES,
                 daemon_url: Optional[str] = None):
        """
        LitecoinClient interface
        Constructor to create a new LitecoinClient.

        :param network: The network type
        :param phrase: The seed phrase
        :param private_key: The private key
        :param fee_bound: The fee bound
        :param root_derivation_paths: The root derivation paths
        :param explorer_providers: The explorer providers
        :param wallet_index: The wallet index (default is 0)
        :param provider_names: The provider names
        :param daemon_url: The daemon url. If it is provided, the provider_names will be ignored
        """
        if not provider_names:
            provider_names = DEFAULT_PROVIDER_NAMES

        super().__init__(network, phrase, private_key, fee_bound, root_derivation_paths, explorer_providers,
                         wallet_index, provider_names, daemon_url,
                         _chain=Chain.Litecoin)

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

    @staticmethod
    def _make_daemon_service(url):
        return LitecoindClient(base_url=url)

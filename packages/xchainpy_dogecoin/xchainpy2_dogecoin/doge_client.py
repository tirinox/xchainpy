from typing import Optional, Union

from bitcoinlib.services.dogecoind import DogecoindClient

from xchainpy2_bitcoin import BitcoinClient
from xchainpy2_client import FeeBounds, RootDerivationPaths
from xchainpy2_utils import NetworkType, Asset, Chain, AssetDOGE
from .const import ROOT_DERIVATION_PATHS, DOGE_DECIMAL, DEFAULT_PROVIDER_NAMES, DEFAULT_DOGE_EXPLORERS, \
    DOGE_DEFAULT_FEE_BOUNDS, AssetTestDOGE


class DogecoinClient(BitcoinClient):
    def __init__(self,
                 network=NetworkType.MAINNET,
                 phrase: Optional[str] = None,
                 private_key: Union[str, bytes, callable, None] = None,
                 fee_bound: Optional[FeeBounds] = DOGE_DEFAULT_FEE_BOUNDS,
                 root_derivation_paths: Optional[RootDerivationPaths] = ROOT_DERIVATION_PATHS,
                 explorer_providers=DEFAULT_DOGE_EXPLORERS,
                 wallet_index=0,
                 provider_names=DEFAULT_PROVIDER_NAMES,
                 daemon_url: Optional[str] = None):
        """
        DogecoinClient interface
        Constructor to create a new Do.

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
                         _chain=Chain.Doge)

        self._prefix = ""
        self._decimal = DOGE_DECIMAL

    @staticmethod
    def _detect_network_and_gas_asset(network: NetworkType) -> (str, Asset):
        if network in (NetworkType.MAINNET, NetworkType.STAGENET):
            return 'dogecoin', AssetDOGE
        elif network == NetworkType.DEVNET:
            return 'dogecoin_testnet', AssetTestDOGE
        else:
            return 'dogecoin_testnet', AssetTestDOGE

    @staticmethod
    def _make_daemon_service(url):
        return DogecoindClient(base_url=url)

    def get_address(self) -> str:
        """
        Get the DOGE address
        Uses standard P2PKH address format (starting with 'D' for mainnet, 'n' for testnet)
        :return: The DOGE address
        """
        return self.get_public_key().address(script_type='p2pkh')

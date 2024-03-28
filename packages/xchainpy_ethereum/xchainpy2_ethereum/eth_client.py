import logging
from datetime import datetime
from functools import reduce
from typing import Optional, List, Union

from eth_account import Account
from web3 import EthereumTesterProvider, Web3
from web3.providers import BaseProvider

from xchainpy2_client import XChainClient, RootDerivationPaths, FeeBounds, Fees, XcTx, TxPage, FeeRate
from xchainpy2_ethereum import ETH_ROOT_DERIVATION_PATHS, ETH_DECIMAL, DEFAULT_ETH_EXPLORER_PROVIDERS
from xchainpy2_ethereum.utils import is_valid_eth_address, format_fee_history, estimate_fees
from xchainpy2_utils import Chain, NetworkType, CryptoAmount, AssetETH, Asset

logger = logging.getLogger(__name__)


class EthereumClient(XChainClient):

    def __init__(self,
                 network=NetworkType.MAINNET,
                 phrase: Optional[str] = None,
                 private_key: Union[str, bytes, callable, None] = None,
                 fee_bound: Optional[FeeBounds] = None,
                 root_derivation_paths: Optional[RootDerivationPaths] = None,
                 explorer_providers=DEFAULT_ETH_EXPLORER_PROVIDERS.copy(),
                 wallet_index=0,
                 provider: Optional[BaseProvider] = None
                 ):
        """
        Initialize Ethereum
        :param network: Network type. Default is `NetworkType.MAINNET`
        :param phrase: Mnemonic phrase
        :param private_key: Private key (if you want to use a private key instead of a mnemonic phrase)
        :param fee_bound: Fee bound structure. See: FeeBounds
        :param root_derivation_paths: Dictionary of derivation paths for each network type. See: ROOT_DERIVATION_PATHS
        :param explorer_providers: Dictionary of explorer providers for each network type.
        :param wallet_index: int (default 0)
        :param provider: EVM RPC provider
        """
        root_derivation_paths = root_derivation_paths.copy() \
            if root_derivation_paths else ETH_ROOT_DERIVATION_PATHS.copy()

        super().__init__(Chain.Ethereum, network, phrase, private_key, fee_bound, root_derivation_paths, wallet_index)

        self.explorers = explorer_providers
        self._gas_asset = AssetETH
        self._decimal = ETH_DECIMAL

        self.tx_responses = {}

        self._remake_provider(provider)

    @property
    def provider(self):
        return self.web3.provider

    @provider.setter
    def provider(self, provider: BaseProvider):
        self._remake_provider(provider)

    def _remake_provider(self, provider: BaseProvider):
        if not provider:
            provider = EthereumTesterProvider()
            logger.warning("You are using EthereumTesterProvider. Please use your own provider to hide this warning!")
        self.web3 = Web3(provider)

    def validate_address(self, address: str) -> bool:
        """
        Validates a Ethereum address.
        :param address: Address string
        :return: True if valid, False otherwise.
        """
        return is_valid_eth_address(address)

    def get_address(self) -> str:
        """
        Get the address for the given wallet index.
        :return: string address
        """
        account = self.get_account()
        return account.address

    async def get_balance(self, address: str = '') -> List[CryptoAmount]:
        """
        Get the balance of a given address.
        :param address: By default, it will return the balance of the current wallet. (optional)
        :return:
        """
        raise NotImplementedError("Ethereum balance fetching is not implemented yet")

    def get_public_key(self):
        """
        Get the public key for the current wallet.
        """
        return self.get_account().public_key

    def get_account(self):
        """
        Get the account object (web3) for the current wallet.
        """
        return Account.from_key(self.get_private_key())

    async def get_transactions(self, address: str, offset: int = 0, limit: int = 0,
                               start_time: Optional[datetime] = None, end_time: Optional[datetime] = None,
                               asset: Optional[Asset] = None) -> TxPage:
        pass

    async def get_transaction_data(self, tx_id: str) -> Optional[XcTx]:
        pass

    async def get_fees(self) -> Fees:
        """
        Get Ethereum fees
        Fees are estimated based on the last 20 blocks.
        FeeRate is in Gwei
        """
        return await self._call_service(estimate_fees, self.web3)

    async def get_last_fee(self) -> FeeRate:
        """
        Get the last Ethereum fee
        FeeRate is in Gwei
        """
        fee = await self._call_service(self.web3.eth._gas_price)
        return Web3.from_wei(fee, 'gwei')

    async def transfer(self, what: CryptoAmount, recipient: str, memo: Optional[str] = None,
                       fee_rate: Optional[int] = None, **kwargs) -> str:
        pass

    async def broadcast_tx(self, tx_hex: str) -> str:
        pass

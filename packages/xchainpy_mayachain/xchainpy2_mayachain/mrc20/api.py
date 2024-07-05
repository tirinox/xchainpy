import logging
from typing import Optional, List, Union

from aiohttp import ClientSession

from xchainpy2_utils import NetworkType, Asset
from .model import MRC20Token, MRC20Price, MNFTToken, MRC20Order, MNFTOrder, MNFTBalance, MRC20StakingInfo, \
    MRC20StakingBalance, MRC20Balance
from .utils import build_url

MAYA_SCAN_BASE_API = "https://www.MayaScan.org/api/"
"""Base URL for the MayaScan API"""

MAYANS_BASE_API = 'https://www.mayans.app/api/'
"""Base URL for the Mayans API"""

logger = logging.getLogger('MayaScanClient')
"""Logger for the MayaScanClient"""


class MayaScanException(Exception):
    """
    Exception raised when an error occurs in the MayaScanClient
    """

    def __init__(self, *args, code=200):
        super().__init__(*args)
        self.code = code

    @property
    def is_not_found(self):
        """
        Check if the error is a 404 error
        """
        return self.code == 404


class MayaScanClient:
    """
    Client for interacting with the MayaScan API
    See: https://www.mayascan.org/standards/api/docs
    """

    def __init__(self, network: NetworkType = NetworkType.MAINNET, session=None):
        """
        Initialize the MayaScanClient. At the moment, only the mainnet is supported.

        :param network: Network type to use
        :type network: NetworkType
        :param session: aiohttp ClientSession to use for requests
        :type session: aiohttp.ClientSession
        """
        self.network = network
        self.base_api_url = MAYA_SCAN_BASE_API
        self.mayans_base_api_url = MAYANS_BASE_API

        self.session: ClientSession = session

    def url_transactions(self, mtype: str = None, page=None):
        """
        Get the URL for the transactions endpoint

        :param mtype: Type of transaction to filter by
        :param page: Page number to get
        :return: str
        """
        return self._url(f'tx/sends', page=page, mtype=mtype)

    # -- MRC20 --

    def url_all_tokens(self):
        """
        Get the URL to the whole MRC20 tokens list

        :return: str
        """
        return self._url('mrc20')

    def url_ticker(self, ticker: str):
        """
        Get the URL for a specific MRC20 token

        :param ticker: Ticker of the token
        :return: str
        """

        return self._url(f'mrc20', ticker=ticker)

    def url_balance(self, address: str):
        """
        Get the URL for the MRC20 balance of a specific address

        :param address: MayaChain address
        :return: str
        """
        return self._url(f'mrc20/balance', address=address)

    def url_orderbook(self, ticker: str):
        """
        Get the URL for the MRC20 orderbook of a specific token

        :param ticker: Ticker of the token
        :return: str
        """
        return self._url(f'mrc20/orderBook', ticker=ticker)

    def url_price(self, ticker: str):
        """
        Get the URL for the MRC20 price of a specific token

        :param ticker: Ticker of the token
        :return: str
        """
        return self._url(f'mrc20/price', ticker=ticker)

    def url_staking(self):
        """
        Get the URL for the staking summary

        :return: str
        """
        return self._url(f'staking')

    def url_staking_balance(self, ticker: str, address: str):
        """
        Get the URL for the MRC20 token staking balance of a specific address

        :param ticker: Ticker of the token
        :param address: MayaChain address
        :return: str
        """
        return self._url(f'staking/balance', address=address, ticker=ticker, is_mayans=True)

    async def get_all_tokens(self) -> List[MRC20Token]:
        """
        Get all MRC20 token information

        :return: List[MRC20Token]
        """

        tokens = await self._request(self.url_all_tokens())
        return MRC20Token.from_api(tokens)

    async def get_token(self, ticker: Union[Asset, str]) -> Optional[MRC20Token]:
        """
        Get a specific MRC20 token information

        :param ticker: MRC20 token ticker
        :return: Optional[MRC20Token]
        """
        ticker = self._get_ticker(ticker)
        token = await self._request(self.url_ticker(ticker))
        return MRC20Token.from_dict(token) if token else None

    async def get_balance(self, address: str) -> List[MRC20Price]:
        """
        Get the MRC20 token balances of a specific address

        :param address: MayaChain address
        :return:
        """
        results = await self._request(self.url_balance(address))
        return [MRC20Balance.from_dict(r) for r in results]

    async def get_orderbook(self, ticker: Union[Asset, str]) -> List[MRC20Order]:
        """
        Get the MRC20 token orderbook

        :param ticker: MRC20 token ticker
        :return: List[MRC20Order]
        :rtype: List[MRC20Order]
        """

        ticker = self._get_ticker(ticker)
        results = await self._request(self.url_orderbook(ticker))
        return MRC20Order.from_api(results)

    async def get_price(self, ticker: Union[Asset, str]) -> Optional[MRC20Price]:
        """
        Get the MRC20 token price (last trade price probably)

        :param ticker: MRC20 token ticker
        :return: Optional[MRC20Price]
        """
        ticker = self._get_ticker(ticker)
        price = await self._request(self.url_price(ticker))
        return MRC20Price.from_dict(price) if price else None

    async def get_staking_summary(self) -> List[MRC20StakingInfo]:
        """
        Get the staking summary of MRC20 tokens

        :return: List[MRC20StakingInfo]
        """
        results = await self._request(self.url_staking())
        return [MRC20StakingInfo.from_dict(r) for r in results]

    async def get_staking_balance(self, address: str, ticker: Union[Asset, str]) -> Optional[MRC20StakingBalance]:
        """
        Get the MRC20 token staking balance of a specific MayaChain address.
        None is returned if the address has no staking balance.

        :param address: MayaChain address
        :param ticker: MRC20 token ticker
        :return: Optional[MRC20StakingBalance]
        """

        ticker = self._get_ticker(ticker)
        result = await self._request(self.url_staking_balance(ticker, address))
        return MRC20StakingBalance.from_dict(result) if result else None

    # -- NFT --

    def url_nft_all_tokens(self):
        """
        Get the URL for all NFT token collection

        :return: str
        """
        return self._url('mnft')

    def url_nft_collection(self, symbol):
        """
        Get the URL for a specific NFT token collection

        :param symbol: M-NFT symbol
        :return: str
        """
        symbol = self._get_ticker(symbol)
        return self._url(f'mnft', symbol=symbol)

    def url_nft_balance(self, address: str, page=0):
        """
        Get the URL for the NFT balance of a specific address

        :param address: MayaChain address
        :param page: Page number to get, default is 0
        :return: str
        """
        return self._url(f'mnft/balance', address=address, page=page)

    def url_nft_orderbook(self, symbol=None, page=0):
        """
        Get the URL for the M-NFT orderbook for a specific collection

        :param symbol: M-NFT collection symbol
        :param page: Page number to get, default is 0
        :return: str
        """
        return self._url(f'mnft/orderBook', symbol=symbol, page=page)

    async def get_all_nft_tokens(self) -> List[MNFTToken]:
        """
        Get all M-NFT token collections information

        :return: List[MNFTToken]
        """
        results = await self._request(self.url_nft_all_tokens())
        return MNFTToken.from_api(results)

    async def get_nft_collection(self, symbol: str) -> Optional[MNFTToken]:
        """
        Get a specific M-NFT token collection information

        :param symbol: M-NFT collection symbol
        :return: Optional[MNFTToken]
        """
        result = await self._request(self.url_nft_collection(symbol))
        return MNFTToken.from_dict(result) if result else None

    async def get_nft_balance(self, address: str, page=0) -> List[MNFTBalance]:
        """
        Get the M-NFT balance of a specific address

        :param address: MayaChain address
        :param page: Page number to get, default is 0
        :return: List[MNFTBalance]
        """
        results = await self._request(self.url_nft_balance(address, page))
        return [MNFTBalance.from_dict(d) for d in results]

    async def get_nft_orderbook(self, symbol=None, page=0) -> List[MNFTOrder]:
        """
        Get the M-NFT orderbook for a specific collection

        :param symbol: M-NFT collection symbol
        :param page: Page number to get, default is 0
        :return: List[MNFTOrder]
        """
        results = await self._request(self.url_nft_orderbook(symbol, page))
        return MNFTOrder.from_api(results)

    # -- common --

    async def close(self):
        """
        Close the aiohttp session if any
        """
        if self.session:
            await self.session.close()
            self.session = None

    async def _ensure_session(self):
        if not self.session:
            self.session = ClientSession()

    async def _request(self, url):
        logger.debug(f'Starting request {url!r}')
        await self._ensure_session()
        async with self.session.get(url) as resp:
            try:
                r = await resp.json()
            except Exception as e:
                raise MayaScanException(f'Error parsing response from {url}: {e}')

            if isinstance(r, dict) and r.get('error'):
                raise MayaScanException(f'Error response from {url}: {r["error"]}', code=resp.status)
            return r

    @staticmethod
    def _get_ticker(ticker):
        if isinstance(ticker, str):
            return ticker
        elif isinstance(ticker, Asset):
            return ticker.ticker

    def _url(self, endpoint: str, params=None, is_mayans=False, **kwargs):
        params = params or {}
        if kwargs:
            params.update(kwargs)

        # remove all None values
        params = {k: v for k, v in params.items() if v is not None}

        base_url = self.mayans_base_api_url if is_mayans else self.base_api_url

        return build_url(base_url + endpoint, params)

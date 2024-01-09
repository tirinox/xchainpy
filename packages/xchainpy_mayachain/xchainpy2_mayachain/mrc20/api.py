import logging
from typing import Optional, List, Union

from aiohttp import ClientSession

from xchainpy2_utils import NetworkType, Asset
from .model import MRC20Token, MRC20Price, MNFTToken, MRC20Order, MNFTOrder, MNFTBalance, MRC20StakingInfo, \
    MRC20StakingBalance, MRC20Balance
from .utils import build_url

MAYA_SCAN_BASE_API = "https://www.MayaScan.org/api/"
MAYANS_BASE_API = 'https://www.mayans.app/api/'

logger = logging.getLogger('MayaScanClient')


class MayaScanException(Exception):
    def __init__(self, *args, code=200):
        super().__init__(*args)
        self.code = code

    @property
    def is_not_found(self):
        return self.code == 404


class MayaScanClient:
    def __init__(self, network: NetworkType = NetworkType.MAINNET, session=None):
        self.network = network
        self.base_api_url = MAYA_SCAN_BASE_API
        self.mayans_base_api_url = MAYANS_BASE_API

        self.session: ClientSession = session

    def url_transactions(self, mtype: str = None, page=None):
        return self._url(f'tx/sends', page=page, mtype=mtype)

    # -- MRC20 --

    def url_all_tokens(self):
        return self._url('mrc20')

    def url_ticker(self, ticker: str):
        return self._url(f'mrc20', ticker=ticker)

    def url_balance(self, address: str):
        return self._url(f'mrc20/balance', address=address)

    def url_orderbook(self, ticker: str):
        return self._url(f'mrc20/orderBook', ticker=ticker)

    def url_price(self, ticker: str):
        return self._url(f'mrc20/price', ticker=ticker)

    def url_staking(self):
        return self._url(f'staking')

    def url_staking_balance(self, ticker: str, address: str):
        return self._url(f'staking/balance', address=address, ticker=ticker, is_mayans=True)

    async def get_all_tokens(self) -> List[MRC20Token]:
        tokens = await self._request(self.url_all_tokens())
        return MRC20Token.from_api(tokens)

    async def get_token(self, ticker: Union[Asset, str]) -> Optional[MRC20Token]:
        ticker = self._get_ticker(ticker)
        token = await self._request(self.url_ticker(ticker))
        return MRC20Token.from_dict(token) if token else None

    async def get_balance(self, address: str):
        results = await self._request(self.url_balance(address))
        return [MRC20Balance.from_dict(r) for r in results]

    async def get_orderbook(self, ticker: Union[Asset, str]):
        ticker = self._get_ticker(ticker)
        results = await self._request(self.url_orderbook(ticker))
        return MRC20Order.from_api(results)

    async def get_price(self, ticker: Union[Asset, str]) -> Optional[MRC20Price]:
        ticker = self._get_ticker(ticker)
        price = await self._request(self.url_price(ticker))
        return MRC20Price.from_dict(price) if price else None

    async def get_staking_summary(self):
        results = await self._request(self.url_staking())
        return [MRC20StakingInfo.from_dict(r) for r in results]

    async def get_staking_balance(self, address: str, ticker: Union[Asset, str]):
        ticker = self._get_ticker(ticker)
        result = await self._request(self.url_staking_balance(ticker, address))
        return MRC20StakingBalance.from_dict(result) if result else None

    # -- NFT --

    def url_nft_all_tokens(self):
        return self._url('mnft')

    def url_nft_collection(self, symbol):
        symbol = self._get_ticker(symbol)
        return self._url(f'mnft', symbol=symbol)

    def url_nft_balance(self, address: str, page=0):
        return self._url(f'mnft/balance', address=address, page=page)

    def url_nft_orderbook(self, symbol=None, page=0):
        return self._url(f'mnft/orderBook', symbol=symbol, page=page)

    async def get_all_nft_tokens(self):
        results = await self._request(self.url_nft_all_tokens())
        return MNFTToken.from_api(results)

    async def get_nft_collection(self, symbol: str):
        result = await self._request(self.url_nft_collection(symbol))
        return MNFTToken.from_dict(result) if result else None

    async def get_nft_balance(self, address: str, page=0):
        results = await self._request(self.url_nft_balance(address, page))
        return [MNFTBalance.from_dict(d) for d in results]

    async def get_nft_orderbook(self, symbol=None, page=0):
        results = await self._request(self.url_nft_orderbook(symbol, page))
        return MNFTOrder.from_api(results)

    # -- common --

    async def close(self):
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

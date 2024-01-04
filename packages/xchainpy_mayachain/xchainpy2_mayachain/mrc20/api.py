from xchainpy2_utils import NetworkType

MAYA_SCAN_BASE_API = "https://www.MayaScan.org/api/"


class MayaScanClient:
    def __init__(self, network: NetworkType = NetworkType.MAINNET, session=None):
        self._network = network
        self._base_api = MAYA_SCAN_BASE_API
        if network == NetworkType.STAGENET:
            self._base_api = MAYA_SCAN_BASE_API
        self.session = session

    def url(self, endpoint: str):
        return self._base_api + endpoint

    def url_all_tokens(self):
        return self.url('mrc20')

    def url_ticker(self, ticker: str):
        return self.url(f'mrc20?ticker={ticker}')

    def url_balance(self, address: str):
        return self.url(f'mrc20/balance?address={address}')

    def url_nft_all_tokens(self):
        return self.url('mnft')

    def url_nft_collection(self, symbol):
        return self.url(f'mnft?symbol={symbol}')

    def url_nft_balance(self, address: str, page=0):
        return self.url(f'mnft/balance?address={address}&page={page}')

    async def _request(self, url):
        async with self.session.get(url) as resp:
            return await resp.json()

    async def get_all_tokens(self):
        return await self._request(self.url_all_tokens())

    async def get_token(self, ticker: str):
        return await self._request(self.url_ticker(ticker))

    async def get_balance(self, address: str):
        return await self._request(self.url_balance(address))

    async def get_all_nft_tokens(self):
        return await self._request(self.url_nft_all_tokens())

    async def get_nft_collection(self, symbol: str):
        return await self._request(self.url_nft_collection(symbol))

    async def get_nft_balance(self, address: str, page=0):
        return await self._request(self.url_nft_balance(address, page))

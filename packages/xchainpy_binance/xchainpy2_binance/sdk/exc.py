import ujson as json


class BinanceChainAPIException(Exception):

    def __init__(self, j, response, status_code):
        self.code = 0
        try:
            json_res = j
            # json_res = json.loads(contents)
        except ValueError:
            if not response.content:
                self.message = status_code
            else:
                self.message = 'Invalid JSON error message from Binance Chain: {}'.format(response.text)
        else:
            self.code = json_res.get('code', None)
            self.message = json_res.get('message')
        self.status_code = status_code
        self.response = response
        self.request = getattr(response, 'request', None)

    def __str__(self):  # pragma: no cover
        return f'BinanceAPIError(code={self.code}, status={self.status_code}, message={self.message!r})'


class BinanceChainRequestException(Exception):
    pass


class BinanceChainBroadcastException(Exception):
    pass


class BinanceChainSigningAuthenticationException(Exception):
    pass


class BinanceChainRPCException(Exception):
    def __init__(self, response):
        self.code = 0
        try:
            json_res = json.loads(response.content)
        except ValueError:
            self.message = 'Invalid JSON error message from Binance Chain: {}'.format(response.text)
        else:
            self.code = json_res['error']['code']
            self.message = json_res['error']['message']
        self.status_code = response.status_code
        self.response = response
        self.request = getattr(response, 'request', None)

    def __str__(self):  # pragma: no cover
        return f'RPCError(code={self.code}): {self.message}'

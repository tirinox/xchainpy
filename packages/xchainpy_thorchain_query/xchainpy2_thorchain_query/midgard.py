from multiprocessing.pool import ThreadPool
from typing import Optional

import xchainpy2_midgard as mdg
from xchainpy2_utils import XCHAINPY_IDENTIFIER, NINE_REALMS_CLIENT_HEADER, DEFAULT_USER_AGENT
from .patch_clients import RESTClientRetry, ConfigurationEx, HeadersPatch


class MidgardAPIClient(HeadersPatch, mdg.ApiClient):
    # noinspection PyMissingConstructor
    def __init__(self, configuration: Optional[ConfigurationEx] = None,
                 header_name=NINE_REALMS_CLIENT_HEADER,
                 header_value=XCHAINPY_IDENTIFIER,
                 cookie=None, pool_processes=None, user_agent=DEFAULT_USER_AGENT):
        if configuration is None:
            configuration = ConfigurationEx()
        self.configuration = configuration

        self.pool = ThreadPool(pool_processes)

        self.default_headers = {}
        if header_name is not None:
            self.default_headers[header_name] = header_value
        self.cookie = cookie

        # Set User-Agent.
        self.user_agent = user_agent

        # Patch REST client with additional retry logic and backup hosts
        self.rest_client = None

    async def close(self):
        if self.rest_client:
            await self.rest_client.close()

    def request(self, method, url, query_params=None, headers=None, post_params=None, body=None, _preload_content=True,
                _request_timeout=None):
        if not self.rest_client:
            # it must be initialized here, because we need to be inside asyncio loop
            self.rest_client = RESTClientRetry(self.configuration)

        if _request_timeout is None:
            _request_timeout = self.configuration.timeout

        return super().request(method, url, query_params, headers, post_params, body, _preload_content,
                               _request_timeout)

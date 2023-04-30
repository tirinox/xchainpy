from multiprocessing.pool import ThreadPool
from typing import Optional

import xchainpy2_midgard as mdg
from . import DEFAULT_USER_AGENT
from .patch_clients import RESTClientRetry, ConfigurationEx


class MidgardAPIClient(mdg.ApiClient):
    # noinspection PyMissingConstructor
    def __init__(self, configuration: Optional[ConfigurationEx] = None,
                 header_name=None, header_value=None, cookie=None):
        if configuration is None:
            configuration = ConfigurationEx()
        self.configuration = configuration

        self.pool = ThreadPool()

        self.default_headers = {}
        if header_name is not None:
            self.default_headers[header_name] = header_value
        self.cookie = cookie

        # Set default User-Agent.
        self.user_agent = DEFAULT_USER_AGENT

        # Patch REST client with additional retry logic and backup hosts
        self.rest_client = RESTClientRetry(
            configuration,
        )

    async def close(self):
        await self.rest_client.close()

    def deserialize(self, response, response_type):
        # todo: raise
        return super().deserialize(response, response_type)

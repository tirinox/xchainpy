from multiprocessing.pool import ThreadPool

import xchainpy2_thornode as thornode
from .patch_clients import ConfigurationEx, RESTClientRetry
from .const import DEFAULT_USER_AGENT, XCHAINPY_IDENTIFIER, NINE_REALMS_CLIENT_HEADER


class ThornodeAPIClient(thornode.ApiClient):
    # noinspection PyMissingConstructor
    def __init__(self, configuration: ConfigurationEx = None,
                 header_name=NINE_REALMS_CLIENT_HEADER, header_value=XCHAINPY_IDENTIFIER,
                 cookie=None):
        if configuration is None:
            configuration = ConfigurationEx()
        self.configuration = configuration

        self.pool = ThreadPool()
        # Patch REST client with additional retry logic and backup hosts
        self.rest_client = RESTClientRetry(
            configuration,
        )
        self.default_headers = {}
        if header_name is not None:
            self.default_headers[header_name] = header_value
        self.cookie = cookie

        # Set default User-Agent.
        self.user_agent = DEFAULT_USER_AGENT

    async def close(self):
        await self.rest_client.close()

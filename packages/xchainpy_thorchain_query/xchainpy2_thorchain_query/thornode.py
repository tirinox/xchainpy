from multiprocessing.pool import ThreadPool

import xchainpy2_thornode as thornode
from xchainpy2_utils import NINE_REALMS_CLIENT_HEADER, XCHAINPY_IDENTIFIER, DEFAULT_USER_AGENT
from .patch_clients import ConfigurationEx, RESTClientRetry, HeadersPatch


class THORNodeAPIClient(HeadersPatch, thornode.ApiClient):
    """
    THORNode API client.

    :param configuration: ConfigurationEx object
    """
    # noinspection PyMissingConstructor
    def __init__(self, configuration: ConfigurationEx = None,
                 header_name=NINE_REALMS_CLIENT_HEADER, header_value=XCHAINPY_IDENTIFIER,
                 cookie=None):
        if configuration is None:
            configuration = ConfigurationEx()
        self.configuration = configuration

        self.pool = ThreadPool()

        # Patch REST client with additional retry logic and backup hosts
        self.rest_client = None

        self.default_headers = {}
        if header_name is not None:
            self.default_headers[header_name] = header_value
        self.cookie = cookie

        # Set default User-Agent.
        self.user_agent = DEFAULT_USER_AGENT

    async def close(self):
        """
        Close the REST client.

        :return: None
        """
        if self.rest_client:
            await self.rest_client.close()

    def request(self, method, url, query_params=None, headers=None, post_params=None, body=None, _preload_content=True,
                _request_timeout=None):
        """
        Override the request method to use the RESTClientRetry class and set the request timeout.

        :param method: Method type
        :param url: URL
        :param query_params: Parameters
        :param headers: Headers
        :param post_params: POST parameters
        :param body: The body of the request
        :param _preload_content: Flag to preload content
        :param _request_timeout: Timeout for the request
        :return: Response
        :rtype: RESTResponse
        """
        if not self.rest_client:
            # it must be initialized here, because we need to be inside asyncio loop
            self.rest_client = RESTClientRetry(self.configuration)

        if _request_timeout is None:
            _request_timeout = self.configuration.timeout

        return super().request(method, url, query_params, headers, post_params, body, _preload_content,
                               _request_timeout)

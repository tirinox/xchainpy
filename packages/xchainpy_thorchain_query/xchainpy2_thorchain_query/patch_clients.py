import ssl
import urllib.parse
from typing import Optional

import aiohttp
import certifi
from aiohttp import ClientTimeout
from aiohttp.helpers import sentinel
from aiohttp_retry import ExponentialRetry, RetryClient

from xchainpy2_midgard import Configuration
from xchainpy2_midgard.rest import RESTClientObject

DEFAULT_RETRY_ATTEMPTS = 3
DEFAULT_TIMEOUT = 300


class ConfigurationEx(Configuration):
    def __init__(self):
        super().__init__()
        self.backup_hosts = []
        self.timeout = DEFAULT_TIMEOUT
        self.retry_config = ExponentialRetry(attempts=DEFAULT_RETRY_ATTEMPTS)
        self.raise_for_status = False


class RESTClientRetry(RESTClientObject):
    # noinspection PyMissingConstructor
    def __init__(self, configuration: Optional[ConfigurationEx], pools_size=4, maxsize=4):
        # We rewrite the constructor completely to add retry logic and backup hosts
        # No need to call super().__init__ here, to avoid creating a useless session

        # ca_certs
        if configuration.ssl_ca_cert:
            ca_certs = configuration.ssl_ca_cert
        else:
            # if not set certificate file, use Mozilla's root certificates.
            ca_certs = certifi.where()

        ssl_context = ssl.create_default_context(cafile=ca_certs)
        if configuration.cert_file:
            ssl_context.load_cert_chain(
                configuration.cert_file, keyfile=configuration.key_file
            )

        connector = aiohttp.TCPConnector(
            limit=maxsize,
            ssl_context=ssl_context,
            verify_ssl=configuration.verify_ssl
        )

        self.retry_config = configuration.retry_config

        # Parse URLs and make sure that all backup hosts are valid
        self.backup_hosts_urls = [
            urllib.parse.urlparse(host) for host in configuration.backup_hosts
        ] if configuration.backup_hosts else None

        if self.backup_hosts_urls:
            assert all(
                url.netloc and url.scheme.lower() in ('http', 'https')
                for url in self.backup_hosts_urls
            )

        # Retrying client
        timeout = sentinel
        if isinstance(configuration.timeout, (float, int)):
            timeout = ClientTimeout(total=configuration.timeout)
        elif isinstance(configuration.timeout, ClientTimeout):
            timeout = configuration.timeout

        self.pool_manager = RetryClient(
            raise_for_status=configuration.raise_for_status,
            retry_options=configuration.retry_config,
            connector=connector,
            timeout=timeout
        )
        # todo: move "proxy" parameter to request method

    async def request(self, method, url, query_params=None, headers=None,
                      body=None, post_params=None,
                      _preload_content=True, _request_timeout=None):
        if self.backup_hosts_urls:
            # noinspection PyTypeChecker
            urls = [None] + self.backup_hosts_urls
            exc = None
            for backup_url in urls:
                try:
                    # if it is None, it is original url
                    if backup_url:
                        # replace scheme and netloc
                        original_url = urllib.parse.urlparse(url)
                        url = original_url._replace(
                            scheme=backup_url.scheme,
                            netloc=backup_url.netloc,
                        )
                    print(f'{url=}, {backup_url=}')
                    return await super().request(method, url, query_params,
                                                 headers, body, post_params,
                                                 _preload_content, _request_timeout)
                except Exception as e:
                    exc = e
                    # todo: log exception
            raise Exception(f'All backup hosts failed ({exc}) "{method}", {url=}')
        else:
            return await super().request(method, url, query_params, headers, body, post_params, _preload_content,
                                         _request_timeout)

    async def close(self):
        await self.pool_manager.close()

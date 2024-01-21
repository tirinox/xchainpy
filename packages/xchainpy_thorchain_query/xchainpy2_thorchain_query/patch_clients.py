import logging
import ssl
from typing import Optional

import aiohttp
import certifi
from aiohttp import ClientTimeout
from aiohttp.helpers import sentinel
from aiohttp_retry import ExponentialRetry, RetryClient

from xchainpy2_cosmos import DEFAULT_REST_USER_AGENT
from xchainpy2_midgard import Configuration
from xchainpy2_midgard.rest import RESTClientObject
from xchainpy2_utils import XCHAINPY_IDENTIFIER, NINE_REALMS_CLIENT_HEADER

DEFAULT_RETRY_ATTEMPTS = 3
DEFAULT_TIMEOUT = 300


class ConfigurationEx(Configuration):
    def __init__(self):
        super().__init__()
        self.timeout = DEFAULT_TIMEOUT
        self.retry_config = ExponentialRetry(attempts=DEFAULT_RETRY_ATTEMPTS)
        self.raise_for_status = False
        self.backup_hosts = []

    @classmethod
    def new(cls, host=None, api_key=None, api_key_prefix=None, username=None, password=None,
            ssl_ca_cert=None, cert_file=None, key_file=None, timeout=DEFAULT_TIMEOUT,
            retry_config=ExponentialRetry(attempts=DEFAULT_RETRY_ATTEMPTS), raise_for_status=False,
            backup_hosts=None, verify_ssl=True):
        if backup_hosts is None:
            backup_hosts = []
        self = cls()
        self.host = host
        self.api_key = api_key
        self.api_key_prefix = api_key_prefix
        self.username = username
        self.password = password
        self.ssl_ca_cert = ssl_ca_cert
        self.cert_file = cert_file
        self.key_file = key_file
        self.timeout = timeout
        self.retry_config = retry_config
        self.raise_for_status = raise_for_status
        self.backup_hosts = backup_hosts
        self.verify_ssl = verify_ssl
        return self


class RESTClientRetry(RESTClientObject):
    # noinspection PyMissingConstructor
    def __init__(self, configuration: Optional[ConfigurationEx], pools_size=4, maxsize=4):
        # We rewrite the constructor completely to add retry logic and backup hosts
        # No need to call super().__init__ here, to avoid creating a useless session
        self.configuration = configuration

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

    async def close(self):
        await self.pool_manager.close()


logger = logging.getLogger('backup_hosts')


async def request_api_with_backup_hosts(api, method, *args, **kwargs):
    configuration = getattr(api, 'configuration', None)
    if not configuration:
        configuration = api.api_client.configuration

    original_host = configuration.host

    hosts = []
    if original_host and original_host != '/':
        hosts.append(original_host)

    hosts.extend(configuration.backup_hosts)

    if not hosts:
        raise Exception('No hosts to try')

    last_exception = None
    for host in hosts:
        try:
            configuration.host = host
            if isinstance(method, str):
                method = getattr(api, method)
            return await method(*args, **kwargs)
        except Exception as e:
            logger.error(f'Host {host} failed for method {method}: {e}')
            last_exception = e
        finally:
            configuration.host = original_host

    if last_exception:
        raise Exception('All backup hosts failed') from last_exception

    return None


class HeadersPatch:
    def __init__(self):
        self.default_headers = None

    def patch_client(self, user_agent=DEFAULT_REST_USER_AGENT, identifier9r=XCHAINPY_IDENTIFIER):
        headers = self.default_headers
        headers['User-Agent'] = user_agent
        if identifier9r:
            headers[NINE_REALMS_CLIENT_HEADER] = identifier9r

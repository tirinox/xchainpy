# coding: utf-8

"""
    Mayanode API

    Mayanode REST API.  # noqa: E501

    OpenAPI spec version: 1.110.0
    Contact: devs@mayachain.org
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

from __future__ import absolute_import

import unittest

import xchainpy2_mayanode
from xchainpy2_mayanode.api.liquidity_providers_api import LiquidityProvidersApi  # noqa: E501
from xchainpy2_mayanode.rest import ApiException


class TestLiquidityProvidersApi(unittest.TestCase):
    """LiquidityProvidersApi unit test stubs"""

    def setUp(self):
        self.api = LiquidityProvidersApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_liquidity_provider(self):
        """Test case for liquidity_provider

        """
        pass

    def test_liquidity_providers(self):
        """Test case for liquidity_providers

        """
        pass


if __name__ == '__main__':
    unittest.main()

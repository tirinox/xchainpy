# coding: utf-8

"""
    Thornode API

    Thornode REST API.  # noqa: E501

    OpenAPI spec version: 1.134.0
    Contact: devs@thorchain.org
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

from __future__ import absolute_import

import unittest

import xchainpy2_thornode
from xchainpy2_thornode.api.pools_api import PoolsApi  # noqa: E501
from xchainpy2_thornode.rest import ApiException


class TestPoolsApi(unittest.TestCase):
    """PoolsApi unit test stubs"""

    def setUp(self):
        self.api = PoolsApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_dpool(self):
        """Test case for dpool

        """
        pass

    def test_dpools(self):
        """Test case for dpools

        """
        pass

    def test_pool(self):
        """Test case for pool

        """
        pass

    def test_pools(self):
        """Test case for pools

        """
        pass


if __name__ == '__main__':
    unittest.main()

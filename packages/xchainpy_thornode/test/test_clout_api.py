# coding: utf-8

"""
    Thornode API

    Thornode REST API.  # noqa: E501

    OpenAPI spec version: 2.135.0
    Contact: devs@thorchain.org
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

from __future__ import absolute_import

import unittest

import xchainpy2_thornode
from xchainpy2_thornode.api.clout_api import CloutApi  # noqa: E501
from xchainpy2_thornode.rest import ApiException


class TestCloutApi(unittest.TestCase):
    """CloutApi unit test stubs"""

    def setUp(self):
        self.api = CloutApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_swapper_clout(self):
        """Test case for swapper_clout

        """
        pass


if __name__ == '__main__':
    unittest.main()

# coding: utf-8

"""
    Thornode API

    Thornode REST API.  # noqa: E501

    OpenAPI spec version: 1.125.0
    Contact: devs@thorchain.org
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

from __future__ import absolute_import

import unittest

import xchainpy2_thornode
from xchainpy2_thornode.api.block_api import BlockApi  # noqa: E501
from xchainpy2_thornode.rest import ApiException


class TestBlockApi(unittest.TestCase):
    """BlockApi unit test stubs"""

    def setUp(self):
        self.api = BlockApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_block(self):
        """Test case for block

        """
        pass


if __name__ == '__main__':
    unittest.main()

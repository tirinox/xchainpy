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
from xchainpy2_thornode.api.mimir_api import MimirApi  # noqa: E501
from xchainpy2_thornode.rest import ApiException


class TestMimirApi(unittest.TestCase):
    """MimirApi unit test stubs"""

    def setUp(self):
        self.api = MimirApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_mimir(self):
        """Test case for mimir

        """
        pass

    def test_mimir_admin(self):
        """Test case for mimir_admin

        """
        pass

    def test_mimir_key(self):
        """Test case for mimir_key

        """
        pass

    def test_mimir_node(self):
        """Test case for mimir_node

        """
        pass

    def test_mimir_nodes(self):
        """Test case for mimir_nodes

        """
        pass


if __name__ == '__main__':
    unittest.main()

# coding: utf-8

"""
    Mayanode API

    Mayanode REST API.  # noqa: E501

    OpenAPI spec version: 1.103.3
    Contact: devs@mayachain.org
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

from __future__ import absolute_import

import unittest

import xchainpy2_mayanode
from xchainpy2_mayanode.api.nodes_api import NodesApi  # noqa: E501
from xchainpy2_mayanode.rest import ApiException


class TestNodesApi(unittest.TestCase):
    """NodesApi unit test stubs"""

    def setUp(self):
        self.api = NodesApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_node(self):
        """Test case for node

        """
        pass

    def test_nodes(self):
        """Test case for nodes

        """
        pass


if __name__ == '__main__':
    unittest.main()

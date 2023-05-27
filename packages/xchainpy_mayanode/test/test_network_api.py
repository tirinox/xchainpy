# coding: utf-8

"""
    Mayanode API

    Mayanode REST API.  # noqa: E501

    OpenAPI spec version: 1.104.0
    Contact: devs@mayachain.org
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

from __future__ import absolute_import

import unittest

import xchainpy2_mayanode
from xchainpy2_mayanode.api.network_api import NetworkApi  # noqa: E501
from xchainpy2_mayanode.rest import ApiException


class TestNetworkApi(unittest.TestCase):
    """NetworkApi unit test stubs"""

    def setUp(self):
        self.api = NetworkApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_ban(self):
        """Test case for ban

        """
        pass

    def test_constants(self):
        """Test case for constants

        """
        pass

    def test_inbound_addresses(self):
        """Test case for inbound_addresses

        """
        pass

    def test_lastblock(self):
        """Test case for lastblock

        """
        pass

    def test_lastblock_chain(self):
        """Test case for lastblock_chain

        """
        pass

    def test_network(self):
        """Test case for network

        """
        pass

    def test_ragnarok(self):
        """Test case for ragnarok

        """
        pass

    def test_version(self):
        """Test case for version

        """
        pass


if __name__ == '__main__':
    unittest.main()

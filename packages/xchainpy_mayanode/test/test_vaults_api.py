# coding: utf-8

"""
    Mayanode API

    Mayanode REST API.  # noqa: E501

    OpenAPI spec version: 1.107.1
    Contact: devs@mayachain.org
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

from __future__ import absolute_import

import unittest

import xchainpy2_mayanode
from xchainpy2_mayanode.api.vaults_api import VaultsApi  # noqa: E501
from xchainpy2_mayanode.rest import ApiException


class TestVaultsApi(unittest.TestCase):
    """VaultsApi unit test stubs"""

    def setUp(self):
        self.api = VaultsApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_asgard(self):
        """Test case for asgard

        """
        pass

    def test_vault(self):
        """Test case for vault

        """
        pass

    def test_vault_pubkeys(self):
        """Test case for vault_pubkeys

        """
        pass

    def test_yggdrasil(self):
        """Test case for yggdrasil

        """
        pass


if __name__ == '__main__':
    unittest.main()

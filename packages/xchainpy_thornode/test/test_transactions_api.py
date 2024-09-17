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
from xchainpy2_thornode.api.transactions_api import TransactionsApi  # noqa: E501
from xchainpy2_thornode.rest import ApiException


class TestTransactionsApi(unittest.TestCase):
    """TransactionsApi unit test stubs"""

    def setUp(self):
        self.api = TransactionsApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_tx(self):
        """Test case for tx

        """
        pass

    def test_tx_signers(self):
        """Test case for tx_signers

        """
        pass

    def test_tx_signers_old(self):
        """Test case for tx_signers_old

        """
        pass

    def test_tx_stages(self):
        """Test case for tx_stages

        """
        pass

    def test_tx_status(self):
        """Test case for tx_status

        """
        pass


if __name__ == '__main__':
    unittest.main()

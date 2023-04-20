# coding: utf-8

"""
    Thornode API

    Thornode REST API.  # noqa: E501

    OpenAPI spec version: 1.108.3
    Contact: devs@thorchain.org
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

from __future__ import absolute_import

import unittest

import thornode_client
from thornode_client.api.quote_api import QuoteApi  # noqa: E501
from thornode_client.rest import ApiException


class TestQuoteApi(unittest.TestCase):
    """QuoteApi unit test stubs"""

    def setUp(self):
        self.api = QuoteApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_quoteloanclose(self):
        """Test case for quoteloanclose

        """
        pass

    def test_quoteloanopen(self):
        """Test case for quoteloanopen

        """
        pass

    def test_quotesaverdeposit(self):
        """Test case for quotesaverdeposit

        """
        pass

    def test_quotesaverwithdraw(self):
        """Test case for quotesaverwithdraw

        """
        pass

    def test_quoteswap(self):
        """Test case for quoteswap

        """
        pass


if __name__ == '__main__':
    unittest.main()

# coding: utf-8

"""
    Thornode API

    Thornode REST API.  # noqa: E501

    OpenAPI spec version: 1.130.1
    Contact: devs@thorchain.org
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

from __future__ import absolute_import

import unittest

import xchainpy2_thornode
from xchainpy2_thornode.api.trade_accounts_api import TradeAccountsApi  # noqa: E501
from xchainpy2_thornode.rest import ApiException


class TestTradeAccountsApi(unittest.TestCase):
    """TradeAccountsApi unit test stubs"""

    def setUp(self):
        self.api = TradeAccountsApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_trade_accounts(self):
        """Test case for trade_accounts

        """
        pass


if __name__ == '__main__':
    unittest.main()
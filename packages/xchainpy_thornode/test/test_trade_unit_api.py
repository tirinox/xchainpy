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
from xchainpy2_thornode.api.trade_unit_api import TradeUnitApi  # noqa: E501
from xchainpy2_thornode.rest import ApiException


class TestTradeUnitApi(unittest.TestCase):
    """TradeUnitApi unit test stubs"""

    def setUp(self):
        self.api = TradeUnitApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_trade_unit(self):
        """Test case for trade_unit

        """
        pass


if __name__ == '__main__':
    unittest.main()
# coding: utf-8

"""
    Midgard Public API

    The Midgard Public API queries THORChain and any chains linked via the Bifröst and prepares information about the network to be readily available for public users. The API parses transaction event data from THORChain and stores them in a time-series database to make time-dependent queries easy. Midgard does not hold critical information. To interact with THORChain protocol, users should query THORNode directly.  # noqa: E501

    OpenAPI spec version: 2.24.3
    Contact: devs@thorchain.org
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

from __future__ import absolute_import

import unittest

import xchainpy2_midgard
from xchainpy2_midgard.models.coins import Coins  # noqa: E501
from xchainpy2_midgard.rest import ApiException


class TestCoins(unittest.TestCase):
    """Coins unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testCoins(self):
        """Test Coins"""
        # FIXME: construct object with mandatory attributes with example values
        # model = xchainpy2_midgard.models.coins.Coins()  # noqa: E501
        pass


if __name__ == '__main__':
    unittest.main()

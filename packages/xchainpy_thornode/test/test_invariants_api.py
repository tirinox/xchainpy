# coding: utf-8

"""
    Thornode API

    Thornode REST API.  # noqa: E501

    OpenAPI spec version: 3.0.0
    Contact: devs@thorchain.org
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

from __future__ import absolute_import

import unittest

import xchainpy2_thornode
from xchainpy2_thornode.api.invariants_api import InvariantsApi  # noqa: E501
from xchainpy2_thornode.rest import ApiException


class TestInvariantsApi(unittest.TestCase):
    """InvariantsApi unit test stubs"""

    def setUp(self):
        self.api = InvariantsApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_invariant(self):
        """Test case for invariant

        """
        pass

    def test_invariants(self):
        """Test case for invariants

        """
        pass


if __name__ == '__main__':
    unittest.main()

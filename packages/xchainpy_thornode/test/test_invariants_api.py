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
from thornode_client.api.invariants_api import InvariantsApi  # noqa: E501
from thornode_client.rest import ApiException


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

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

import xchainpy2_thornode
from xchainpy2_thornode.api.borrowers_api import BorrowersApi  # noqa: E501
from xchainpy2_thornode.rest import ApiException


class TestBorrowersApi(unittest.TestCase):
    """BorrowersApi unit test stubs"""

    def setUp(self):
        self.api = BorrowersApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_borrower(self):
        """Test case for borrower

        """
        pass

    def test_borrowers(self):
        """Test case for borrowers

        """
        pass


if __name__ == '__main__':
    unittest.main()

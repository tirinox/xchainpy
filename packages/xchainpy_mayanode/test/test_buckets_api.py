# coding: utf-8

"""
    Mayanode API

    Mayanode REST API.  # noqa: E501

    OpenAPI spec version: 1.103.2
    Contact: devs@mayachain.org
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

from __future__ import absolute_import

import unittest

import xchainpy2_mayanode
from xchainpy2_mayanode.api.buckets_api import BucketsApi  # noqa: E501
from xchainpy2_mayanode.rest import ApiException


class TestBucketsApi(unittest.TestCase):
    """BucketsApi unit test stubs"""

    def setUp(self):
        self.api = BucketsApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_bucket(self):
        """Test case for bucket

        """
        pass

    def test_buckets(self):
        """Test case for buckets

        """
        pass


if __name__ == '__main__':
    unittest.main()

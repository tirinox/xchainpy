# coding: utf-8

"""
    Mayanode API

    Mayanode REST API.  # noqa: E501

    OpenAPI spec version: 1.103.3
    Contact: devs@mayachain.org
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

from __future__ import absolute_import

import unittest

import xchainpy2_mayanode
from xchainpy2_mayanode.api.pol_api import POLApi  # noqa: E501
from xchainpy2_mayanode.rest import ApiException


class TestPOLApi(unittest.TestCase):
    """POLApi unit test stubs"""

    def setUp(self):
        self.api = POLApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_pol(self):
        """Test case for pol

        """
        pass


if __name__ == '__main__':
    unittest.main()

# coding: utf-8

"""
    Mayanode API

    Mayanode REST API.  # noqa: E501

    OpenAPI spec version: 1.108.1
    Contact: devs@mayachain.org
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

from __future__ import absolute_import

import unittest

import xchainpy2_mayanode
from xchainpy2_mayanode.api.queue_api import QueueApi  # noqa: E501
from xchainpy2_mayanode.rest import ApiException


class TestQueueApi(unittest.TestCase):
    """QueueApi unit test stubs"""

    def setUp(self):
        self.api = QueueApi()  # noqa: E501

    def tearDown(self):
        pass

    def test_queue(self):
        """Test case for queue

        """
        pass

    def test_queue_outbound(self):
        """Test case for queue_outbound

        """
        pass

    def test_queue_scheduled(self):
        """Test case for queue_scheduled

        """
        pass


if __name__ == '__main__':
    unittest.main()

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
from xchainpy2_thornode.api.queue_api import QueueApi  # noqa: E501
from xchainpy2_thornode.rest import ApiException


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

    def test_queue_swap(self):
        """Test case for queue_swap

        """
        pass


if __name__ == '__main__':
    unittest.main()

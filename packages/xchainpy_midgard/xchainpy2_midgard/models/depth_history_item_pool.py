# coding: utf-8

"""
    Midgard Public API

    The Midgard Public API queries THORChain and any chains linked via the Bifröst and prepares information about the network to be readily available for public users. The API parses transaction event data from THORChain and stores them in a time-series database to make time-dependent queries easy. Midgard does not hold critical information. To interact with THORChain protocol, users should query THORNode directly.  # noqa: E501

    OpenAPI spec version: 2.23.2
    Contact: devs@thorchain.org
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

import pprint
import re  # noqa: F401

import six

class DepthHistoryItemPool(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """
    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        'pool': 'str',
        'total_depth': 'str'
    }

    attribute_map = {
        'pool': 'pool',
        'total_depth': 'totalDepth'
    }

    def __init__(self, pool=None, total_depth=None):  # noqa: E501
        """DepthHistoryItemPool - a model defined in Swagger"""  # noqa: E501
        self._pool = None
        self._total_depth = None
        self.discriminator = None
        self.pool = pool
        self.total_depth = total_depth

    @property
    def pool(self):
        """Gets the pool of this DepthHistoryItemPool.  # noqa: E501

        asset for the given pool  # noqa: E501

        :return: The pool of this DepthHistoryItemPool.  # noqa: E501
        :rtype: str
        """
        return self._pool

    @pool.setter
    def pool(self, pool):
        """Sets the pool of this DepthHistoryItemPool.

        asset for the given pool  # noqa: E501

        :param pool: The pool of this DepthHistoryItemPool.  # noqa: E501
        :type: str
        """
        if pool is None:
            raise ValueError("Invalid value for `pool`, must not be `None`")  # noqa: E501

        self._pool = pool

    @property
    def total_depth(self):
        """Gets the total_depth of this DepthHistoryItemPool.  # noqa: E501

        Int64(e8) in rune, the total value in the pool (both assets and rune) at the end of the interval. Note: this is twice of the pool's Rune depth. (as pools are symmetrically balance)   # noqa: E501

        :return: The total_depth of this DepthHistoryItemPool.  # noqa: E501
        :rtype: str
        """
        return self._total_depth

    @total_depth.setter
    def total_depth(self, total_depth):
        """Sets the total_depth of this DepthHistoryItemPool.

        Int64(e8) in rune, the total value in the pool (both assets and rune) at the end of the interval. Note: this is twice of the pool's Rune depth. (as pools are symmetrically balance)   # noqa: E501

        :param total_depth: The total_depth of this DepthHistoryItemPool.  # noqa: E501
        :type: str
        """
        if total_depth is None:
            raise ValueError("Invalid value for `total_depth`, must not be `None`")  # noqa: E501

        self._total_depth = total_depth

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.swagger_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value
        if issubclass(DepthHistoryItemPool, dict):
            for key, value in self.items():
                result[key] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, DepthHistoryItemPool):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other

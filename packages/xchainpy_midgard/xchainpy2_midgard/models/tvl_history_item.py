# coding: utf-8

"""
    Midgard Public API

    The Midgard Public API queries THORChain and any chains linked via the Bifröst and prepares information about the network to be readily available for public users. The API parses transaction event data from THORChain and stores them in a time-series database to make time-dependent queries easy. Midgard does not hold critical information. To interact with THORChain protocol, users should query THORNode directly.  # noqa: E501

    OpenAPI spec version: 2.18.2
    Contact: devs@thorchain.org
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

import pprint
import re  # noqa: F401

import six

class TVLHistoryItem(object):
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
        'end_time': 'str',
        'pools_depth': 'list[DepthHistoryItemPool]',
        'rune_price_usd': 'str',
        'start_time': 'str',
        'total_value_bonded': 'str',
        'total_value_locked': 'str',
        'total_value_pooled': 'str'
    }

    attribute_map = {
        'end_time': 'endTime',
        'pools_depth': 'poolsDepth',
        'rune_price_usd': 'runePriceUSD',
        'start_time': 'startTime',
        'total_value_bonded': 'totalValueBonded',
        'total_value_locked': 'totalValueLocked',
        'total_value_pooled': 'totalValuePooled'
    }

    def __init__(self, end_time=None, pools_depth=None, rune_price_usd=None, start_time=None, total_value_bonded=None, total_value_locked=None, total_value_pooled=None):  # noqa: E501
        """TVLHistoryItem - a model defined in Swagger"""  # noqa: E501
        self._end_time = None
        self._pools_depth = None
        self._rune_price_usd = None
        self._start_time = None
        self._total_value_bonded = None
        self._total_value_locked = None
        self._total_value_pooled = None
        self.discriminator = None
        self.end_time = end_time
        self.pools_depth = pools_depth
        self.rune_price_usd = rune_price_usd
        self.start_time = start_time
        if total_value_bonded is not None:
            self.total_value_bonded = total_value_bonded
        if total_value_locked is not None:
            self.total_value_locked = total_value_locked
        self.total_value_pooled = total_value_pooled

    @property
    def end_time(self):
        """Gets the end_time of this TVLHistoryItem.  # noqa: E501

        Int64, The end time of bucket in unix timestamp  # noqa: E501

        :return: The end_time of this TVLHistoryItem.  # noqa: E501
        :rtype: str
        """
        return self._end_time

    @end_time.setter
    def end_time(self, end_time):
        """Sets the end_time of this TVLHistoryItem.

        Int64, The end time of bucket in unix timestamp  # noqa: E501

        :param end_time: The end_time of this TVLHistoryItem.  # noqa: E501
        :type: str
        """
        if end_time is None:
            raise ValueError("Invalid value for `end_time`, must not be `None`")  # noqa: E501

        self._end_time = end_time

    @property
    def pools_depth(self):
        """Gets the pools_depth of this TVLHistoryItem.  # noqa: E501


        :return: The pools_depth of this TVLHistoryItem.  # noqa: E501
        :rtype: list[DepthHistoryItemPool]
        """
        return self._pools_depth

    @pools_depth.setter
    def pools_depth(self, pools_depth):
        """Sets the pools_depth of this TVLHistoryItem.


        :param pools_depth: The pools_depth of this TVLHistoryItem.  # noqa: E501
        :type: list[DepthHistoryItemPool]
        """
        if pools_depth is None:
            raise ValueError("Invalid value for `pools_depth`, must not be `None`")  # noqa: E501

        self._pools_depth = pools_depth

    @property
    def rune_price_usd(self):
        """Gets the rune_price_usd of this TVLHistoryItem.  # noqa: E501

        Float, the price of Rune based on the deepest USD pool at the end of the interval.   # noqa: E501

        :return: The rune_price_usd of this TVLHistoryItem.  # noqa: E501
        :rtype: str
        """
        return self._rune_price_usd

    @rune_price_usd.setter
    def rune_price_usd(self, rune_price_usd):
        """Sets the rune_price_usd of this TVLHistoryItem.

        Float, the price of Rune based on the deepest USD pool at the end of the interval.   # noqa: E501

        :param rune_price_usd: The rune_price_usd of this TVLHistoryItem.  # noqa: E501
        :type: str
        """
        if rune_price_usd is None:
            raise ValueError("Invalid value for `rune_price_usd`, must not be `None`")  # noqa: E501

        self._rune_price_usd = rune_price_usd

    @property
    def start_time(self):
        """Gets the start_time of this TVLHistoryItem.  # noqa: E501

        Int64, The beginning time of bucket in unix timestamp  # noqa: E501

        :return: The start_time of this TVLHistoryItem.  # noqa: E501
        :rtype: str
        """
        return self._start_time

    @start_time.setter
    def start_time(self, start_time):
        """Sets the start_time of this TVLHistoryItem.

        Int64, The beginning time of bucket in unix timestamp  # noqa: E501

        :param start_time: The start_time of this TVLHistoryItem.  # noqa: E501
        :type: str
        """
        if start_time is None:
            raise ValueError("Invalid value for `start_time`, must not be `None`")  # noqa: E501

        self._start_time = start_time

    @property
    def total_value_bonded(self):
        """Gets the total_value_bonded of this TVLHistoryItem.  # noqa: E501

        Int64(e8), the total amount of bonds (both active and standby) at the end of the interval   # noqa: E501

        :return: The total_value_bonded of this TVLHistoryItem.  # noqa: E501
        :rtype: str
        """
        return self._total_value_bonded

    @total_value_bonded.setter
    def total_value_bonded(self, total_value_bonded):
        """Sets the total_value_bonded of this TVLHistoryItem.

        Int64(e8), the total amount of bonds (both active and standby) at the end of the interval   # noqa: E501

        :param total_value_bonded: The total_value_bonded of this TVLHistoryItem.  # noqa: E501
        :type: str
        """

        self._total_value_bonded = total_value_bonded

    @property
    def total_value_locked(self):
        """Gets the total_value_locked of this TVLHistoryItem.  # noqa: E501

        Int64(e8), total value locked in the chain (in rune) This equals `totalPooledValue + totalBondedValue`, as it combines the liquidity pools and bonds of the nodes.   # noqa: E501

        :return: The total_value_locked of this TVLHistoryItem.  # noqa: E501
        :rtype: str
        """
        return self._total_value_locked

    @total_value_locked.setter
    def total_value_locked(self, total_value_locked):
        """Sets the total_value_locked of this TVLHistoryItem.

        Int64(e8), total value locked in the chain (in rune) This equals `totalPooledValue + totalBondedValue`, as it combines the liquidity pools and bonds of the nodes.   # noqa: E501

        :param total_value_locked: The total_value_locked of this TVLHistoryItem.  # noqa: E501
        :type: str
        """

        self._total_value_locked = total_value_locked

    @property
    def total_value_pooled(self):
        """Gets the total_value_pooled of this TVLHistoryItem.  # noqa: E501

        Int64(e8) in rune, the total pooled value (both assets and rune) in all of the pools at the end of the interval. Note: this is twice the aggregate Rune depth of all pools.   # noqa: E501

        :return: The total_value_pooled of this TVLHistoryItem.  # noqa: E501
        :rtype: str
        """
        return self._total_value_pooled

    @total_value_pooled.setter
    def total_value_pooled(self, total_value_pooled):
        """Sets the total_value_pooled of this TVLHistoryItem.

        Int64(e8) in rune, the total pooled value (both assets and rune) in all of the pools at the end of the interval. Note: this is twice the aggregate Rune depth of all pools.   # noqa: E501

        :param total_value_pooled: The total_value_pooled of this TVLHistoryItem.  # noqa: E501
        :type: str
        """
        if total_value_pooled is None:
            raise ValueError("Invalid value for `total_value_pooled`, must not be `None`")  # noqa: E501

        self._total_value_pooled = total_value_pooled

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
        if issubclass(TVLHistoryItem, dict):
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
        if not isinstance(other, TVLHistoryItem):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other

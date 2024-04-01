# coding: utf-8

"""
    Midgard Public API

    The Midgard Public API queries THORChain and any chains linked via the Bifröst and prepares information about the network to be readily available for public users. The API parses transaction event data from THORChain and stores them in a time-series database to make time-dependent queries easy. Midgard does not hold critical information. To interact with THORChain protocol, users should query THORNode directly.  # noqa: E501

    OpenAPI spec version: 2.20.1
    Contact: devs@thorchain.org
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

import pprint
import re  # noqa: F401

import six

class SaversHistoryItem(object):
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
        'savers_count': 'str',
        'savers_depth': 'str',
        'savers_units': 'str',
        'start_time': 'str'
    }

    attribute_map = {
        'end_time': 'endTime',
        'savers_count': 'saversCount',
        'savers_depth': 'saversDepth',
        'savers_units': 'saversUnits',
        'start_time': 'startTime'
    }

    def __init__(self, end_time=None, savers_count=None, savers_depth=None, savers_units=None, start_time=None):  # noqa: E501
        """SaversHistoryItem - a model defined in Swagger"""  # noqa: E501
        self._end_time = None
        self._savers_count = None
        self._savers_depth = None
        self._savers_units = None
        self._start_time = None
        self.discriminator = None
        self.end_time = end_time
        self.savers_count = savers_count
        self.savers_depth = savers_depth
        self.savers_units = savers_units
        self.start_time = start_time

    @property
    def end_time(self):
        """Gets the end_time of this SaversHistoryItem.  # noqa: E501

        Int64, The end time of bucket in unix timestamp  # noqa: E501

        :return: The end_time of this SaversHistoryItem.  # noqa: E501
        :rtype: str
        """
        return self._end_time

    @end_time.setter
    def end_time(self, end_time):
        """Sets the end_time of this SaversHistoryItem.

        Int64, The end time of bucket in unix timestamp  # noqa: E501

        :param end_time: The end_time of this SaversHistoryItem.  # noqa: E501
        :type: str
        """
        if end_time is None:
            raise ValueError("Invalid value for `end_time`, must not be `None`")  # noqa: E501

        self._end_time = end_time

    @property
    def savers_count(self):
        """Gets the savers_count of this SaversHistoryItem.  # noqa: E501

        Int64, Number of saver members in the pool at the end of the interval  # noqa: E501

        :return: The savers_count of this SaversHistoryItem.  # noqa: E501
        :rtype: str
        """
        return self._savers_count

    @savers_count.setter
    def savers_count(self, savers_count):
        """Sets the savers_count of this SaversHistoryItem.

        Int64, Number of saver members in the pool at the end of the interval  # noqa: E501

        :param savers_count: The savers_count of this SaversHistoryItem.  # noqa: E501
        :type: str
        """
        if savers_count is None:
            raise ValueError("Invalid value for `savers_count`, must not be `None`")  # noqa: E501

        self._savers_count = savers_count

    @property
    def savers_depth(self):
        """Gets the savers_depth of this SaversHistoryItem.  # noqa: E501

        Int64(e8), The depth in the savers vault at the end of the interval  # noqa: E501

        :return: The savers_depth of this SaversHistoryItem.  # noqa: E501
        :rtype: str
        """
        return self._savers_depth

    @savers_depth.setter
    def savers_depth(self, savers_depth):
        """Sets the savers_depth of this SaversHistoryItem.

        Int64(e8), The depth in the savers vault at the end of the interval  # noqa: E501

        :param savers_depth: The savers_depth of this SaversHistoryItem.  # noqa: E501
        :type: str
        """
        if savers_depth is None:
            raise ValueError("Invalid value for `savers_depth`, must not be `None`")  # noqa: E501

        self._savers_depth = savers_depth

    @property
    def savers_units(self):
        """Gets the savers_units of this SaversHistoryItem.  # noqa: E501

        Int64, Savers Units in the saver vault at the end of the interval   # noqa: E501

        :return: The savers_units of this SaversHistoryItem.  # noqa: E501
        :rtype: str
        """
        return self._savers_units

    @savers_units.setter
    def savers_units(self, savers_units):
        """Sets the savers_units of this SaversHistoryItem.

        Int64, Savers Units in the saver vault at the end of the interval   # noqa: E501

        :param savers_units: The savers_units of this SaversHistoryItem.  # noqa: E501
        :type: str
        """
        if savers_units is None:
            raise ValueError("Invalid value for `savers_units`, must not be `None`")  # noqa: E501

        self._savers_units = savers_units

    @property
    def start_time(self):
        """Gets the start_time of this SaversHistoryItem.  # noqa: E501

        Int64, The beginning time of bucket in unix timestamp  # noqa: E501

        :return: The start_time of this SaversHistoryItem.  # noqa: E501
        :rtype: str
        """
        return self._start_time

    @start_time.setter
    def start_time(self, start_time):
        """Sets the start_time of this SaversHistoryItem.

        Int64, The beginning time of bucket in unix timestamp  # noqa: E501

        :param start_time: The start_time of this SaversHistoryItem.  # noqa: E501
        :type: str
        """
        if start_time is None:
            raise ValueError("Invalid value for `start_time`, must not be `None`")  # noqa: E501

        self._start_time = start_time

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
        if issubclass(SaversHistoryItem, dict):
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
        if not isinstance(other, SaversHistoryItem):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other

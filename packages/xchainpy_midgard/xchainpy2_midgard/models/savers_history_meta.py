# coding: utf-8

"""
    Midgard Public API

    The Midgard Public API queries THORChain and any chains linked via the Bifröst and prepares information about the network to be readily available for public users. The API parses transaction event data from THORChain and stores them in a time-series database to make time-dependent queries easy. Midgard does not hold critical information. To interact with THORChain protocol, users should query THORNode directly.  # noqa: E501

    OpenAPI spec version: 2.24.3
    Contact: devs@thorchain.org
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

import pprint
import re  # noqa: F401

import six

class SaversHistoryMeta(object):
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
        'end_savers_count': 'str',
        'end_savers_depth': 'str',
        'end_time': 'str',
        'end_units': 'str',
        'start_savers_count': 'str',
        'start_savers_depth': 'str',
        'start_time': 'str',
        'start_units': 'str'
    }

    attribute_map = {
        'end_savers_count': 'endSaversCount',
        'end_savers_depth': 'endSaversDepth',
        'end_time': 'endTime',
        'end_units': 'endUnits',
        'start_savers_count': 'startSaversCount',
        'start_savers_depth': 'startSaversDepth',
        'start_time': 'startTime',
        'start_units': 'startUnits'
    }

    def __init__(self, end_savers_count=None, end_savers_depth=None, end_time=None, end_units=None, start_savers_count=None, start_savers_depth=None, start_time=None, start_units=None):  # noqa: E501
        """SaversHistoryMeta - a model defined in Swagger"""  # noqa: E501
        self._end_savers_count = None
        self._end_savers_depth = None
        self._end_time = None
        self._end_units = None
        self._start_savers_count = None
        self._start_savers_depth = None
        self._start_time = None
        self._start_units = None
        self.discriminator = None
        self.end_savers_count = end_savers_count
        self.end_savers_depth = end_savers_depth
        self.end_time = end_time
        self.end_units = end_units
        self.start_savers_count = start_savers_count
        self.start_savers_depth = start_savers_depth
        self.start_time = start_time
        self.start_units = start_units

    @property
    def end_savers_count(self):
        """Gets the end_savers_count of this SaversHistoryMeta.  # noqa: E501

        Int64, Number of savers member in the savers vault at the end of the interval at time endTime  # noqa: E501

        :return: The end_savers_count of this SaversHistoryMeta.  # noqa: E501
        :rtype: str
        """
        return self._end_savers_count

    @end_savers_count.setter
    def end_savers_count(self, end_savers_count):
        """Sets the end_savers_count of this SaversHistoryMeta.

        Int64, Number of savers member in the savers vault at the end of the interval at time endTime  # noqa: E501

        :param end_savers_count: The end_savers_count of this SaversHistoryMeta.  # noqa: E501
        :type: str
        """
        if end_savers_count is None:
            raise ValueError("Invalid value for `end_savers_count`, must not be `None`")  # noqa: E501

        self._end_savers_count = end_savers_count

    @property
    def end_savers_depth(self):
        """Gets the end_savers_depth of this SaversHistoryMeta.  # noqa: E501

        Int64(e8), The depth in the savers vault at the end of the interval at time endTime   # noqa: E501

        :return: The end_savers_depth of this SaversHistoryMeta.  # noqa: E501
        :rtype: str
        """
        return self._end_savers_depth

    @end_savers_depth.setter
    def end_savers_depth(self, end_savers_depth):
        """Sets the end_savers_depth of this SaversHistoryMeta.

        Int64(e8), The depth in the savers vault at the end of the interval at time endTime   # noqa: E501

        :param end_savers_depth: The end_savers_depth of this SaversHistoryMeta.  # noqa: E501
        :type: str
        """
        if end_savers_depth is None:
            raise ValueError("Invalid value for `end_savers_depth`, must not be `None`")  # noqa: E501

        self._end_savers_depth = end_savers_depth

    @property
    def end_time(self):
        """Gets the end_time of this SaversHistoryMeta.  # noqa: E501

        Int64, The end time of bucket in unix timestamp  # noqa: E501

        :return: The end_time of this SaversHistoryMeta.  # noqa: E501
        :rtype: str
        """
        return self._end_time

    @end_time.setter
    def end_time(self, end_time):
        """Sets the end_time of this SaversHistoryMeta.

        Int64, The end time of bucket in unix timestamp  # noqa: E501

        :param end_time: The end_time of this SaversHistoryMeta.  # noqa: E501
        :type: str
        """
        if end_time is None:
            raise ValueError("Invalid value for `end_time`, must not be `None`")  # noqa: E501

        self._end_time = end_time

    @property
    def end_units(self):
        """Gets the end_units of this SaversHistoryMeta.  # noqa: E501

        Int64, Savers Units in the savers vault at the end of the interval at time endTime  # noqa: E501

        :return: The end_units of this SaversHistoryMeta.  # noqa: E501
        :rtype: str
        """
        return self._end_units

    @end_units.setter
    def end_units(self, end_units):
        """Sets the end_units of this SaversHistoryMeta.

        Int64, Savers Units in the savers vault at the end of the interval at time endTime  # noqa: E501

        :param end_units: The end_units of this SaversHistoryMeta.  # noqa: E501
        :type: str
        """
        if end_units is None:
            raise ValueError("Invalid value for `end_units`, must not be `None`")  # noqa: E501

        self._end_units = end_units

    @property
    def start_savers_count(self):
        """Gets the start_savers_count of this SaversHistoryMeta.  # noqa: E501

        Int64, Number of savers member in the savers vault at the start of the interval at time startTime   # noqa: E501

        :return: The start_savers_count of this SaversHistoryMeta.  # noqa: E501
        :rtype: str
        """
        return self._start_savers_count

    @start_savers_count.setter
    def start_savers_count(self, start_savers_count):
        """Sets the start_savers_count of this SaversHistoryMeta.

        Int64, Number of savers member in the savers vault at the start of the interval at time startTime   # noqa: E501

        :param start_savers_count: The start_savers_count of this SaversHistoryMeta.  # noqa: E501
        :type: str
        """
        if start_savers_count is None:
            raise ValueError("Invalid value for `start_savers_count`, must not be `None`")  # noqa: E501

        self._start_savers_count = start_savers_count

    @property
    def start_savers_depth(self):
        """Gets the start_savers_depth of this SaversHistoryMeta.  # noqa: E501

        Int64(e8), The depth in savers vault at the start of the interval at time startTime   # noqa: E501

        :return: The start_savers_depth of this SaversHistoryMeta.  # noqa: E501
        :rtype: str
        """
        return self._start_savers_depth

    @start_savers_depth.setter
    def start_savers_depth(self, start_savers_depth):
        """Sets the start_savers_depth of this SaversHistoryMeta.

        Int64(e8), The depth in savers vault at the start of the interval at time startTime   # noqa: E501

        :param start_savers_depth: The start_savers_depth of this SaversHistoryMeta.  # noqa: E501
        :type: str
        """
        if start_savers_depth is None:
            raise ValueError("Invalid value for `start_savers_depth`, must not be `None`")  # noqa: E501

        self._start_savers_depth = start_savers_depth

    @property
    def start_time(self):
        """Gets the start_time of this SaversHistoryMeta.  # noqa: E501

        Int64, The beginning time of bucket in unix timestamp  # noqa: E501

        :return: The start_time of this SaversHistoryMeta.  # noqa: E501
        :rtype: str
        """
        return self._start_time

    @start_time.setter
    def start_time(self, start_time):
        """Sets the start_time of this SaversHistoryMeta.

        Int64, The beginning time of bucket in unix timestamp  # noqa: E501

        :param start_time: The start_time of this SaversHistoryMeta.  # noqa: E501
        :type: str
        """
        if start_time is None:
            raise ValueError("Invalid value for `start_time`, must not be `None`")  # noqa: E501

        self._start_time = start_time

    @property
    def start_units(self):
        """Gets the start_units of this SaversHistoryMeta.  # noqa: E501

        Int64, Savers Units in the savers vault at the start of the interval at time startTime   # noqa: E501

        :return: The start_units of this SaversHistoryMeta.  # noqa: E501
        :rtype: str
        """
        return self._start_units

    @start_units.setter
    def start_units(self, start_units):
        """Sets the start_units of this SaversHistoryMeta.

        Int64, Savers Units in the savers vault at the start of the interval at time startTime   # noqa: E501

        :param start_units: The start_units of this SaversHistoryMeta.  # noqa: E501
        :type: str
        """
        if start_units is None:
            raise ValueError("Invalid value for `start_units`, must not be `None`")  # noqa: E501

        self._start_units = start_units

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
        if issubclass(SaversHistoryMeta, dict):
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
        if not isinstance(other, SaversHistoryMeta):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other

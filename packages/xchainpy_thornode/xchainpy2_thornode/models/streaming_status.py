# coding: utf-8

"""
    Thornode API

    Thornode REST API.  # noqa: E501

    OpenAPI spec version: 3.0.0
    Contact: devs@thorchain.org
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

import pprint
import re  # noqa: F401

import six

class StreamingStatus(object):
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
        'interval': 'int',
        'quantity': 'int',
        'count': 'int'
    }

    attribute_map = {
        'interval': 'interval',
        'quantity': 'quantity',
        'count': 'count'
    }

    def __init__(self, interval=None, quantity=None, count=None):  # noqa: E501
        """StreamingStatus - a model defined in Swagger"""  # noqa: E501
        self._interval = None
        self._quantity = None
        self._count = None
        self.discriminator = None
        self.interval = interval
        self.quantity = quantity
        self.count = count

    @property
    def interval(self):
        """Gets the interval of this StreamingStatus.  # noqa: E501

        how often each swap is made, in blocks  # noqa: E501

        :return: The interval of this StreamingStatus.  # noqa: E501
        :rtype: int
        """
        return self._interval

    @interval.setter
    def interval(self, interval):
        """Sets the interval of this StreamingStatus.

        how often each swap is made, in blocks  # noqa: E501

        :param interval: The interval of this StreamingStatus.  # noqa: E501
        :type: int
        """
        if interval is None:
            raise ValueError("Invalid value for `interval`, must not be `None`")  # noqa: E501

        self._interval = interval

    @property
    def quantity(self):
        """Gets the quantity of this StreamingStatus.  # noqa: E501

        the total number of swaps in a streaming swaps  # noqa: E501

        :return: The quantity of this StreamingStatus.  # noqa: E501
        :rtype: int
        """
        return self._quantity

    @quantity.setter
    def quantity(self, quantity):
        """Sets the quantity of this StreamingStatus.

        the total number of swaps in a streaming swaps  # noqa: E501

        :param quantity: The quantity of this StreamingStatus.  # noqa: E501
        :type: int
        """
        if quantity is None:
            raise ValueError("Invalid value for `quantity`, must not be `None`")  # noqa: E501

        self._quantity = quantity

    @property
    def count(self):
        """Gets the count of this StreamingStatus.  # noqa: E501

        the amount of swap attempts so far  # noqa: E501

        :return: The count of this StreamingStatus.  # noqa: E501
        :rtype: int
        """
        return self._count

    @count.setter
    def count(self, count):
        """Sets the count of this StreamingStatus.

        the amount of swap attempts so far  # noqa: E501

        :param count: The count of this StreamingStatus.  # noqa: E501
        :type: int
        """
        if count is None:
            raise ValueError("Invalid value for `count`, must not be `None`")  # noqa: E501

        self._count = count

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
        if issubclass(StreamingStatus, dict):
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
        if not isinstance(other, StreamingStatus):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other

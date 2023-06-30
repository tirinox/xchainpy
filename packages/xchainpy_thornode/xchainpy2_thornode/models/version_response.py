# coding: utf-8

"""
    Thornode API

    Thornode REST API.  # noqa: E501

    OpenAPI spec version: 1.114.0
    Contact: devs@thorchain.org
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

import pprint
import re  # noqa: F401

import six

class VersionResponse(object):
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
        'current': 'str',
        'next': 'str',
        'next_since_height': 'int',
        'querier': 'str'
    }

    attribute_map = {
        'current': 'current',
        'next': 'next',
        'next_since_height': 'next_since_height',
        'querier': 'querier'
    }

    def __init__(self, current=None, next=None, next_since_height=None, querier=None):  # noqa: E501
        """VersionResponse - a model defined in Swagger"""  # noqa: E501
        self._current = None
        self._next = None
        self._next_since_height = None
        self._querier = None
        self.discriminator = None
        self.current = current
        self.next = next
        if next_since_height is not None:
            self.next_since_height = next_since_height
        self.querier = querier

    @property
    def current(self):
        """Gets the current of this VersionResponse.  # noqa: E501

        current version  # noqa: E501

        :return: The current of this VersionResponse.  # noqa: E501
        :rtype: str
        """
        return self._current

    @current.setter
    def current(self, current):
        """Sets the current of this VersionResponse.

        current version  # noqa: E501

        :param current: The current of this VersionResponse.  # noqa: E501
        :type: str
        """
        if current is None:
            raise ValueError("Invalid value for `current`, must not be `None`")  # noqa: E501

        self._current = current

    @property
    def next(self):
        """Gets the next of this VersionResponse.  # noqa: E501

        next version (minimum version for a node to become Active)  # noqa: E501

        :return: The next of this VersionResponse.  # noqa: E501
        :rtype: str
        """
        return self._next

    @next.setter
    def next(self, next):
        """Sets the next of this VersionResponse.

        next version (minimum version for a node to become Active)  # noqa: E501

        :param next: The next of this VersionResponse.  # noqa: E501
        :type: str
        """
        if next is None:
            raise ValueError("Invalid value for `next`, must not be `None`")  # noqa: E501

        self._next = next

    @property
    def next_since_height(self):
        """Gets the next_since_height of this VersionResponse.  # noqa: E501

        height at which the minimum joining version last changed  # noqa: E501

        :return: The next_since_height of this VersionResponse.  # noqa: E501
        :rtype: int
        """
        return self._next_since_height

    @next_since_height.setter
    def next_since_height(self, next_since_height):
        """Sets the next_since_height of this VersionResponse.

        height at which the minimum joining version last changed  # noqa: E501

        :param next_since_height: The next_since_height of this VersionResponse.  # noqa: E501
        :type: int
        """

        self._next_since_height = next_since_height

    @property
    def querier(self):
        """Gets the querier of this VersionResponse.  # noqa: E501

        querier version  # noqa: E501

        :return: The querier of this VersionResponse.  # noqa: E501
        :rtype: str
        """
        return self._querier

    @querier.setter
    def querier(self, querier):
        """Sets the querier of this VersionResponse.

        querier version  # noqa: E501

        :param querier: The querier of this VersionResponse.  # noqa: E501
        :type: str
        """
        if querier is None:
            raise ValueError("Invalid value for `querier`, must not be `None`")  # noqa: E501

        self._querier = querier

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
        if issubclass(VersionResponse, dict):
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
        if not isinstance(other, VersionResponse):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other

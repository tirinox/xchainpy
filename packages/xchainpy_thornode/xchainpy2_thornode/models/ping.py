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

class Ping(object):
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
        'ping': 'str'
    }

    attribute_map = {
        'ping': 'ping'
    }

    def __init__(self, ping=None):  # noqa: E501
        """Ping - a model defined in Swagger"""  # noqa: E501
        self._ping = None
        self.discriminator = None
        if ping is not None:
            self.ping = ping

    @property
    def ping(self):
        """Gets the ping of this Ping.  # noqa: E501


        :return: The ping of this Ping.  # noqa: E501
        :rtype: str
        """
        return self._ping

    @ping.setter
    def ping(self, ping):
        """Sets the ping of this Ping.


        :param ping: The ping of this Ping.  # noqa: E501
        :type: str
        """

        self._ping = ping

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
        if issubclass(Ping, dict):
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
        if not isinstance(other, Ping):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other

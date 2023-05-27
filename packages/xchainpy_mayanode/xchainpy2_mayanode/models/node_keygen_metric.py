# coding: utf-8

"""
    Mayanode API

    Mayanode REST API.  # noqa: E501

    OpenAPI spec version: 1.104.0
    Contact: devs@mayachain.org
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

import pprint
import re  # noqa: F401

import six

class NodeKeygenMetric(object):
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
        'address': 'str',
        'tss_time': 'str'
    }

    attribute_map = {
        'address': 'address',
        'tss_time': 'tss_time'
    }

    def __init__(self, address=None, tss_time=None):  # noqa: E501
        """NodeKeygenMetric - a model defined in Swagger"""  # noqa: E501
        self._address = None
        self._tss_time = None
        self.discriminator = None
        if address is not None:
            self.address = address
        if tss_time is not None:
            self.tss_time = tss_time

    @property
    def address(self):
        """Gets the address of this NodeKeygenMetric.  # noqa: E501


        :return: The address of this NodeKeygenMetric.  # noqa: E501
        :rtype: str
        """
        return self._address

    @address.setter
    def address(self, address):
        """Sets the address of this NodeKeygenMetric.


        :param address: The address of this NodeKeygenMetric.  # noqa: E501
        :type: str
        """

        self._address = address

    @property
    def tss_time(self):
        """Gets the tss_time of this NodeKeygenMetric.  # noqa: E501


        :return: The tss_time of this NodeKeygenMetric.  # noqa: E501
        :rtype: str
        """
        return self._tss_time

    @tss_time.setter
    def tss_time(self, tss_time):
        """Sets the tss_time of this NodeKeygenMetric.


        :param tss_time: The tss_time of this NodeKeygenMetric.  # noqa: E501
        :type: str
        """

        self._tss_time = tss_time

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
        if issubclass(NodeKeygenMetric, dict):
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
        if not isinstance(other, NodeKeygenMetric):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other

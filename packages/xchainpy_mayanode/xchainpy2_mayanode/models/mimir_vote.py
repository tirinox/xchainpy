# coding: utf-8

"""
    Mayanode API

    Mayanode REST API.  # noqa: E501

    OpenAPI spec version: 1.106.1
    Contact: devs@mayachain.org
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

import pprint
import re  # noqa: F401

import six

class MimirVote(object):
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
        'key': 'str',
        'value': 'int',
        'signer': 'str'
    }

    attribute_map = {
        'key': 'key',
        'value': 'value',
        'signer': 'signer'
    }

    def __init__(self, key=None, value=None, signer=None):  # noqa: E501
        """MimirVote - a model defined in Swagger"""  # noqa: E501
        self._key = None
        self._value = None
        self._signer = None
        self.discriminator = None
        if key is not None:
            self.key = key
        if value is not None:
            self.value = value
        if signer is not None:
            self.signer = signer

    @property
    def key(self):
        """Gets the key of this MimirVote.  # noqa: E501


        :return: The key of this MimirVote.  # noqa: E501
        :rtype: str
        """
        return self._key

    @key.setter
    def key(self, key):
        """Sets the key of this MimirVote.


        :param key: The key of this MimirVote.  # noqa: E501
        :type: str
        """

        self._key = key

    @property
    def value(self):
        """Gets the value of this MimirVote.  # noqa: E501


        :return: The value of this MimirVote.  # noqa: E501
        :rtype: int
        """
        return self._value

    @value.setter
    def value(self, value):
        """Sets the value of this MimirVote.


        :param value: The value of this MimirVote.  # noqa: E501
        :type: int
        """

        self._value = value

    @property
    def signer(self):
        """Gets the signer of this MimirVote.  # noqa: E501


        :return: The signer of this MimirVote.  # noqa: E501
        :rtype: str
        """
        return self._signer

    @signer.setter
    def signer(self, signer):
        """Sets the signer of this MimirVote.


        :param signer: The signer of this MimirVote.  # noqa: E501
        :type: str
        """

        self._signer = signer

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
        if issubclass(MimirVote, dict):
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
        if not isinstance(other, MimirVote):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other

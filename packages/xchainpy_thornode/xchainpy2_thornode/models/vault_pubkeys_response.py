# coding: utf-8

"""
    Thornode API

    Thornode REST API.  # noqa: E501

    OpenAPI spec version: 1.127.0
    Contact: devs@thorchain.org
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

import pprint
import re  # noqa: F401

import six

class VaultPubkeysResponse(object):
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
        'asgard': 'list[VaultInfo]',
        'yggdrasil': 'list[VaultInfo]',
        'inactive': 'list[VaultInfo]'
    }

    attribute_map = {
        'asgard': 'asgard',
        'yggdrasil': 'yggdrasil',
        'inactive': 'inactive'
    }

    def __init__(self, asgard=None, yggdrasil=None, inactive=None):  # noqa: E501
        """VaultPubkeysResponse - a model defined in Swagger"""  # noqa: E501
        self._asgard = None
        self._yggdrasil = None
        self._inactive = None
        self.discriminator = None
        self.asgard = asgard
        self.yggdrasil = yggdrasil
        self.inactive = inactive

    @property
    def asgard(self):
        """Gets the asgard of this VaultPubkeysResponse.  # noqa: E501


        :return: The asgard of this VaultPubkeysResponse.  # noqa: E501
        :rtype: list[VaultInfo]
        """
        return self._asgard

    @asgard.setter
    def asgard(self, asgard):
        """Sets the asgard of this VaultPubkeysResponse.


        :param asgard: The asgard of this VaultPubkeysResponse.  # noqa: E501
        :type: list[VaultInfo]
        """
        if asgard is None:
            raise ValueError("Invalid value for `asgard`, must not be `None`")  # noqa: E501

        self._asgard = asgard

    @property
    def yggdrasil(self):
        """Gets the yggdrasil of this VaultPubkeysResponse.  # noqa: E501


        :return: The yggdrasil of this VaultPubkeysResponse.  # noqa: E501
        :rtype: list[VaultInfo]
        """
        return self._yggdrasil

    @yggdrasil.setter
    def yggdrasil(self, yggdrasil):
        """Sets the yggdrasil of this VaultPubkeysResponse.


        :param yggdrasil: The yggdrasil of this VaultPubkeysResponse.  # noqa: E501
        :type: list[VaultInfo]
        """
        if yggdrasil is None:
            raise ValueError("Invalid value for `yggdrasil`, must not be `None`")  # noqa: E501

        self._yggdrasil = yggdrasil

    @property
    def inactive(self):
        """Gets the inactive of this VaultPubkeysResponse.  # noqa: E501


        :return: The inactive of this VaultPubkeysResponse.  # noqa: E501
        :rtype: list[VaultInfo]
        """
        return self._inactive

    @inactive.setter
    def inactive(self, inactive):
        """Sets the inactive of this VaultPubkeysResponse.


        :param inactive: The inactive of this VaultPubkeysResponse.  # noqa: E501
        :type: list[VaultInfo]
        """
        if inactive is None:
            raise ValueError("Invalid value for `inactive`, must not be `None`")  # noqa: E501

        self._inactive = inactive

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
        if issubclass(VaultPubkeysResponse, dict):
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
        if not isinstance(other, VaultPubkeysResponse):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other

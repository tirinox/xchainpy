# coding: utf-8

"""
    Mayanode API

    Mayanode REST API.  # noqa: E501

    OpenAPI spec version: 1.109.0
    Contact: devs@mayachain.org
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

import pprint
import re  # noqa: F401

import six

class NodeBondProvider(object):
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
        'bond_address': 'str',
        'bond': 'str'
    }

    attribute_map = {
        'bond_address': 'bond_address',
        'bond': 'bond'
    }

    def __init__(self, bond_address=None, bond=None):  # noqa: E501
        """NodeBondProvider - a model defined in Swagger"""  # noqa: E501
        self._bond_address = None
        self._bond = None
        self.discriminator = None
        if bond_address is not None:
            self.bond_address = bond_address
        if bond is not None:
            self.bond = bond

    @property
    def bond_address(self):
        """Gets the bond_address of this NodeBondProvider.  # noqa: E501


        :return: The bond_address of this NodeBondProvider.  # noqa: E501
        :rtype: str
        """
        return self._bond_address

    @bond_address.setter
    def bond_address(self, bond_address):
        """Sets the bond_address of this NodeBondProvider.


        :param bond_address: The bond_address of this NodeBondProvider.  # noqa: E501
        :type: str
        """

        self._bond_address = bond_address

    @property
    def bond(self):
        """Gets the bond of this NodeBondProvider.  # noqa: E501


        :return: The bond of this NodeBondProvider.  # noqa: E501
        :rtype: str
        """
        return self._bond

    @bond.setter
    def bond(self, bond):
        """Sets the bond of this NodeBondProvider.


        :param bond: The bond of this NodeBondProvider.  # noqa: E501
        :type: str
        """

        self._bond = bond

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
        if issubclass(NodeBondProvider, dict):
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
        if not isinstance(other, NodeBondProvider):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other

# coding: utf-8

"""
    Mayanode API

    Mayanode REST API.  # noqa: E501

    OpenAPI spec version: 1.107.1
    Contact: devs@mayachain.org
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

import pprint
import re  # noqa: F401

import six

class LPBondedNode(object):
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
        'node_address': 'str',
        'units': 'str'
    }

    attribute_map = {
        'node_address': 'node_address',
        'units': 'units'
    }

    def __init__(self, node_address=None, units=None):  # noqa: E501
        """LPBondedNode - a model defined in Swagger"""  # noqa: E501
        self._node_address = None
        self._units = None
        self.discriminator = None
        self.node_address = node_address
        self.units = units

    @property
    def node_address(self):
        """Gets the node_address of this LPBondedNode.  # noqa: E501


        :return: The node_address of this LPBondedNode.  # noqa: E501
        :rtype: str
        """
        return self._node_address

    @node_address.setter
    def node_address(self, node_address):
        """Sets the node_address of this LPBondedNode.


        :param node_address: The node_address of this LPBondedNode.  # noqa: E501
        :type: str
        """
        if node_address is None:
            raise ValueError("Invalid value for `node_address`, must not be `None`")  # noqa: E501

        self._node_address = node_address

    @property
    def units(self):
        """Gets the units of this LPBondedNode.  # noqa: E501


        :return: The units of this LPBondedNode.  # noqa: E501
        :rtype: str
        """
        return self._units

    @units.setter
    def units(self, units):
        """Sets the units of this LPBondedNode.


        :param units: The units of this LPBondedNode.  # noqa: E501
        :type: str
        """
        if units is None:
            raise ValueError("Invalid value for `units`, must not be `None`")  # noqa: E501

        self._units = units

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
        if issubclass(LPBondedNode, dict):
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
        if not isinstance(other, LPBondedNode):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other

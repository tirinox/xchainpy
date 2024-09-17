# coding: utf-8

"""
    Thornode API

    Thornode REST API.  # noqa: E501

    OpenAPI spec version: 2.135.0
    Contact: devs@thorchain.org
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

import pprint
import re  # noqa: F401

import six

class NodeBondProviders(object):
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
        'node_operator_fee': 'str',
        'providers': 'list[NodeBondProvider]'
    }

    attribute_map = {
        'node_operator_fee': 'node_operator_fee',
        'providers': 'providers'
    }

    def __init__(self, node_operator_fee=None, providers=None):  # noqa: E501
        """NodeBondProviders - a model defined in Swagger"""  # noqa: E501
        self._node_operator_fee = None
        self._providers = None
        self.discriminator = None
        self.node_operator_fee = node_operator_fee
        self.providers = providers

    @property
    def node_operator_fee(self):
        """Gets the node_operator_fee of this NodeBondProviders.  # noqa: E501

        node operator fee in basis points  # noqa: E501

        :return: The node_operator_fee of this NodeBondProviders.  # noqa: E501
        :rtype: str
        """
        return self._node_operator_fee

    @node_operator_fee.setter
    def node_operator_fee(self, node_operator_fee):
        """Sets the node_operator_fee of this NodeBondProviders.

        node operator fee in basis points  # noqa: E501

        :param node_operator_fee: The node_operator_fee of this NodeBondProviders.  # noqa: E501
        :type: str
        """
        if node_operator_fee is None:
            raise ValueError("Invalid value for `node_operator_fee`, must not be `None`")  # noqa: E501

        self._node_operator_fee = node_operator_fee

    @property
    def providers(self):
        """Gets the providers of this NodeBondProviders.  # noqa: E501

        all the bond providers for the node  # noqa: E501

        :return: The providers of this NodeBondProviders.  # noqa: E501
        :rtype: list[NodeBondProvider]
        """
        return self._providers

    @providers.setter
    def providers(self, providers):
        """Sets the providers of this NodeBondProviders.

        all the bond providers for the node  # noqa: E501

        :param providers: The providers of this NodeBondProviders.  # noqa: E501
        :type: list[NodeBondProvider]
        """
        if providers is None:
            raise ValueError("Invalid value for `providers`, must not be `None`")  # noqa: E501

        self._providers = providers

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
        if issubclass(NodeBondProviders, dict):
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
        if not isinstance(other, NodeBondProviders):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other

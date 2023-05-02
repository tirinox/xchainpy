# coding: utf-8

"""
    Mayanode API

    Mayanode REST API.  # noqa: E501

    OpenAPI spec version: 1.103.3
    Contact: devs@mayachain.org
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
        'node_address': 'str',
        'node_operator_fee': 'str',
        'providers': 'NodeBondProvider'
    }

    attribute_map = {
        'node_address': 'node_address',
        'node_operator_fee': 'node_operator_fee',
        'providers': 'providers'
    }

    def __init__(self, node_address=None, node_operator_fee=None, providers=None):  # noqa: E501
        """NodeBondProviders - a model defined in Swagger"""  # noqa: E501
        self._node_address = None
        self._node_operator_fee = None
        self._providers = None
        self.discriminator = None
        if node_address is not None:
            self.node_address = node_address
        if node_operator_fee is not None:
            self.node_operator_fee = node_operator_fee
        if providers is not None:
            self.providers = providers

    @property
    def node_address(self):
        """Gets the node_address of this NodeBondProviders.  # noqa: E501


        :return: The node_address of this NodeBondProviders.  # noqa: E501
        :rtype: str
        """
        return self._node_address

    @node_address.setter
    def node_address(self, node_address):
        """Sets the node_address of this NodeBondProviders.


        :param node_address: The node_address of this NodeBondProviders.  # noqa: E501
        :type: str
        """

        self._node_address = node_address

    @property
    def node_operator_fee(self):
        """Gets the node_operator_fee of this NodeBondProviders.  # noqa: E501


        :return: The node_operator_fee of this NodeBondProviders.  # noqa: E501
        :rtype: str
        """
        return self._node_operator_fee

    @node_operator_fee.setter
    def node_operator_fee(self, node_operator_fee):
        """Sets the node_operator_fee of this NodeBondProviders.


        :param node_operator_fee: The node_operator_fee of this NodeBondProviders.  # noqa: E501
        :type: str
        """

        self._node_operator_fee = node_operator_fee

    @property
    def providers(self):
        """Gets the providers of this NodeBondProviders.  # noqa: E501


        :return: The providers of this NodeBondProviders.  # noqa: E501
        :rtype: NodeBondProvider
        """
        return self._providers

    @providers.setter
    def providers(self, providers):
        """Sets the providers of this NodeBondProviders.


        :param providers: The providers of this NodeBondProviders.  # noqa: E501
        :type: NodeBondProvider
        """

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

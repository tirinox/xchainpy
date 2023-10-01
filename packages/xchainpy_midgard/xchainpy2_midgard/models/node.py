# coding: utf-8

"""
    Midgard Public API

    The Midgard Public API queries THORChain and any chains linked via the Bifröst and prepares information about the network to be readily available for public users. The API parses transaction event data from THORChain and stores them in a time-series database to make time-dependent queries easy. Midgard does not hold critical information. To interact with THORChain protocol, users should query THORNode directly.  # noqa: E501

    OpenAPI spec version: 2.17.0
    Contact: devs@thorchain.org
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

import pprint
import re  # noqa: F401

import six

class Node(object):
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
        'ed25519': 'str',
        'node_address': 'str',
        'secp256k1': 'str'
    }

    attribute_map = {
        'ed25519': 'ed25519',
        'node_address': 'nodeAddress',
        'secp256k1': 'secp256k1'
    }

    def __init__(self, ed25519=None, node_address=None, secp256k1=None):  # noqa: E501
        """Node - a model defined in Swagger"""  # noqa: E501
        self._ed25519 = None
        self._node_address = None
        self._secp256k1 = None
        self.discriminator = None
        self.ed25519 = ed25519
        self.node_address = node_address
        self.secp256k1 = secp256k1

    @property
    def ed25519(self):
        """Gets the ed25519 of this Node.  # noqa: E501

        ed25519 public key  # noqa: E501

        :return: The ed25519 of this Node.  # noqa: E501
        :rtype: str
        """
        return self._ed25519

    @ed25519.setter
    def ed25519(self, ed25519):
        """Sets the ed25519 of this Node.

        ed25519 public key  # noqa: E501

        :param ed25519: The ed25519 of this Node.  # noqa: E501
        :type: str
        """
        if ed25519 is None:
            raise ValueError("Invalid value for `ed25519`, must not be `None`")  # noqa: E501

        self._ed25519 = ed25519

    @property
    def node_address(self):
        """Gets the node_address of this Node.  # noqa: E501

        node thorchain address  # noqa: E501

        :return: The node_address of this Node.  # noqa: E501
        :rtype: str
        """
        return self._node_address

    @node_address.setter
    def node_address(self, node_address):
        """Sets the node_address of this Node.

        node thorchain address  # noqa: E501

        :param node_address: The node_address of this Node.  # noqa: E501
        :type: str
        """
        if node_address is None:
            raise ValueError("Invalid value for `node_address`, must not be `None`")  # noqa: E501

        self._node_address = node_address

    @property
    def secp256k1(self):
        """Gets the secp256k1 of this Node.  # noqa: E501

        secp256k1 public key  # noqa: E501

        :return: The secp256k1 of this Node.  # noqa: E501
        :rtype: str
        """
        return self._secp256k1

    @secp256k1.setter
    def secp256k1(self, secp256k1):
        """Sets the secp256k1 of this Node.

        secp256k1 public key  # noqa: E501

        :param secp256k1: The secp256k1 of this Node.  # noqa: E501
        :type: str
        """
        if secp256k1 is None:
            raise ValueError("Invalid value for `secp256k1`, must not be `None`")  # noqa: E501

        self._secp256k1 = secp256k1

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
        if issubclass(Node, dict):
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
        if not isinstance(other, Node):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other

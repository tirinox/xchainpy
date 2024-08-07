# coding: utf-8

"""
    Mayanode API

    Mayanode REST API.  # noqa: E501

    OpenAPI spec version: 1.110.0
    Contact: devs@mayachain.org
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

import pprint
import re  # noqa: F401

import six

class NodePubKeySet(object):
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
        'secp256k1': 'str',
        'ed25519': 'str'
    }

    attribute_map = {
        'secp256k1': 'secp256k1',
        'ed25519': 'ed25519'
    }

    def __init__(self, secp256k1=None, ed25519=None):  # noqa: E501
        """NodePubKeySet - a model defined in Swagger"""  # noqa: E501
        self._secp256k1 = None
        self._ed25519 = None
        self.discriminator = None
        if secp256k1 is not None:
            self.secp256k1 = secp256k1
        if ed25519 is not None:
            self.ed25519 = ed25519

    @property
    def secp256k1(self):
        """Gets the secp256k1 of this NodePubKeySet.  # noqa: E501


        :return: The secp256k1 of this NodePubKeySet.  # noqa: E501
        :rtype: str
        """
        return self._secp256k1

    @secp256k1.setter
    def secp256k1(self, secp256k1):
        """Sets the secp256k1 of this NodePubKeySet.


        :param secp256k1: The secp256k1 of this NodePubKeySet.  # noqa: E501
        :type: str
        """

        self._secp256k1 = secp256k1

    @property
    def ed25519(self):
        """Gets the ed25519 of this NodePubKeySet.  # noqa: E501


        :return: The ed25519 of this NodePubKeySet.  # noqa: E501
        :rtype: str
        """
        return self._ed25519

    @ed25519.setter
    def ed25519(self, ed25519):
        """Sets the ed25519 of this NodePubKeySet.


        :param ed25519: The ed25519 of this NodePubKeySet.  # noqa: E501
        :type: str
        """

        self._ed25519 = ed25519

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
        if issubclass(NodePubKeySet, dict):
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
        if not isinstance(other, NodePubKeySet):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other

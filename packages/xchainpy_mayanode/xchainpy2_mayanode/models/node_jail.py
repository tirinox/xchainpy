# coding: utf-8

"""
    Mayanode API

    Mayanode REST API.  # noqa: E501

    OpenAPI spec version: 1.108.1
    Contact: devs@mayachain.org
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

import pprint
import re  # noqa: F401

import six

class NodeJail(object):
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
        'release_height': 'int',
        'reason': 'str'
    }

    attribute_map = {
        'node_address': 'node_address',
        'release_height': 'release_height',
        'reason': 'reason'
    }

    def __init__(self, node_address=None, release_height=None, reason=None):  # noqa: E501
        """NodeJail - a model defined in Swagger"""  # noqa: E501
        self._node_address = None
        self._release_height = None
        self._reason = None
        self.discriminator = None
        if node_address is not None:
            self.node_address = node_address
        if release_height is not None:
            self.release_height = release_height
        if reason is not None:
            self.reason = reason

    @property
    def node_address(self):
        """Gets the node_address of this NodeJail.  # noqa: E501


        :return: The node_address of this NodeJail.  # noqa: E501
        :rtype: str
        """
        return self._node_address

    @node_address.setter
    def node_address(self, node_address):
        """Sets the node_address of this NodeJail.


        :param node_address: The node_address of this NodeJail.  # noqa: E501
        :type: str
        """

        self._node_address = node_address

    @property
    def release_height(self):
        """Gets the release_height of this NodeJail.  # noqa: E501


        :return: The release_height of this NodeJail.  # noqa: E501
        :rtype: int
        """
        return self._release_height

    @release_height.setter
    def release_height(self, release_height):
        """Sets the release_height of this NodeJail.


        :param release_height: The release_height of this NodeJail.  # noqa: E501
        :type: int
        """

        self._release_height = release_height

    @property
    def reason(self):
        """Gets the reason of this NodeJail.  # noqa: E501


        :return: The reason of this NodeJail.  # noqa: E501
        :rtype: str
        """
        return self._reason

    @reason.setter
    def reason(self, reason):
        """Sets the reason of this NodeJail.


        :param reason: The reason of this NodeJail.  # noqa: E501
        :type: str
        """

        self._reason = reason

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
        if issubclass(NodeJail, dict):
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
        if not isinstance(other, NodeJail):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other

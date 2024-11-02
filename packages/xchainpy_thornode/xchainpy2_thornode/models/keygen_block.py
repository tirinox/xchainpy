# coding: utf-8

"""
    Thornode API

    Thornode REST API.  # noqa: E501

    OpenAPI spec version: 2.137.1
    Contact: devs@thorchain.org
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

import pprint
import re  # noqa: F401

import six

class KeygenBlock(object):
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
        'height': 'int',
        'keygens': 'list[Keygen]'
    }

    attribute_map = {
        'height': 'height',
        'keygens': 'keygens'
    }

    def __init__(self, height=None, keygens=None):  # noqa: E501
        """KeygenBlock - a model defined in Swagger"""  # noqa: E501
        self._height = None
        self._keygens = None
        self.discriminator = None
        if height is not None:
            self.height = height
        self.keygens = keygens

    @property
    def height(self):
        """Gets the height of this KeygenBlock.  # noqa: E501

        the height of the keygen block  # noqa: E501

        :return: The height of this KeygenBlock.  # noqa: E501
        :rtype: int
        """
        return self._height

    @height.setter
    def height(self, height):
        """Sets the height of this KeygenBlock.

        the height of the keygen block  # noqa: E501

        :param height: The height of this KeygenBlock.  # noqa: E501
        :type: int
        """

        self._height = height

    @property
    def keygens(self):
        """Gets the keygens of this KeygenBlock.  # noqa: E501


        :return: The keygens of this KeygenBlock.  # noqa: E501
        :rtype: list[Keygen]
        """
        return self._keygens

    @keygens.setter
    def keygens(self, keygens):
        """Sets the keygens of this KeygenBlock.


        :param keygens: The keygens of this KeygenBlock.  # noqa: E501
        :type: list[Keygen]
        """
        if keygens is None:
            raise ValueError("Invalid value for `keygens`, must not be `None`")  # noqa: E501

        self._keygens = keygens

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
        if issubclass(KeygenBlock, dict):
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
        if not isinstance(other, KeygenBlock):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other

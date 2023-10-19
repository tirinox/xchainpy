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

class Mayaname1(object):
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
        'name': 'str',
        'chain': 'str',
        'address': 'str',
        'expire_block_height': 'int'
    }

    attribute_map = {
        'name': 'name',
        'chain': 'chain',
        'address': 'address',
        'expire_block_height': 'expire_block_height'
    }

    def __init__(self, name=None, chain=None, address=None, expire_block_height=None):  # noqa: E501
        """Mayaname1 - a model defined in Swagger"""  # noqa: E501
        self._name = None
        self._chain = None
        self._address = None
        self._expire_block_height = None
        self.discriminator = None
        if name is not None:
            self.name = name
        if chain is not None:
            self.chain = chain
        if address is not None:
            self.address = address
        if expire_block_height is not None:
            self.expire_block_height = expire_block_height

    @property
    def name(self):
        """Gets the name of this Mayaname1.  # noqa: E501


        :return: The name of this Mayaname1.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this Mayaname1.


        :param name: The name of this Mayaname1.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def chain(self):
        """Gets the chain of this Mayaname1.  # noqa: E501


        :return: The chain of this Mayaname1.  # noqa: E501
        :rtype: str
        """
        return self._chain

    @chain.setter
    def chain(self, chain):
        """Sets the chain of this Mayaname1.


        :param chain: The chain of this Mayaname1.  # noqa: E501
        :type: str
        """

        self._chain = chain

    @property
    def address(self):
        """Gets the address of this Mayaname1.  # noqa: E501


        :return: The address of this Mayaname1.  # noqa: E501
        :rtype: str
        """
        return self._address

    @address.setter
    def address(self, address):
        """Sets the address of this Mayaname1.


        :param address: The address of this Mayaname1.  # noqa: E501
        :type: str
        """

        self._address = address

    @property
    def expire_block_height(self):
        """Gets the expire_block_height of this Mayaname1.  # noqa: E501


        :return: The expire_block_height of this Mayaname1.  # noqa: E501
        :rtype: int
        """
        return self._expire_block_height

    @expire_block_height.setter
    def expire_block_height(self, expire_block_height):
        """Sets the expire_block_height of this Mayaname1.


        :param expire_block_height: The expire_block_height of this Mayaname1.  # noqa: E501
        :type: int
        """

        self._expire_block_height = expire_block_height

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
        if issubclass(Mayaname1, dict):
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
        if not isinstance(other, Mayaname1):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other

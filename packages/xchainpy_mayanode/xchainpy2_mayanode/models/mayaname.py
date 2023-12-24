# coding: utf-8

"""
    Mayanode API

    Mayanode REST API.  # noqa: E501

    OpenAPI spec version: 1.107.3
    Contact: devs@mayachain.org
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

import pprint
import re  # noqa: F401

import six

class Mayaname(object):
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
        'expire_block_height': 'int',
        'owner': 'str',
        'preferred_asset': 'str',
        'aliases': 'list[MayanameAlias]'
    }

    attribute_map = {
        'name': 'name',
        'expire_block_height': 'expire_block_height',
        'owner': 'owner',
        'preferred_asset': 'preferred_asset',
        'aliases': 'aliases'
    }

    def __init__(self, name=None, expire_block_height=None, owner=None, preferred_asset=None, aliases=None):  # noqa: E501
        """Mayaname - a model defined in Swagger"""  # noqa: E501
        self._name = None
        self._expire_block_height = None
        self._owner = None
        self._preferred_asset = None
        self._aliases = None
        self.discriminator = None
        if name is not None:
            self.name = name
        if expire_block_height is not None:
            self.expire_block_height = expire_block_height
        if owner is not None:
            self.owner = owner
        self.preferred_asset = preferred_asset
        self.aliases = aliases

    @property
    def name(self):
        """Gets the name of this Mayaname.  # noqa: E501


        :return: The name of this Mayaname.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this Mayaname.


        :param name: The name of this Mayaname.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def expire_block_height(self):
        """Gets the expire_block_height of this Mayaname.  # noqa: E501


        :return: The expire_block_height of this Mayaname.  # noqa: E501
        :rtype: int
        """
        return self._expire_block_height

    @expire_block_height.setter
    def expire_block_height(self, expire_block_height):
        """Sets the expire_block_height of this Mayaname.


        :param expire_block_height: The expire_block_height of this Mayaname.  # noqa: E501
        :type: int
        """

        self._expire_block_height = expire_block_height

    @property
    def owner(self):
        """Gets the owner of this Mayaname.  # noqa: E501


        :return: The owner of this Mayaname.  # noqa: E501
        :rtype: str
        """
        return self._owner

    @owner.setter
    def owner(self, owner):
        """Sets the owner of this Mayaname.


        :param owner: The owner of this Mayaname.  # noqa: E501
        :type: str
        """

        self._owner = owner

    @property
    def preferred_asset(self):
        """Gets the preferred_asset of this Mayaname.  # noqa: E501


        :return: The preferred_asset of this Mayaname.  # noqa: E501
        :rtype: str
        """
        return self._preferred_asset

    @preferred_asset.setter
    def preferred_asset(self, preferred_asset):
        """Sets the preferred_asset of this Mayaname.


        :param preferred_asset: The preferred_asset of this Mayaname.  # noqa: E501
        :type: str
        """
        if preferred_asset is None:
            raise ValueError("Invalid value for `preferred_asset`, must not be `None`")  # noqa: E501

        self._preferred_asset = preferred_asset

    @property
    def aliases(self):
        """Gets the aliases of this Mayaname.  # noqa: E501


        :return: The aliases of this Mayaname.  # noqa: E501
        :rtype: list[MayanameAlias]
        """
        return self._aliases

    @aliases.setter
    def aliases(self, aliases):
        """Sets the aliases of this Mayaname.


        :param aliases: The aliases of this Mayaname.  # noqa: E501
        :type: list[MayanameAlias]
        """
        if aliases is None:
            raise ValueError("Invalid value for `aliases`, must not be `None`")  # noqa: E501

        self._aliases = aliases

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
        if issubclass(Mayaname, dict):
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
        if not isinstance(other, Mayaname):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other

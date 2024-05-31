# coding: utf-8

"""
    Thornode API

    Thornode REST API.  # noqa: E501

    OpenAPI spec version: 1.132.0
    Contact: devs@thorchain.org
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

import pprint
import re  # noqa: F401

import six

class Thorname(object):
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
        'affiliate_collector_rune': 'str',
        'aliases': 'list[ThornameAlias]'
    }

    attribute_map = {
        'name': 'name',
        'expire_block_height': 'expire_block_height',
        'owner': 'owner',
        'preferred_asset': 'preferred_asset',
        'affiliate_collector_rune': 'affiliate_collector_rune',
        'aliases': 'aliases'
    }

    def __init__(self, name=None, expire_block_height=None, owner=None, preferred_asset=None, affiliate_collector_rune=None, aliases=None):  # noqa: E501
        """Thorname - a model defined in Swagger"""  # noqa: E501
        self._name = None
        self._expire_block_height = None
        self._owner = None
        self._preferred_asset = None
        self._affiliate_collector_rune = None
        self._aliases = None
        self.discriminator = None
        if name is not None:
            self.name = name
        if expire_block_height is not None:
            self.expire_block_height = expire_block_height
        if owner is not None:
            self.owner = owner
        self.preferred_asset = preferred_asset
        if affiliate_collector_rune is not None:
            self.affiliate_collector_rune = affiliate_collector_rune
        self.aliases = aliases

    @property
    def name(self):
        """Gets the name of this Thorname.  # noqa: E501


        :return: The name of this Thorname.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this Thorname.


        :param name: The name of this Thorname.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def expire_block_height(self):
        """Gets the expire_block_height of this Thorname.  # noqa: E501


        :return: The expire_block_height of this Thorname.  # noqa: E501
        :rtype: int
        """
        return self._expire_block_height

    @expire_block_height.setter
    def expire_block_height(self, expire_block_height):
        """Sets the expire_block_height of this Thorname.


        :param expire_block_height: The expire_block_height of this Thorname.  # noqa: E501
        :type: int
        """

        self._expire_block_height = expire_block_height

    @property
    def owner(self):
        """Gets the owner of this Thorname.  # noqa: E501


        :return: The owner of this Thorname.  # noqa: E501
        :rtype: str
        """
        return self._owner

    @owner.setter
    def owner(self, owner):
        """Sets the owner of this Thorname.


        :param owner: The owner of this Thorname.  # noqa: E501
        :type: str
        """

        self._owner = owner

    @property
    def preferred_asset(self):
        """Gets the preferred_asset of this Thorname.  # noqa: E501


        :return: The preferred_asset of this Thorname.  # noqa: E501
        :rtype: str
        """
        return self._preferred_asset

    @preferred_asset.setter
    def preferred_asset(self, preferred_asset):
        """Sets the preferred_asset of this Thorname.


        :param preferred_asset: The preferred_asset of this Thorname.  # noqa: E501
        :type: str
        """
        if preferred_asset is None:
            raise ValueError("Invalid value for `preferred_asset`, must not be `None`")  # noqa: E501

        self._preferred_asset = preferred_asset

    @property
    def affiliate_collector_rune(self):
        """Gets the affiliate_collector_rune of this Thorname.  # noqa: E501

        Amount of RUNE currently accrued by this thorname in affiliate fees waiting to be swapped to preferred asset.  # noqa: E501

        :return: The affiliate_collector_rune of this Thorname.  # noqa: E501
        :rtype: str
        """
        return self._affiliate_collector_rune

    @affiliate_collector_rune.setter
    def affiliate_collector_rune(self, affiliate_collector_rune):
        """Sets the affiliate_collector_rune of this Thorname.

        Amount of RUNE currently accrued by this thorname in affiliate fees waiting to be swapped to preferred asset.  # noqa: E501

        :param affiliate_collector_rune: The affiliate_collector_rune of this Thorname.  # noqa: E501
        :type: str
        """

        self._affiliate_collector_rune = affiliate_collector_rune

    @property
    def aliases(self):
        """Gets the aliases of this Thorname.  # noqa: E501


        :return: The aliases of this Thorname.  # noqa: E501
        :rtype: list[ThornameAlias]
        """
        return self._aliases

    @aliases.setter
    def aliases(self, aliases):
        """Sets the aliases of this Thorname.


        :param aliases: The aliases of this Thorname.  # noqa: E501
        :type: list[ThornameAlias]
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
        if issubclass(Thorname, dict):
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
        if not isinstance(other, Thorname):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other

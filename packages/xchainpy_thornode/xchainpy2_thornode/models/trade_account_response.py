# coding: utf-8

"""
    Thornode API

    Thornode REST API.  # noqa: E501

    OpenAPI spec version: 1.134.0
    Contact: devs@thorchain.org
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

import pprint
import re  # noqa: F401

import six

class TradeAccountResponse(object):
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
        'asset': 'str',
        'units': 'str',
        'owner': 'str',
        'last_add_height': 'int',
        'last_withdraw_height': 'int'
    }

    attribute_map = {
        'asset': 'asset',
        'units': 'units',
        'owner': 'owner',
        'last_add_height': 'last_add_height',
        'last_withdraw_height': 'last_withdraw_height'
    }

    def __init__(self, asset=None, units=None, owner=None, last_add_height=None, last_withdraw_height=None):  # noqa: E501
        """TradeAccountResponse - a model defined in Swagger"""  # noqa: E501
        self._asset = None
        self._units = None
        self._owner = None
        self._last_add_height = None
        self._last_withdraw_height = None
        self.discriminator = None
        self.asset = asset
        self.units = units
        self.owner = owner
        if last_add_height is not None:
            self.last_add_height = last_add_height
        if last_withdraw_height is not None:
            self.last_withdraw_height = last_withdraw_height

    @property
    def asset(self):
        """Gets the asset of this TradeAccountResponse.  # noqa: E501

        trade account asset with \"~\" separator  # noqa: E501

        :return: The asset of this TradeAccountResponse.  # noqa: E501
        :rtype: str
        """
        return self._asset

    @asset.setter
    def asset(self, asset):
        """Sets the asset of this TradeAccountResponse.

        trade account asset with \"~\" separator  # noqa: E501

        :param asset: The asset of this TradeAccountResponse.  # noqa: E501
        :type: str
        """
        if asset is None:
            raise ValueError("Invalid value for `asset`, must not be `None`")  # noqa: E501

        self._asset = asset

    @property
    def units(self):
        """Gets the units of this TradeAccountResponse.  # noqa: E501

        units of trade asset belonging to this owner  # noqa: E501

        :return: The units of this TradeAccountResponse.  # noqa: E501
        :rtype: str
        """
        return self._units

    @units.setter
    def units(self, units):
        """Sets the units of this TradeAccountResponse.

        units of trade asset belonging to this owner  # noqa: E501

        :param units: The units of this TradeAccountResponse.  # noqa: E501
        :type: str
        """
        if units is None:
            raise ValueError("Invalid value for `units`, must not be `None`")  # noqa: E501

        self._units = units

    @property
    def owner(self):
        """Gets the owner of this TradeAccountResponse.  # noqa: E501

        thor address of trade account owner  # noqa: E501

        :return: The owner of this TradeAccountResponse.  # noqa: E501
        :rtype: str
        """
        return self._owner

    @owner.setter
    def owner(self, owner):
        """Sets the owner of this TradeAccountResponse.

        thor address of trade account owner  # noqa: E501

        :param owner: The owner of this TradeAccountResponse.  # noqa: E501
        :type: str
        """
        if owner is None:
            raise ValueError("Invalid value for `owner`, must not be `None`")  # noqa: E501

        self._owner = owner

    @property
    def last_add_height(self):
        """Gets the last_add_height of this TradeAccountResponse.  # noqa: E501

        last thorchain height trade assets were added to trade account  # noqa: E501

        :return: The last_add_height of this TradeAccountResponse.  # noqa: E501
        :rtype: int
        """
        return self._last_add_height

    @last_add_height.setter
    def last_add_height(self, last_add_height):
        """Sets the last_add_height of this TradeAccountResponse.

        last thorchain height trade assets were added to trade account  # noqa: E501

        :param last_add_height: The last_add_height of this TradeAccountResponse.  # noqa: E501
        :type: int
        """

        self._last_add_height = last_add_height

    @property
    def last_withdraw_height(self):
        """Gets the last_withdraw_height of this TradeAccountResponse.  # noqa: E501

        last thorchain height trade assets were withdrawn from trade account  # noqa: E501

        :return: The last_withdraw_height of this TradeAccountResponse.  # noqa: E501
        :rtype: int
        """
        return self._last_withdraw_height

    @last_withdraw_height.setter
    def last_withdraw_height(self, last_withdraw_height):
        """Sets the last_withdraw_height of this TradeAccountResponse.

        last thorchain height trade assets were withdrawn from trade account  # noqa: E501

        :param last_withdraw_height: The last_withdraw_height of this TradeAccountResponse.  # noqa: E501
        :type: int
        """

        self._last_withdraw_height = last_withdraw_height

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
        if issubclass(TradeAccountResponse, dict):
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
        if not isinstance(other, TradeAccountResponse):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other

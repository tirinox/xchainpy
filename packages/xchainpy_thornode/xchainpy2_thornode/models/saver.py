# coding: utf-8

"""
    Thornode API

    Thornode REST API.  # noqa: E501

    OpenAPI spec version: 1.122.0
    Contact: devs@thorchain.org
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

import pprint
import re  # noqa: F401

import six

class Saver(object):
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
        'asset_address': 'str',
        'last_add_height': 'int',
        'last_withdraw_height': 'int',
        'units': 'str',
        'asset_deposit_value': 'str',
        'asset_redeem_value': 'str',
        'growth_pct': 'str'
    }

    attribute_map = {
        'asset': 'asset',
        'asset_address': 'asset_address',
        'last_add_height': 'last_add_height',
        'last_withdraw_height': 'last_withdraw_height',
        'units': 'units',
        'asset_deposit_value': 'asset_deposit_value',
        'asset_redeem_value': 'asset_redeem_value',
        'growth_pct': 'growth_pct'
    }

    def __init__(self, asset=None, asset_address=None, last_add_height=None, last_withdraw_height=None, units=None, asset_deposit_value=None, asset_redeem_value=None, growth_pct=None):  # noqa: E501
        """Saver - a model defined in Swagger"""  # noqa: E501
        self._asset = None
        self._asset_address = None
        self._last_add_height = None
        self._last_withdraw_height = None
        self._units = None
        self._asset_deposit_value = None
        self._asset_redeem_value = None
        self._growth_pct = None
        self.discriminator = None
        self.asset = asset
        self.asset_address = asset_address
        if last_add_height is not None:
            self.last_add_height = last_add_height
        if last_withdraw_height is not None:
            self.last_withdraw_height = last_withdraw_height
        self.units = units
        self.asset_deposit_value = asset_deposit_value
        self.asset_redeem_value = asset_redeem_value
        self.growth_pct = growth_pct

    @property
    def asset(self):
        """Gets the asset of this Saver.  # noqa: E501


        :return: The asset of this Saver.  # noqa: E501
        :rtype: str
        """
        return self._asset

    @asset.setter
    def asset(self, asset):
        """Sets the asset of this Saver.


        :param asset: The asset of this Saver.  # noqa: E501
        :type: str
        """
        if asset is None:
            raise ValueError("Invalid value for `asset`, must not be `None`")  # noqa: E501

        self._asset = asset

    @property
    def asset_address(self):
        """Gets the asset_address of this Saver.  # noqa: E501


        :return: The asset_address of this Saver.  # noqa: E501
        :rtype: str
        """
        return self._asset_address

    @asset_address.setter
    def asset_address(self, asset_address):
        """Sets the asset_address of this Saver.


        :param asset_address: The asset_address of this Saver.  # noqa: E501
        :type: str
        """
        if asset_address is None:
            raise ValueError("Invalid value for `asset_address`, must not be `None`")  # noqa: E501

        self._asset_address = asset_address

    @property
    def last_add_height(self):
        """Gets the last_add_height of this Saver.  # noqa: E501


        :return: The last_add_height of this Saver.  # noqa: E501
        :rtype: int
        """
        return self._last_add_height

    @last_add_height.setter
    def last_add_height(self, last_add_height):
        """Sets the last_add_height of this Saver.


        :param last_add_height: The last_add_height of this Saver.  # noqa: E501
        :type: int
        """

        self._last_add_height = last_add_height

    @property
    def last_withdraw_height(self):
        """Gets the last_withdraw_height of this Saver.  # noqa: E501


        :return: The last_withdraw_height of this Saver.  # noqa: E501
        :rtype: int
        """
        return self._last_withdraw_height

    @last_withdraw_height.setter
    def last_withdraw_height(self, last_withdraw_height):
        """Sets the last_withdraw_height of this Saver.


        :param last_withdraw_height: The last_withdraw_height of this Saver.  # noqa: E501
        :type: int
        """

        self._last_withdraw_height = last_withdraw_height

    @property
    def units(self):
        """Gets the units of this Saver.  # noqa: E501


        :return: The units of this Saver.  # noqa: E501
        :rtype: str
        """
        return self._units

    @units.setter
    def units(self, units):
        """Sets the units of this Saver.


        :param units: The units of this Saver.  # noqa: E501
        :type: str
        """
        if units is None:
            raise ValueError("Invalid value for `units`, must not be `None`")  # noqa: E501

        self._units = units

    @property
    def asset_deposit_value(self):
        """Gets the asset_deposit_value of this Saver.  # noqa: E501


        :return: The asset_deposit_value of this Saver.  # noqa: E501
        :rtype: str
        """
        return self._asset_deposit_value

    @asset_deposit_value.setter
    def asset_deposit_value(self, asset_deposit_value):
        """Sets the asset_deposit_value of this Saver.


        :param asset_deposit_value: The asset_deposit_value of this Saver.  # noqa: E501
        :type: str
        """
        if asset_deposit_value is None:
            raise ValueError("Invalid value for `asset_deposit_value`, must not be `None`")  # noqa: E501

        self._asset_deposit_value = asset_deposit_value

    @property
    def asset_redeem_value(self):
        """Gets the asset_redeem_value of this Saver.  # noqa: E501


        :return: The asset_redeem_value of this Saver.  # noqa: E501
        :rtype: str
        """
        return self._asset_redeem_value

    @asset_redeem_value.setter
    def asset_redeem_value(self, asset_redeem_value):
        """Sets the asset_redeem_value of this Saver.


        :param asset_redeem_value: The asset_redeem_value of this Saver.  # noqa: E501
        :type: str
        """
        if asset_redeem_value is None:
            raise ValueError("Invalid value for `asset_redeem_value`, must not be `None`")  # noqa: E501

        self._asset_redeem_value = asset_redeem_value

    @property
    def growth_pct(self):
        """Gets the growth_pct of this Saver.  # noqa: E501


        :return: The growth_pct of this Saver.  # noqa: E501
        :rtype: str
        """
        return self._growth_pct

    @growth_pct.setter
    def growth_pct(self, growth_pct):
        """Sets the growth_pct of this Saver.


        :param growth_pct: The growth_pct of this Saver.  # noqa: E501
        :type: str
        """
        if growth_pct is None:
            raise ValueError("Invalid value for `growth_pct`, must not be `None`")  # noqa: E501

        self._growth_pct = growth_pct

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
        if issubclass(Saver, dict):
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
        if not isinstance(other, Saver):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other

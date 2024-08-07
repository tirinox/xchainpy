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

class RUNEProvider(object):
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
        'rune_address': 'str',
        'units': 'str',
        'value': 'str',
        'pnl': 'str',
        'deposit_amount': 'str',
        'withdraw_amount': 'str',
        'last_deposit_height': 'int',
        'last_withdraw_height': 'int'
    }

    attribute_map = {
        'rune_address': 'rune_address',
        'units': 'units',
        'value': 'value',
        'pnl': 'pnl',
        'deposit_amount': 'deposit_amount',
        'withdraw_amount': 'withdraw_amount',
        'last_deposit_height': 'last_deposit_height',
        'last_withdraw_height': 'last_withdraw_height'
    }

    def __init__(self, rune_address=None, units=None, value=None, pnl=None, deposit_amount=None, withdraw_amount=None, last_deposit_height=None, last_withdraw_height=None):  # noqa: E501
        """RUNEProvider - a model defined in Swagger"""  # noqa: E501
        self._rune_address = None
        self._units = None
        self._value = None
        self._pnl = None
        self._deposit_amount = None
        self._withdraw_amount = None
        self._last_deposit_height = None
        self._last_withdraw_height = None
        self.discriminator = None
        self.rune_address = rune_address
        self.units = units
        self.value = value
        self.pnl = pnl
        self.deposit_amount = deposit_amount
        self.withdraw_amount = withdraw_amount
        self.last_deposit_height = last_deposit_height
        self.last_withdraw_height = last_withdraw_height

    @property
    def rune_address(self):
        """Gets the rune_address of this RUNEProvider.  # noqa: E501


        :return: The rune_address of this RUNEProvider.  # noqa: E501
        :rtype: str
        """
        return self._rune_address

    @rune_address.setter
    def rune_address(self, rune_address):
        """Sets the rune_address of this RUNEProvider.


        :param rune_address: The rune_address of this RUNEProvider.  # noqa: E501
        :type: str
        """
        if rune_address is None:
            raise ValueError("Invalid value for `rune_address`, must not be `None`")  # noqa: E501

        self._rune_address = rune_address

    @property
    def units(self):
        """Gets the units of this RUNEProvider.  # noqa: E501


        :return: The units of this RUNEProvider.  # noqa: E501
        :rtype: str
        """
        return self._units

    @units.setter
    def units(self, units):
        """Sets the units of this RUNEProvider.


        :param units: The units of this RUNEProvider.  # noqa: E501
        :type: str
        """
        if units is None:
            raise ValueError("Invalid value for `units`, must not be `None`")  # noqa: E501

        self._units = units

    @property
    def value(self):
        """Gets the value of this RUNEProvider.  # noqa: E501


        :return: The value of this RUNEProvider.  # noqa: E501
        :rtype: str
        """
        return self._value

    @value.setter
    def value(self, value):
        """Sets the value of this RUNEProvider.


        :param value: The value of this RUNEProvider.  # noqa: E501
        :type: str
        """
        if value is None:
            raise ValueError("Invalid value for `value`, must not be `None`")  # noqa: E501

        self._value = value

    @property
    def pnl(self):
        """Gets the pnl of this RUNEProvider.  # noqa: E501


        :return: The pnl of this RUNEProvider.  # noqa: E501
        :rtype: str
        """
        return self._pnl

    @pnl.setter
    def pnl(self, pnl):
        """Sets the pnl of this RUNEProvider.


        :param pnl: The pnl of this RUNEProvider.  # noqa: E501
        :type: str
        """
        if pnl is None:
            raise ValueError("Invalid value for `pnl`, must not be `None`")  # noqa: E501

        self._pnl = pnl

    @property
    def deposit_amount(self):
        """Gets the deposit_amount of this RUNEProvider.  # noqa: E501


        :return: The deposit_amount of this RUNEProvider.  # noqa: E501
        :rtype: str
        """
        return self._deposit_amount

    @deposit_amount.setter
    def deposit_amount(self, deposit_amount):
        """Sets the deposit_amount of this RUNEProvider.


        :param deposit_amount: The deposit_amount of this RUNEProvider.  # noqa: E501
        :type: str
        """
        if deposit_amount is None:
            raise ValueError("Invalid value for `deposit_amount`, must not be `None`")  # noqa: E501

        self._deposit_amount = deposit_amount

    @property
    def withdraw_amount(self):
        """Gets the withdraw_amount of this RUNEProvider.  # noqa: E501


        :return: The withdraw_amount of this RUNEProvider.  # noqa: E501
        :rtype: str
        """
        return self._withdraw_amount

    @withdraw_amount.setter
    def withdraw_amount(self, withdraw_amount):
        """Sets the withdraw_amount of this RUNEProvider.


        :param withdraw_amount: The withdraw_amount of this RUNEProvider.  # noqa: E501
        :type: str
        """
        if withdraw_amount is None:
            raise ValueError("Invalid value for `withdraw_amount`, must not be `None`")  # noqa: E501

        self._withdraw_amount = withdraw_amount

    @property
    def last_deposit_height(self):
        """Gets the last_deposit_height of this RUNEProvider.  # noqa: E501


        :return: The last_deposit_height of this RUNEProvider.  # noqa: E501
        :rtype: int
        """
        return self._last_deposit_height

    @last_deposit_height.setter
    def last_deposit_height(self, last_deposit_height):
        """Sets the last_deposit_height of this RUNEProvider.


        :param last_deposit_height: The last_deposit_height of this RUNEProvider.  # noqa: E501
        :type: int
        """
        if last_deposit_height is None:
            raise ValueError("Invalid value for `last_deposit_height`, must not be `None`")  # noqa: E501

        self._last_deposit_height = last_deposit_height

    @property
    def last_withdraw_height(self):
        """Gets the last_withdraw_height of this RUNEProvider.  # noqa: E501


        :return: The last_withdraw_height of this RUNEProvider.  # noqa: E501
        :rtype: int
        """
        return self._last_withdraw_height

    @last_withdraw_height.setter
    def last_withdraw_height(self, last_withdraw_height):
        """Sets the last_withdraw_height of this RUNEProvider.


        :param last_withdraw_height: The last_withdraw_height of this RUNEProvider.  # noqa: E501
        :type: int
        """
        if last_withdraw_height is None:
            raise ValueError("Invalid value for `last_withdraw_height`, must not be `None`")  # noqa: E501

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
        if issubclass(RUNEProvider, dict):
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
        if not isinstance(other, RUNEProvider):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other

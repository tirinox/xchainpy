# coding: utf-8

"""
    Thornode API

    Thornode REST API.  # noqa: E501

    OpenAPI spec version: 3.0.0
    Contact: devs@thorchain.org
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

import pprint
import re  # noqa: F401

import six

class Borrower(object):
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
        'owner': 'str',
        'asset': 'str',
        'debt_issued': 'str',
        'debt_repaid': 'str',
        'debt_current': 'str',
        'collateral_deposited': 'str',
        'collateral_withdrawn': 'str',
        'collateral_current': 'str',
        'last_open_height': 'int',
        'last_repay_height': 'int'
    }

    attribute_map = {
        'owner': 'owner',
        'asset': 'asset',
        'debt_issued': 'debt_issued',
        'debt_repaid': 'debt_repaid',
        'debt_current': 'debt_current',
        'collateral_deposited': 'collateral_deposited',
        'collateral_withdrawn': 'collateral_withdrawn',
        'collateral_current': 'collateral_current',
        'last_open_height': 'last_open_height',
        'last_repay_height': 'last_repay_height'
    }

    def __init__(self, owner=None, asset=None, debt_issued=None, debt_repaid=None, debt_current=None, collateral_deposited=None, collateral_withdrawn=None, collateral_current=None, last_open_height=None, last_repay_height=None):  # noqa: E501
        """Borrower - a model defined in Swagger"""  # noqa: E501
        self._owner = None
        self._asset = None
        self._debt_issued = None
        self._debt_repaid = None
        self._debt_current = None
        self._collateral_deposited = None
        self._collateral_withdrawn = None
        self._collateral_current = None
        self._last_open_height = None
        self._last_repay_height = None
        self.discriminator = None
        self.owner = owner
        self.asset = asset
        self.debt_issued = debt_issued
        self.debt_repaid = debt_repaid
        self.debt_current = debt_current
        self.collateral_deposited = collateral_deposited
        self.collateral_withdrawn = collateral_withdrawn
        self.collateral_current = collateral_current
        self.last_open_height = last_open_height
        self.last_repay_height = last_repay_height

    @property
    def owner(self):
        """Gets the owner of this Borrower.  # noqa: E501


        :return: The owner of this Borrower.  # noqa: E501
        :rtype: str
        """
        return self._owner

    @owner.setter
    def owner(self, owner):
        """Sets the owner of this Borrower.


        :param owner: The owner of this Borrower.  # noqa: E501
        :type: str
        """
        if owner is None:
            raise ValueError("Invalid value for `owner`, must not be `None`")  # noqa: E501

        self._owner = owner

    @property
    def asset(self):
        """Gets the asset of this Borrower.  # noqa: E501


        :return: The asset of this Borrower.  # noqa: E501
        :rtype: str
        """
        return self._asset

    @asset.setter
    def asset(self, asset):
        """Sets the asset of this Borrower.


        :param asset: The asset of this Borrower.  # noqa: E501
        :type: str
        """
        if asset is None:
            raise ValueError("Invalid value for `asset`, must not be `None`")  # noqa: E501

        self._asset = asset

    @property
    def debt_issued(self):
        """Gets the debt_issued of this Borrower.  # noqa: E501


        :return: The debt_issued of this Borrower.  # noqa: E501
        :rtype: str
        """
        return self._debt_issued

    @debt_issued.setter
    def debt_issued(self, debt_issued):
        """Sets the debt_issued of this Borrower.


        :param debt_issued: The debt_issued of this Borrower.  # noqa: E501
        :type: str
        """
        if debt_issued is None:
            raise ValueError("Invalid value for `debt_issued`, must not be `None`")  # noqa: E501

        self._debt_issued = debt_issued

    @property
    def debt_repaid(self):
        """Gets the debt_repaid of this Borrower.  # noqa: E501


        :return: The debt_repaid of this Borrower.  # noqa: E501
        :rtype: str
        """
        return self._debt_repaid

    @debt_repaid.setter
    def debt_repaid(self, debt_repaid):
        """Sets the debt_repaid of this Borrower.


        :param debt_repaid: The debt_repaid of this Borrower.  # noqa: E501
        :type: str
        """
        if debt_repaid is None:
            raise ValueError("Invalid value for `debt_repaid`, must not be `None`")  # noqa: E501

        self._debt_repaid = debt_repaid

    @property
    def debt_current(self):
        """Gets the debt_current of this Borrower.  # noqa: E501


        :return: The debt_current of this Borrower.  # noqa: E501
        :rtype: str
        """
        return self._debt_current

    @debt_current.setter
    def debt_current(self, debt_current):
        """Sets the debt_current of this Borrower.


        :param debt_current: The debt_current of this Borrower.  # noqa: E501
        :type: str
        """
        if debt_current is None:
            raise ValueError("Invalid value for `debt_current`, must not be `None`")  # noqa: E501

        self._debt_current = debt_current

    @property
    def collateral_deposited(self):
        """Gets the collateral_deposited of this Borrower.  # noqa: E501


        :return: The collateral_deposited of this Borrower.  # noqa: E501
        :rtype: str
        """
        return self._collateral_deposited

    @collateral_deposited.setter
    def collateral_deposited(self, collateral_deposited):
        """Sets the collateral_deposited of this Borrower.


        :param collateral_deposited: The collateral_deposited of this Borrower.  # noqa: E501
        :type: str
        """
        if collateral_deposited is None:
            raise ValueError("Invalid value for `collateral_deposited`, must not be `None`")  # noqa: E501

        self._collateral_deposited = collateral_deposited

    @property
    def collateral_withdrawn(self):
        """Gets the collateral_withdrawn of this Borrower.  # noqa: E501


        :return: The collateral_withdrawn of this Borrower.  # noqa: E501
        :rtype: str
        """
        return self._collateral_withdrawn

    @collateral_withdrawn.setter
    def collateral_withdrawn(self, collateral_withdrawn):
        """Sets the collateral_withdrawn of this Borrower.


        :param collateral_withdrawn: The collateral_withdrawn of this Borrower.  # noqa: E501
        :type: str
        """
        if collateral_withdrawn is None:
            raise ValueError("Invalid value for `collateral_withdrawn`, must not be `None`")  # noqa: E501

        self._collateral_withdrawn = collateral_withdrawn

    @property
    def collateral_current(self):
        """Gets the collateral_current of this Borrower.  # noqa: E501


        :return: The collateral_current of this Borrower.  # noqa: E501
        :rtype: str
        """
        return self._collateral_current

    @collateral_current.setter
    def collateral_current(self, collateral_current):
        """Sets the collateral_current of this Borrower.


        :param collateral_current: The collateral_current of this Borrower.  # noqa: E501
        :type: str
        """
        if collateral_current is None:
            raise ValueError("Invalid value for `collateral_current`, must not be `None`")  # noqa: E501

        self._collateral_current = collateral_current

    @property
    def last_open_height(self):
        """Gets the last_open_height of this Borrower.  # noqa: E501


        :return: The last_open_height of this Borrower.  # noqa: E501
        :rtype: int
        """
        return self._last_open_height

    @last_open_height.setter
    def last_open_height(self, last_open_height):
        """Sets the last_open_height of this Borrower.


        :param last_open_height: The last_open_height of this Borrower.  # noqa: E501
        :type: int
        """
        if last_open_height is None:
            raise ValueError("Invalid value for `last_open_height`, must not be `None`")  # noqa: E501

        self._last_open_height = last_open_height

    @property
    def last_repay_height(self):
        """Gets the last_repay_height of this Borrower.  # noqa: E501


        :return: The last_repay_height of this Borrower.  # noqa: E501
        :rtype: int
        """
        return self._last_repay_height

    @last_repay_height.setter
    def last_repay_height(self, last_repay_height):
        """Sets the last_repay_height of this Borrower.


        :param last_repay_height: The last_repay_height of this Borrower.  # noqa: E501
        :type: int
        """
        if last_repay_height is None:
            raise ValueError("Invalid value for `last_repay_height`, must not be `None`")  # noqa: E501

        self._last_repay_height = last_repay_height

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
        if issubclass(Borrower, dict):
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
        if not isinstance(other, Borrower):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other

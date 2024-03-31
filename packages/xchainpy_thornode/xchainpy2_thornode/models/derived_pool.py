# coding: utf-8

"""
    Thornode API

    Thornode REST API.  # noqa: E501

    OpenAPI spec version: 1.130.1
    Contact: devs@thorchain.org
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

import pprint
import re  # noqa: F401

import six

class DerivedPool(object):
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
        'status': 'str',
        'decimals': 'int',
        'balance_asset': 'str',
        'balance_rune': 'str',
        'derived_depth_bps': 'str'
    }

    attribute_map = {
        'asset': 'asset',
        'status': 'status',
        'decimals': 'decimals',
        'balance_asset': 'balance_asset',
        'balance_rune': 'balance_rune',
        'derived_depth_bps': 'derived_depth_bps'
    }

    def __init__(self, asset=None, status=None, decimals=None, balance_asset=None, balance_rune=None, derived_depth_bps=None):  # noqa: E501
        """DerivedPool - a model defined in Swagger"""  # noqa: E501
        self._asset = None
        self._status = None
        self._decimals = None
        self._balance_asset = None
        self._balance_rune = None
        self._derived_depth_bps = None
        self.discriminator = None
        self.asset = asset
        self.status = status
        if decimals is not None:
            self.decimals = decimals
        self.balance_asset = balance_asset
        self.balance_rune = balance_rune
        self.derived_depth_bps = derived_depth_bps

    @property
    def asset(self):
        """Gets the asset of this DerivedPool.  # noqa: E501


        :return: The asset of this DerivedPool.  # noqa: E501
        :rtype: str
        """
        return self._asset

    @asset.setter
    def asset(self, asset):
        """Sets the asset of this DerivedPool.


        :param asset: The asset of this DerivedPool.  # noqa: E501
        :type: str
        """
        if asset is None:
            raise ValueError("Invalid value for `asset`, must not be `None`")  # noqa: E501

        self._asset = asset

    @property
    def status(self):
        """Gets the status of this DerivedPool.  # noqa: E501


        :return: The status of this DerivedPool.  # noqa: E501
        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, status):
        """Sets the status of this DerivedPool.


        :param status: The status of this DerivedPool.  # noqa: E501
        :type: str
        """
        if status is None:
            raise ValueError("Invalid value for `status`, must not be `None`")  # noqa: E501

        self._status = status

    @property
    def decimals(self):
        """Gets the decimals of this DerivedPool.  # noqa: E501


        :return: The decimals of this DerivedPool.  # noqa: E501
        :rtype: int
        """
        return self._decimals

    @decimals.setter
    def decimals(self, decimals):
        """Sets the decimals of this DerivedPool.


        :param decimals: The decimals of this DerivedPool.  # noqa: E501
        :type: int
        """

        self._decimals = decimals

    @property
    def balance_asset(self):
        """Gets the balance_asset of this DerivedPool.  # noqa: E501


        :return: The balance_asset of this DerivedPool.  # noqa: E501
        :rtype: str
        """
        return self._balance_asset

    @balance_asset.setter
    def balance_asset(self, balance_asset):
        """Sets the balance_asset of this DerivedPool.


        :param balance_asset: The balance_asset of this DerivedPool.  # noqa: E501
        :type: str
        """
        if balance_asset is None:
            raise ValueError("Invalid value for `balance_asset`, must not be `None`")  # noqa: E501

        self._balance_asset = balance_asset

    @property
    def balance_rune(self):
        """Gets the balance_rune of this DerivedPool.  # noqa: E501


        :return: The balance_rune of this DerivedPool.  # noqa: E501
        :rtype: str
        """
        return self._balance_rune

    @balance_rune.setter
    def balance_rune(self, balance_rune):
        """Sets the balance_rune of this DerivedPool.


        :param balance_rune: The balance_rune of this DerivedPool.  # noqa: E501
        :type: str
        """
        if balance_rune is None:
            raise ValueError("Invalid value for `balance_rune`, must not be `None`")  # noqa: E501

        self._balance_rune = balance_rune

    @property
    def derived_depth_bps(self):
        """Gets the derived_depth_bps of this DerivedPool.  # noqa: E501

        the depth of the derived virtual pool relative to L1 pool (in basis points)  # noqa: E501

        :return: The derived_depth_bps of this DerivedPool.  # noqa: E501
        :rtype: str
        """
        return self._derived_depth_bps

    @derived_depth_bps.setter
    def derived_depth_bps(self, derived_depth_bps):
        """Sets the derived_depth_bps of this DerivedPool.

        the depth of the derived virtual pool relative to L1 pool (in basis points)  # noqa: E501

        :param derived_depth_bps: The derived_depth_bps of this DerivedPool.  # noqa: E501
        :type: str
        """
        if derived_depth_bps is None:
            raise ValueError("Invalid value for `derived_depth_bps`, must not be `None`")  # noqa: E501

        self._derived_depth_bps = derived_depth_bps

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
        if issubclass(DerivedPool, dict):
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
        if not isinstance(other, DerivedPool):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other

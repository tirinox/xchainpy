# coding: utf-8

"""
    Midgard Public API

    The Midgard Public API queries THORChain and any chains linked via the Bifröst and prepares information about the network to be readily available for public users. The API parses transaction event data from THORChain and stores them in a time-series database to make time-dependent queries easy. Midgard does not hold critical information. To interact with THORChain protocol, users should query THORNode directly.  # noqa: E501

    OpenAPI spec version: 2.24.3
    Contact: devs@thorchain.org
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

import pprint
import re  # noqa: F401

import six

class AddLiquidityMetadata(object):
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
        'liquidity_units': 'str'
    }

    attribute_map = {
        'liquidity_units': 'liquidityUnits'
    }

    def __init__(self, liquidity_units=None):  # noqa: E501
        """AddLiquidityMetadata - a model defined in Swagger"""  # noqa: E501
        self._liquidity_units = None
        self.discriminator = None
        self.liquidity_units = liquidity_units

    @property
    def liquidity_units(self):
        """Gets the liquidity_units of this AddLiquidityMetadata.  # noqa: E501

        Int64, amount of liquidity units assigned to the member as result of the liquidity deposit   # noqa: E501

        :return: The liquidity_units of this AddLiquidityMetadata.  # noqa: E501
        :rtype: str
        """
        return self._liquidity_units

    @liquidity_units.setter
    def liquidity_units(self, liquidity_units):
        """Sets the liquidity_units of this AddLiquidityMetadata.

        Int64, amount of liquidity units assigned to the member as result of the liquidity deposit   # noqa: E501

        :param liquidity_units: The liquidity_units of this AddLiquidityMetadata.  # noqa: E501
        :type: str
        """
        if liquidity_units is None:
            raise ValueError("Invalid value for `liquidity_units`, must not be `None`")  # noqa: E501

        self._liquidity_units = liquidity_units

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
        if issubclass(AddLiquidityMetadata, dict):
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
        if not isinstance(other, AddLiquidityMetadata):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other

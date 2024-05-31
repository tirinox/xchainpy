# coding: utf-8

"""
    Mayanode API

    Mayanode REST API.  # noqa: E501

    OpenAPI spec version: 1.109.0
    Contact: devs@mayachain.org
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

import pprint
import re  # noqa: F401

import six

class QuoteFees(object):
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
        'affiliate': 'str',
        'outbound': 'str',
        'liquidity': 'str',
        'total': 'str',
        'slippage_bps': 'int',
        'total_bps': 'int'
    }

    attribute_map = {
        'asset': 'asset',
        'affiliate': 'affiliate',
        'outbound': 'outbound',
        'liquidity': 'liquidity',
        'total': 'total',
        'slippage_bps': 'slippage_bps',
        'total_bps': 'total_bps'
    }

    def __init__(self, asset=None, affiliate=None, outbound=None, liquidity=None, total=None, slippage_bps=None, total_bps=None):  # noqa: E501
        """QuoteFees - a model defined in Swagger"""  # noqa: E501
        self._asset = None
        self._affiliate = None
        self._outbound = None
        self._liquidity = None
        self._total = None
        self._slippage_bps = None
        self._total_bps = None
        self.discriminator = None
        self.asset = asset
        if affiliate is not None:
            self.affiliate = affiliate
        if outbound is not None:
            self.outbound = outbound
        self.liquidity = liquidity
        self.total = total
        self.slippage_bps = slippage_bps
        self.total_bps = total_bps

    @property
    def asset(self):
        """Gets the asset of this QuoteFees.  # noqa: E501

        the target asset used for all fees  # noqa: E501

        :return: The asset of this QuoteFees.  # noqa: E501
        :rtype: str
        """
        return self._asset

    @asset.setter
    def asset(self, asset):
        """Sets the asset of this QuoteFees.

        the target asset used for all fees  # noqa: E501

        :param asset: The asset of this QuoteFees.  # noqa: E501
        :type: str
        """
        if asset is None:
            raise ValueError("Invalid value for `asset`, must not be `None`")  # noqa: E501

        self._asset = asset

    @property
    def affiliate(self):
        """Gets the affiliate of this QuoteFees.  # noqa: E501

        affiliate fee in the target asset  # noqa: E501

        :return: The affiliate of this QuoteFees.  # noqa: E501
        :rtype: str
        """
        return self._affiliate

    @affiliate.setter
    def affiliate(self, affiliate):
        """Sets the affiliate of this QuoteFees.

        affiliate fee in the target asset  # noqa: E501

        :param affiliate: The affiliate of this QuoteFees.  # noqa: E501
        :type: str
        """

        self._affiliate = affiliate

    @property
    def outbound(self):
        """Gets the outbound of this QuoteFees.  # noqa: E501

        outbound fee in the target asset  # noqa: E501

        :return: The outbound of this QuoteFees.  # noqa: E501
        :rtype: str
        """
        return self._outbound

    @outbound.setter
    def outbound(self, outbound):
        """Sets the outbound of this QuoteFees.

        outbound fee in the target asset  # noqa: E501

        :param outbound: The outbound of this QuoteFees.  # noqa: E501
        :type: str
        """

        self._outbound = outbound

    @property
    def liquidity(self):
        """Gets the liquidity of this QuoteFees.  # noqa: E501

        liquidity fees paid to pools in the target asset  # noqa: E501

        :return: The liquidity of this QuoteFees.  # noqa: E501
        :rtype: str
        """
        return self._liquidity

    @liquidity.setter
    def liquidity(self, liquidity):
        """Sets the liquidity of this QuoteFees.

        liquidity fees paid to pools in the target asset  # noqa: E501

        :param liquidity: The liquidity of this QuoteFees.  # noqa: E501
        :type: str
        """
        if liquidity is None:
            raise ValueError("Invalid value for `liquidity`, must not be `None`")  # noqa: E501

        self._liquidity = liquidity

    @property
    def total(self):
        """Gets the total of this QuoteFees.  # noqa: E501

        total fees in the target asset  # noqa: E501

        :return: The total of this QuoteFees.  # noqa: E501
        :rtype: str
        """
        return self._total

    @total.setter
    def total(self, total):
        """Sets the total of this QuoteFees.

        total fees in the target asset  # noqa: E501

        :param total: The total of this QuoteFees.  # noqa: E501
        :type: str
        """
        if total is None:
            raise ValueError("Invalid value for `total`, must not be `None`")  # noqa: E501

        self._total = total

    @property
    def slippage_bps(self):
        """Gets the slippage_bps of this QuoteFees.  # noqa: E501

        the swap slippage in basis points  # noqa: E501

        :return: The slippage_bps of this QuoteFees.  # noqa: E501
        :rtype: int
        """
        return self._slippage_bps

    @slippage_bps.setter
    def slippage_bps(self, slippage_bps):
        """Sets the slippage_bps of this QuoteFees.

        the swap slippage in basis points  # noqa: E501

        :param slippage_bps: The slippage_bps of this QuoteFees.  # noqa: E501
        :type: int
        """
        if slippage_bps is None:
            raise ValueError("Invalid value for `slippage_bps`, must not be `None`")  # noqa: E501

        self._slippage_bps = slippage_bps

    @property
    def total_bps(self):
        """Gets the total_bps of this QuoteFees.  # noqa: E501

        total basis points in fees relative to amount out  # noqa: E501

        :return: The total_bps of this QuoteFees.  # noqa: E501
        :rtype: int
        """
        return self._total_bps

    @total_bps.setter
    def total_bps(self, total_bps):
        """Sets the total_bps of this QuoteFees.

        total basis points in fees relative to amount out  # noqa: E501

        :param total_bps: The total_bps of this QuoteFees.  # noqa: E501
        :type: int
        """
        if total_bps is None:
            raise ValueError("Invalid value for `total_bps`, must not be `None`")  # noqa: E501

        self._total_bps = total_bps

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
        if issubclass(QuoteFees, dict):
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
        if not isinstance(other, QuoteFees):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other

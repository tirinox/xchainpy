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
        'outbound': 'str'
    }

    attribute_map = {
        'asset': 'asset',
        'affiliate': 'affiliate',
        'outbound': 'outbound'
    }

    def __init__(self, asset=None, affiliate=None, outbound=None):  # noqa: E501
        """QuoteFees - a model defined in Swagger"""  # noqa: E501
        self._asset = None
        self._affiliate = None
        self._outbound = None
        self.discriminator = None
        self.asset = asset
        self.affiliate = affiliate
        self.outbound = outbound

    @property
    def asset(self):
        """Gets the asset of this QuoteFees.  # noqa: E501


        :return: The asset of this QuoteFees.  # noqa: E501
        :rtype: str
        """
        return self._asset

    @asset.setter
    def asset(self, asset):
        """Sets the asset of this QuoteFees.


        :param asset: The asset of this QuoteFees.  # noqa: E501
        :type: str
        """
        if asset is None:
            raise ValueError("Invalid value for `asset`, must not be `None`")  # noqa: E501

        self._asset = asset

    @property
    def affiliate(self):
        """Gets the affiliate of this QuoteFees.  # noqa: E501


        :return: The affiliate of this QuoteFees.  # noqa: E501
        :rtype: str
        """
        return self._affiliate

    @affiliate.setter
    def affiliate(self, affiliate):
        """Sets the affiliate of this QuoteFees.


        :param affiliate: The affiliate of this QuoteFees.  # noqa: E501
        :type: str
        """
        if affiliate is None:
            raise ValueError("Invalid value for `affiliate`, must not be `None`")  # noqa: E501

        self._affiliate = affiliate

    @property
    def outbound(self):
        """Gets the outbound of this QuoteFees.  # noqa: E501


        :return: The outbound of this QuoteFees.  # noqa: E501
        :rtype: str
        """
        return self._outbound

    @outbound.setter
    def outbound(self, outbound):
        """Sets the outbound of this QuoteFees.


        :param outbound: The outbound of this QuoteFees.  # noqa: E501
        :type: str
        """
        if outbound is None:
            raise ValueError("Invalid value for `outbound`, must not be `None`")  # noqa: E501

        self._outbound = outbound

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

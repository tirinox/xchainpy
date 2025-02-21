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

class BorrowerDetails(object):
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
        'pools': 'list[BorrowerPool]'
    }

    attribute_map = {
        'pools': 'pools'
    }

    def __init__(self, pools=None):  # noqa: E501
        """BorrowerDetails - a model defined in Swagger"""  # noqa: E501
        self._pools = None
        self.discriminator = None
        self.pools = pools

    @property
    def pools(self):
        """Gets the pools of this BorrowerDetails.  # noqa: E501

        List details of all the loans identified with the given address  # noqa: E501

        :return: The pools of this BorrowerDetails.  # noqa: E501
        :rtype: list[BorrowerPool]
        """
        return self._pools

    @pools.setter
    def pools(self, pools):
        """Sets the pools of this BorrowerDetails.

        List details of all the loans identified with the given address  # noqa: E501

        :param pools: The pools of this BorrowerDetails.  # noqa: E501
        :type: list[BorrowerPool]
        """
        if pools is None:
            raise ValueError("Invalid value for `pools`, must not be `None`")  # noqa: E501

        self._pools = pools

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
        if issubclass(BorrowerDetails, dict):
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
        if not isinstance(other, BorrowerDetails):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other

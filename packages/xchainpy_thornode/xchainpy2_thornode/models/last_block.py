# coding: utf-8

"""
    Thornode API

    Thornode REST API.  # noqa: E501

    OpenAPI spec version: 1.114.0
    Contact: devs@thorchain.org
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

import pprint
import re  # noqa: F401

import six

class LastBlock(object):
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
        'chain': 'str',
        'last_observed_in': 'int',
        'last_signed_out': 'int',
        'thorchain': 'int'
    }

    attribute_map = {
        'chain': 'chain',
        'last_observed_in': 'last_observed_in',
        'last_signed_out': 'last_signed_out',
        'thorchain': 'thorchain'
    }

    def __init__(self, chain=None, last_observed_in=None, last_signed_out=None, thorchain=None):  # noqa: E501
        """LastBlock - a model defined in Swagger"""  # noqa: E501
        self._chain = None
        self._last_observed_in = None
        self._last_signed_out = None
        self._thorchain = None
        self.discriminator = None
        self.chain = chain
        self.last_observed_in = last_observed_in
        self.last_signed_out = last_signed_out
        self.thorchain = thorchain

    @property
    def chain(self):
        """Gets the chain of this LastBlock.  # noqa: E501


        :return: The chain of this LastBlock.  # noqa: E501
        :rtype: str
        """
        return self._chain

    @chain.setter
    def chain(self, chain):
        """Sets the chain of this LastBlock.


        :param chain: The chain of this LastBlock.  # noqa: E501
        :type: str
        """
        if chain is None:
            raise ValueError("Invalid value for `chain`, must not be `None`")  # noqa: E501

        self._chain = chain

    @property
    def last_observed_in(self):
        """Gets the last_observed_in of this LastBlock.  # noqa: E501


        :return: The last_observed_in of this LastBlock.  # noqa: E501
        :rtype: int
        """
        return self._last_observed_in

    @last_observed_in.setter
    def last_observed_in(self, last_observed_in):
        """Sets the last_observed_in of this LastBlock.


        :param last_observed_in: The last_observed_in of this LastBlock.  # noqa: E501
        :type: int
        """
        if last_observed_in is None:
            raise ValueError("Invalid value for `last_observed_in`, must not be `None`")  # noqa: E501

        self._last_observed_in = last_observed_in

    @property
    def last_signed_out(self):
        """Gets the last_signed_out of this LastBlock.  # noqa: E501


        :return: The last_signed_out of this LastBlock.  # noqa: E501
        :rtype: int
        """
        return self._last_signed_out

    @last_signed_out.setter
    def last_signed_out(self, last_signed_out):
        """Sets the last_signed_out of this LastBlock.


        :param last_signed_out: The last_signed_out of this LastBlock.  # noqa: E501
        :type: int
        """
        if last_signed_out is None:
            raise ValueError("Invalid value for `last_signed_out`, must not be `None`")  # noqa: E501

        self._last_signed_out = last_signed_out

    @property
    def thorchain(self):
        """Gets the thorchain of this LastBlock.  # noqa: E501


        :return: The thorchain of this LastBlock.  # noqa: E501
        :rtype: int
        """
        return self._thorchain

    @thorchain.setter
    def thorchain(self, thorchain):
        """Sets the thorchain of this LastBlock.


        :param thorchain: The thorchain of this LastBlock.  # noqa: E501
        :type: int
        """
        if thorchain is None:
            raise ValueError("Invalid value for `thorchain`, must not be `None`")  # noqa: E501

        self._thorchain = thorchain

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
        if issubclass(LastBlock, dict):
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
        if not isinstance(other, LastBlock):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other

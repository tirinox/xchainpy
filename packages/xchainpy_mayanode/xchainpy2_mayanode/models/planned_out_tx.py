# coding: utf-8

"""
    Mayanode API

    Mayanode REST API.  # noqa: E501

    OpenAPI spec version: 1.112.0
    Contact: devs@mayachain.org
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

import pprint
import re  # noqa: F401

import six

class PlannedOutTx(object):
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
        'to_address': 'str',
        'coin': 'Coin',
        'refund': 'bool'
    }

    attribute_map = {
        'chain': 'chain',
        'to_address': 'to_address',
        'coin': 'coin',
        'refund': 'refund'
    }

    def __init__(self, chain=None, to_address=None, coin=None, refund=None):  # noqa: E501
        """PlannedOutTx - a model defined in Swagger"""  # noqa: E501
        self._chain = None
        self._to_address = None
        self._coin = None
        self._refund = None
        self.discriminator = None
        self.chain = chain
        self.to_address = to_address
        self.coin = coin
        self.refund = refund

    @property
    def chain(self):
        """Gets the chain of this PlannedOutTx.  # noqa: E501


        :return: The chain of this PlannedOutTx.  # noqa: E501
        :rtype: str
        """
        return self._chain

    @chain.setter
    def chain(self, chain):
        """Sets the chain of this PlannedOutTx.


        :param chain: The chain of this PlannedOutTx.  # noqa: E501
        :type: str
        """
        if chain is None:
            raise ValueError("Invalid value for `chain`, must not be `None`")  # noqa: E501

        self._chain = chain

    @property
    def to_address(self):
        """Gets the to_address of this PlannedOutTx.  # noqa: E501


        :return: The to_address of this PlannedOutTx.  # noqa: E501
        :rtype: str
        """
        return self._to_address

    @to_address.setter
    def to_address(self, to_address):
        """Sets the to_address of this PlannedOutTx.


        :param to_address: The to_address of this PlannedOutTx.  # noqa: E501
        :type: str
        """
        if to_address is None:
            raise ValueError("Invalid value for `to_address`, must not be `None`")  # noqa: E501

        self._to_address = to_address

    @property
    def coin(self):
        """Gets the coin of this PlannedOutTx.  # noqa: E501


        :return: The coin of this PlannedOutTx.  # noqa: E501
        :rtype: Coin
        """
        return self._coin

    @coin.setter
    def coin(self, coin):
        """Sets the coin of this PlannedOutTx.


        :param coin: The coin of this PlannedOutTx.  # noqa: E501
        :type: Coin
        """
        if coin is None:
            raise ValueError("Invalid value for `coin`, must not be `None`")  # noqa: E501

        self._coin = coin

    @property
    def refund(self):
        """Gets the refund of this PlannedOutTx.  # noqa: E501

        returns true if the planned transaction has a refund memo  # noqa: E501

        :return: The refund of this PlannedOutTx.  # noqa: E501
        :rtype: bool
        """
        return self._refund

    @refund.setter
    def refund(self, refund):
        """Sets the refund of this PlannedOutTx.

        returns true if the planned transaction has a refund memo  # noqa: E501

        :param refund: The refund of this PlannedOutTx.  # noqa: E501
        :type: bool
        """
        if refund is None:
            raise ValueError("Invalid value for `refund`, must not be `None`")  # noqa: E501

        self._refund = refund

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
        if issubclass(PlannedOutTx, dict):
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
        if not isinstance(other, PlannedOutTx):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other

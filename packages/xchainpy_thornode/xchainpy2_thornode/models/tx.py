# coding: utf-8

"""
    Thornode API

    Thornode REST API.  # noqa: E501

    OpenAPI spec version: 1.121.0
    Contact: devs@thorchain.org
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

import pprint
import re  # noqa: F401

import six

class Tx(object):
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
        'id': 'str',
        'chain': 'str',
        'from_address': 'str',
        'to_address': 'str',
        'coins': 'list[Coin]',
        'gas': 'list[Coin]',
        'memo': 'str'
    }

    attribute_map = {
        'id': 'id',
        'chain': 'chain',
        'from_address': 'from_address',
        'to_address': 'to_address',
        'coins': 'coins',
        'gas': 'gas',
        'memo': 'memo'
    }

    def __init__(self, id=None, chain=None, from_address=None, to_address=None, coins=None, gas=None, memo=None):  # noqa: E501
        """Tx - a model defined in Swagger"""  # noqa: E501
        self._id = None
        self._chain = None
        self._from_address = None
        self._to_address = None
        self._coins = None
        self._gas = None
        self._memo = None
        self.discriminator = None
        if id is not None:
            self.id = id
        if chain is not None:
            self.chain = chain
        if from_address is not None:
            self.from_address = from_address
        if to_address is not None:
            self.to_address = to_address
        self.coins = coins
        self.gas = gas
        if memo is not None:
            self.memo = memo

    @property
    def id(self):
        """Gets the id of this Tx.  # noqa: E501


        :return: The id of this Tx.  # noqa: E501
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this Tx.


        :param id: The id of this Tx.  # noqa: E501
        :type: str
        """

        self._id = id

    @property
    def chain(self):
        """Gets the chain of this Tx.  # noqa: E501


        :return: The chain of this Tx.  # noqa: E501
        :rtype: str
        """
        return self._chain

    @chain.setter
    def chain(self, chain):
        """Sets the chain of this Tx.


        :param chain: The chain of this Tx.  # noqa: E501
        :type: str
        """

        self._chain = chain

    @property
    def from_address(self):
        """Gets the from_address of this Tx.  # noqa: E501


        :return: The from_address of this Tx.  # noqa: E501
        :rtype: str
        """
        return self._from_address

    @from_address.setter
    def from_address(self, from_address):
        """Sets the from_address of this Tx.


        :param from_address: The from_address of this Tx.  # noqa: E501
        :type: str
        """

        self._from_address = from_address

    @property
    def to_address(self):
        """Gets the to_address of this Tx.  # noqa: E501


        :return: The to_address of this Tx.  # noqa: E501
        :rtype: str
        """
        return self._to_address

    @to_address.setter
    def to_address(self, to_address):
        """Sets the to_address of this Tx.


        :param to_address: The to_address of this Tx.  # noqa: E501
        :type: str
        """

        self._to_address = to_address

    @property
    def coins(self):
        """Gets the coins of this Tx.  # noqa: E501


        :return: The coins of this Tx.  # noqa: E501
        :rtype: list[Coin]
        """
        return self._coins

    @coins.setter
    def coins(self, coins):
        """Sets the coins of this Tx.


        :param coins: The coins of this Tx.  # noqa: E501
        :type: list[Coin]
        """
        if coins is None:
            raise ValueError("Invalid value for `coins`, must not be `None`")  # noqa: E501

        self._coins = coins

    @property
    def gas(self):
        """Gets the gas of this Tx.  # noqa: E501


        :return: The gas of this Tx.  # noqa: E501
        :rtype: list[Coin]
        """
        return self._gas

    @gas.setter
    def gas(self, gas):
        """Sets the gas of this Tx.


        :param gas: The gas of this Tx.  # noqa: E501
        :type: list[Coin]
        """
        if gas is None:
            raise ValueError("Invalid value for `gas`, must not be `None`")  # noqa: E501

        self._gas = gas

    @property
    def memo(self):
        """Gets the memo of this Tx.  # noqa: E501


        :return: The memo of this Tx.  # noqa: E501
        :rtype: str
        """
        return self._memo

    @memo.setter
    def memo(self, memo):
        """Sets the memo of this Tx.


        :param memo: The memo of this Tx.  # noqa: E501
        :type: str
        """

        self._memo = memo

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
        if issubclass(Tx, dict):
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
        if not isinstance(other, Tx):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other

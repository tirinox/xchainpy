# coding: utf-8

"""
    Thornode API

    Thornode REST API.  # noqa: E501

    OpenAPI spec version: 1.127.0
    Contact: devs@thorchain.org
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

import pprint
import re  # noqa: F401

import six

class BlockTx(object):
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
        'hash': 'str',
        'tx': 'dict(str, object)',
        'result': 'BlockTxResult'
    }

    attribute_map = {
        'hash': 'hash',
        'tx': 'tx',
        'result': 'result'
    }

    def __init__(self, hash=None, tx=None, result=None):  # noqa: E501
        """BlockTx - a model defined in Swagger"""  # noqa: E501
        self._hash = None
        self._tx = None
        self._result = None
        self.discriminator = None
        self.hash = hash
        self.tx = tx
        self.result = result

    @property
    def hash(self):
        """Gets the hash of this BlockTx.  # noqa: E501


        :return: The hash of this BlockTx.  # noqa: E501
        :rtype: str
        """
        return self._hash

    @hash.setter
    def hash(self, hash):
        """Sets the hash of this BlockTx.


        :param hash: The hash of this BlockTx.  # noqa: E501
        :type: str
        """
        if hash is None:
            raise ValueError("Invalid value for `hash`, must not be `None`")  # noqa: E501

        self._hash = hash

    @property
    def tx(self):
        """Gets the tx of this BlockTx.  # noqa: E501


        :return: The tx of this BlockTx.  # noqa: E501
        :rtype: dict(str, object)
        """
        return self._tx

    @tx.setter
    def tx(self, tx):
        """Sets the tx of this BlockTx.


        :param tx: The tx of this BlockTx.  # noqa: E501
        :type: dict(str, object)
        """
        if tx is None:
            raise ValueError("Invalid value for `tx`, must not be `None`")  # noqa: E501

        self._tx = tx

    @property
    def result(self):
        """Gets the result of this BlockTx.  # noqa: E501


        :return: The result of this BlockTx.  # noqa: E501
        :rtype: BlockTxResult
        """
        return self._result

    @result.setter
    def result(self, result):
        """Sets the result of this BlockTx.


        :param result: The result of this BlockTx.  # noqa: E501
        :type: BlockTxResult
        """
        if result is None:
            raise ValueError("Invalid value for `result`, must not be `None`")  # noqa: E501

        self._result = result

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
        if issubclass(BlockTx, dict):
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
        if not isinstance(other, BlockTx):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other

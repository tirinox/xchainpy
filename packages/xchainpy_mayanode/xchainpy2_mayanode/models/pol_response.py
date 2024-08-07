# coding: utf-8

"""
    Mayanode API

    Mayanode REST API.  # noqa: E501

    OpenAPI spec version: 1.110.0
    Contact: devs@mayachain.org
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

import pprint
import re  # noqa: F401

import six

class POLResponse(object):
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
        'cacao_deposited': 'str',
        'cacao_withdrawn': 'str',
        'value': 'str',
        'pnl': 'str',
        'current_deposit': 'str'
    }

    attribute_map = {
        'cacao_deposited': 'cacao_deposited',
        'cacao_withdrawn': 'cacao_withdrawn',
        'value': 'value',
        'pnl': 'pnl',
        'current_deposit': 'current_deposit'
    }

    def __init__(self, cacao_deposited=None, cacao_withdrawn=None, value=None, pnl=None, current_deposit=None):  # noqa: E501
        """POLResponse - a model defined in Swagger"""  # noqa: E501
        self._cacao_deposited = None
        self._cacao_withdrawn = None
        self._value = None
        self._pnl = None
        self._current_deposit = None
        self.discriminator = None
        self.cacao_deposited = cacao_deposited
        self.cacao_withdrawn = cacao_withdrawn
        self.value = value
        self.pnl = pnl
        self.current_deposit = current_deposit

    @property
    def cacao_deposited(self):
        """Gets the cacao_deposited of this POLResponse.  # noqa: E501

        total amount of CACAO deposited into the pools  # noqa: E501

        :return: The cacao_deposited of this POLResponse.  # noqa: E501
        :rtype: str
        """
        return self._cacao_deposited

    @cacao_deposited.setter
    def cacao_deposited(self, cacao_deposited):
        """Sets the cacao_deposited of this POLResponse.

        total amount of CACAO deposited into the pools  # noqa: E501

        :param cacao_deposited: The cacao_deposited of this POLResponse.  # noqa: E501
        :type: str
        """
        if cacao_deposited is None:
            raise ValueError("Invalid value for `cacao_deposited`, must not be `None`")  # noqa: E501

        self._cacao_deposited = cacao_deposited

    @property
    def cacao_withdrawn(self):
        """Gets the cacao_withdrawn of this POLResponse.  # noqa: E501

        total amount of CACAO withdrawn from the pools  # noqa: E501

        :return: The cacao_withdrawn of this POLResponse.  # noqa: E501
        :rtype: str
        """
        return self._cacao_withdrawn

    @cacao_withdrawn.setter
    def cacao_withdrawn(self, cacao_withdrawn):
        """Sets the cacao_withdrawn of this POLResponse.

        total amount of CACAO withdrawn from the pools  # noqa: E501

        :param cacao_withdrawn: The cacao_withdrawn of this POLResponse.  # noqa: E501
        :type: str
        """
        if cacao_withdrawn is None:
            raise ValueError("Invalid value for `cacao_withdrawn`, must not be `None`")  # noqa: E501

        self._cacao_withdrawn = cacao_withdrawn

    @property
    def value(self):
        """Gets the value of this POLResponse.  # noqa: E501

        total value of protocol's LP position in CACAO value  # noqa: E501

        :return: The value of this POLResponse.  # noqa: E501
        :rtype: str
        """
        return self._value

    @value.setter
    def value(self, value):
        """Sets the value of this POLResponse.

        total value of protocol's LP position in CACAO value  # noqa: E501

        :param value: The value of this POLResponse.  # noqa: E501
        :type: str
        """
        if value is None:
            raise ValueError("Invalid value for `value`, must not be `None`")  # noqa: E501

        self._value = value

    @property
    def pnl(self):
        """Gets the pnl of this POLResponse.  # noqa: E501

        profit and loss of protocol owned liquidity  # noqa: E501

        :return: The pnl of this POLResponse.  # noqa: E501
        :rtype: str
        """
        return self._pnl

    @pnl.setter
    def pnl(self, pnl):
        """Sets the pnl of this POLResponse.

        profit and loss of protocol owned liquidity  # noqa: E501

        :param pnl: The pnl of this POLResponse.  # noqa: E501
        :type: str
        """
        if pnl is None:
            raise ValueError("Invalid value for `pnl`, must not be `None`")  # noqa: E501

        self._pnl = pnl

    @property
    def current_deposit(self):
        """Gets the current_deposit of this POLResponse.  # noqa: E501

        current amount of cacao deposited  # noqa: E501

        :return: The current_deposit of this POLResponse.  # noqa: E501
        :rtype: str
        """
        return self._current_deposit

    @current_deposit.setter
    def current_deposit(self, current_deposit):
        """Sets the current_deposit of this POLResponse.

        current amount of cacao deposited  # noqa: E501

        :param current_deposit: The current_deposit of this POLResponse.  # noqa: E501
        :type: str
        """
        if current_deposit is None:
            raise ValueError("Invalid value for `current_deposit`, must not be `None`")  # noqa: E501

        self._current_deposit = current_deposit

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
        if issubclass(POLResponse, dict):
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
        if not isinstance(other, POLResponse):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other

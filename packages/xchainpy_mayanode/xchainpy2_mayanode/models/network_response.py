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

class NetworkResponse(object):
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
        'bond_reward_cacao': 'str',
        'total_bond_units': 'str',
        'total_reserve': 'str',
        'total_asgard': 'str',
        'gas_spent_cacao': 'str',
        'gas_withheld_cacao': 'str',
        'outbound_fee_multiplier': 'str'
    }

    attribute_map = {
        'bond_reward_cacao': 'bond_reward_cacao',
        'total_bond_units': 'total_bond_units',
        'total_reserve': 'total_reserve',
        'total_asgard': 'total_asgard',
        'gas_spent_cacao': 'gas_spent_cacao',
        'gas_withheld_cacao': 'gas_withheld_cacao',
        'outbound_fee_multiplier': 'outbound_fee_multiplier'
    }

    def __init__(self, bond_reward_cacao=None, total_bond_units=None, total_reserve=None, total_asgard=None, gas_spent_cacao=None, gas_withheld_cacao=None, outbound_fee_multiplier=None):  # noqa: E501
        """NetworkResponse - a model defined in Swagger"""  # noqa: E501
        self._bond_reward_cacao = None
        self._total_bond_units = None
        self._total_reserve = None
        self._total_asgard = None
        self._gas_spent_cacao = None
        self._gas_withheld_cacao = None
        self._outbound_fee_multiplier = None
        self.discriminator = None
        self.bond_reward_cacao = bond_reward_cacao
        self.total_bond_units = total_bond_units
        self.total_reserve = total_reserve
        self.total_asgard = total_asgard
        self.gas_spent_cacao = gas_spent_cacao
        self.gas_withheld_cacao = gas_withheld_cacao
        if outbound_fee_multiplier is not None:
            self.outbound_fee_multiplier = outbound_fee_multiplier

    @property
    def bond_reward_cacao(self):
        """Gets the bond_reward_cacao of this NetworkResponse.  # noqa: E501

        total amount of cacao awarded to node operators  # noqa: E501

        :return: The bond_reward_cacao of this NetworkResponse.  # noqa: E501
        :rtype: str
        """
        return self._bond_reward_cacao

    @bond_reward_cacao.setter
    def bond_reward_cacao(self, bond_reward_cacao):
        """Sets the bond_reward_cacao of this NetworkResponse.

        total amount of cacao awarded to node operators  # noqa: E501

        :param bond_reward_cacao: The bond_reward_cacao of this NetworkResponse.  # noqa: E501
        :type: str
        """
        if bond_reward_cacao is None:
            raise ValueError("Invalid value for `bond_reward_cacao`, must not be `None`")  # noqa: E501

        self._bond_reward_cacao = bond_reward_cacao

    @property
    def total_bond_units(self):
        """Gets the total_bond_units of this NetworkResponse.  # noqa: E501

        total bonded cacao  # noqa: E501

        :return: The total_bond_units of this NetworkResponse.  # noqa: E501
        :rtype: str
        """
        return self._total_bond_units

    @total_bond_units.setter
    def total_bond_units(self, total_bond_units):
        """Sets the total_bond_units of this NetworkResponse.

        total bonded cacao  # noqa: E501

        :param total_bond_units: The total_bond_units of this NetworkResponse.  # noqa: E501
        :type: str
        """
        if total_bond_units is None:
            raise ValueError("Invalid value for `total_bond_units`, must not be `None`")  # noqa: E501

        self._total_bond_units = total_bond_units

    @property
    def total_reserve(self):
        """Gets the total_reserve of this NetworkResponse.  # noqa: E501

        total reserve cacao  # noqa: E501

        :return: The total_reserve of this NetworkResponse.  # noqa: E501
        :rtype: str
        """
        return self._total_reserve

    @total_reserve.setter
    def total_reserve(self, total_reserve):
        """Sets the total_reserve of this NetworkResponse.

        total reserve cacao  # noqa: E501

        :param total_reserve: The total_reserve of this NetworkResponse.  # noqa: E501
        :type: str
        """
        if total_reserve is None:
            raise ValueError("Invalid value for `total_reserve`, must not be `None`")  # noqa: E501

        self._total_reserve = total_reserve

    @property
    def total_asgard(self):
        """Gets the total_asgard of this NetworkResponse.  # noqa: E501

        total asgard cacao  # noqa: E501

        :return: The total_asgard of this NetworkResponse.  # noqa: E501
        :rtype: str
        """
        return self._total_asgard

    @total_asgard.setter
    def total_asgard(self, total_asgard):
        """Sets the total_asgard of this NetworkResponse.

        total asgard cacao  # noqa: E501

        :param total_asgard: The total_asgard of this NetworkResponse.  # noqa: E501
        :type: str
        """
        if total_asgard is None:
            raise ValueError("Invalid value for `total_asgard`, must not be `None`")  # noqa: E501

        self._total_asgard = total_asgard

    @property
    def gas_spent_cacao(self):
        """Gets the gas_spent_cacao of this NetworkResponse.  # noqa: E501

        Sum of the gas the network has spent to send outbounds  # noqa: E501

        :return: The gas_spent_cacao of this NetworkResponse.  # noqa: E501
        :rtype: str
        """
        return self._gas_spent_cacao

    @gas_spent_cacao.setter
    def gas_spent_cacao(self, gas_spent_cacao):
        """Sets the gas_spent_cacao of this NetworkResponse.

        Sum of the gas the network has spent to send outbounds  # noqa: E501

        :param gas_spent_cacao: The gas_spent_cacao of this NetworkResponse.  # noqa: E501
        :type: str
        """
        if gas_spent_cacao is None:
            raise ValueError("Invalid value for `gas_spent_cacao`, must not be `None`")  # noqa: E501

        self._gas_spent_cacao = gas_spent_cacao

    @property
    def gas_withheld_cacao(self):
        """Gets the gas_withheld_cacao of this NetworkResponse.  # noqa: E501

        Sum of the gas withheld from users to cover outbound gas  # noqa: E501

        :return: The gas_withheld_cacao of this NetworkResponse.  # noqa: E501
        :rtype: str
        """
        return self._gas_withheld_cacao

    @gas_withheld_cacao.setter
    def gas_withheld_cacao(self, gas_withheld_cacao):
        """Sets the gas_withheld_cacao of this NetworkResponse.

        Sum of the gas withheld from users to cover outbound gas  # noqa: E501

        :param gas_withheld_cacao: The gas_withheld_cacao of this NetworkResponse.  # noqa: E501
        :type: str
        """
        if gas_withheld_cacao is None:
            raise ValueError("Invalid value for `gas_withheld_cacao`, must not be `None`")  # noqa: E501

        self._gas_withheld_cacao = gas_withheld_cacao

    @property
    def outbound_fee_multiplier(self):
        """Gets the outbound_fee_multiplier of this NetworkResponse.  # noqa: E501

        Current outbound fee multiplier, in basis points  # noqa: E501

        :return: The outbound_fee_multiplier of this NetworkResponse.  # noqa: E501
        :rtype: str
        """
        return self._outbound_fee_multiplier

    @outbound_fee_multiplier.setter
    def outbound_fee_multiplier(self, outbound_fee_multiplier):
        """Sets the outbound_fee_multiplier of this NetworkResponse.

        Current outbound fee multiplier, in basis points  # noqa: E501

        :param outbound_fee_multiplier: The outbound_fee_multiplier of this NetworkResponse.  # noqa: E501
        :type: str
        """

        self._outbound_fee_multiplier = outbound_fee_multiplier

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
        if issubclass(NetworkResponse, dict):
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
        if not isinstance(other, NetworkResponse):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other

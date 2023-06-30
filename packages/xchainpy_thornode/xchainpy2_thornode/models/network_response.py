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
        'bond_reward_rune': 'str',
        'burned_bep_2_rune': 'str',
        'burned_erc_20_rune': 'str',
        'total_bond_units': 'str',
        'total_reserve': 'str',
        'vaults_migrating': 'bool',
        'gas_spent_rune': 'str',
        'gas_withheld_rune': 'str',
        'outbound_fee_multiplier': 'str',
        'outbound_tx_fee_rune': 'str',
        'native_tx_fee_rune': 'str',
        'tns_register_fee_rune': 'str',
        'tns_fee_per_block_rune': 'str'
    }

    attribute_map = {
        'bond_reward_rune': 'bond_reward_rune',
        'burned_bep_2_rune': 'burned_bep_2_rune',
        'burned_erc_20_rune': 'burned_erc_20_rune',
        'total_bond_units': 'total_bond_units',
        'total_reserve': 'total_reserve',
        'vaults_migrating': 'vaults_migrating',
        'gas_spent_rune': 'gas_spent_rune',
        'gas_withheld_rune': 'gas_withheld_rune',
        'outbound_fee_multiplier': 'outbound_fee_multiplier',
        'outbound_tx_fee_rune': 'outbound_tx_fee_rune',
        'native_tx_fee_rune': 'native_tx_fee_rune',
        'tns_register_fee_rune': 'tns_register_fee_rune',
        'tns_fee_per_block_rune': 'tns_fee_per_block_rune'
    }

    def __init__(self, bond_reward_rune=None, burned_bep_2_rune=None, burned_erc_20_rune=None, total_bond_units=None, total_reserve=None, vaults_migrating=None, gas_spent_rune=None, gas_withheld_rune=None, outbound_fee_multiplier=None, outbound_tx_fee_rune=None, native_tx_fee_rune=None, tns_register_fee_rune=None, tns_fee_per_block_rune=None):  # noqa: E501
        """NetworkResponse - a model defined in Swagger"""  # noqa: E501
        self._bond_reward_rune = None
        self._burned_bep_2_rune = None
        self._burned_erc_20_rune = None
        self._total_bond_units = None
        self._total_reserve = None
        self._vaults_migrating = None
        self._gas_spent_rune = None
        self._gas_withheld_rune = None
        self._outbound_fee_multiplier = None
        self._outbound_tx_fee_rune = None
        self._native_tx_fee_rune = None
        self._tns_register_fee_rune = None
        self._tns_fee_per_block_rune = None
        self.discriminator = None
        self.bond_reward_rune = bond_reward_rune
        self.burned_bep_2_rune = burned_bep_2_rune
        self.burned_erc_20_rune = burned_erc_20_rune
        self.total_bond_units = total_bond_units
        self.total_reserve = total_reserve
        self.vaults_migrating = vaults_migrating
        self.gas_spent_rune = gas_spent_rune
        self.gas_withheld_rune = gas_withheld_rune
        if outbound_fee_multiplier is not None:
            self.outbound_fee_multiplier = outbound_fee_multiplier
        self.outbound_tx_fee_rune = outbound_tx_fee_rune
        self.native_tx_fee_rune = native_tx_fee_rune
        self.tns_register_fee_rune = tns_register_fee_rune
        self.tns_fee_per_block_rune = tns_fee_per_block_rune

    @property
    def bond_reward_rune(self):
        """Gets the bond_reward_rune of this NetworkResponse.  # noqa: E501

        total amount of RUNE awarded to node operators  # noqa: E501

        :return: The bond_reward_rune of this NetworkResponse.  # noqa: E501
        :rtype: str
        """
        return self._bond_reward_rune

    @bond_reward_rune.setter
    def bond_reward_rune(self, bond_reward_rune):
        """Sets the bond_reward_rune of this NetworkResponse.

        total amount of RUNE awarded to node operators  # noqa: E501

        :param bond_reward_rune: The bond_reward_rune of this NetworkResponse.  # noqa: E501
        :type: str
        """
        if bond_reward_rune is None:
            raise ValueError("Invalid value for `bond_reward_rune`, must not be `None`")  # noqa: E501

        self._bond_reward_rune = bond_reward_rune

    @property
    def burned_bep_2_rune(self):
        """Gets the burned_bep_2_rune of this NetworkResponse.  # noqa: E501

        total of burned BEP2 RUNE  # noqa: E501

        :return: The burned_bep_2_rune of this NetworkResponse.  # noqa: E501
        :rtype: str
        """
        return self._burned_bep_2_rune

    @burned_bep_2_rune.setter
    def burned_bep_2_rune(self, burned_bep_2_rune):
        """Sets the burned_bep_2_rune of this NetworkResponse.

        total of burned BEP2 RUNE  # noqa: E501

        :param burned_bep_2_rune: The burned_bep_2_rune of this NetworkResponse.  # noqa: E501
        :type: str
        """
        if burned_bep_2_rune is None:
            raise ValueError("Invalid value for `burned_bep_2_rune`, must not be `None`")  # noqa: E501

        self._burned_bep_2_rune = burned_bep_2_rune

    @property
    def burned_erc_20_rune(self):
        """Gets the burned_erc_20_rune of this NetworkResponse.  # noqa: E501

        total of burned ERC20 RUNE  # noqa: E501

        :return: The burned_erc_20_rune of this NetworkResponse.  # noqa: E501
        :rtype: str
        """
        return self._burned_erc_20_rune

    @burned_erc_20_rune.setter
    def burned_erc_20_rune(self, burned_erc_20_rune):
        """Sets the burned_erc_20_rune of this NetworkResponse.

        total of burned ERC20 RUNE  # noqa: E501

        :param burned_erc_20_rune: The burned_erc_20_rune of this NetworkResponse.  # noqa: E501
        :type: str
        """
        if burned_erc_20_rune is None:
            raise ValueError("Invalid value for `burned_erc_20_rune`, must not be `None`")  # noqa: E501

        self._burned_erc_20_rune = burned_erc_20_rune

    @property
    def total_bond_units(self):
        """Gets the total_bond_units of this NetworkResponse.  # noqa: E501

        total bonded RUNE  # noqa: E501

        :return: The total_bond_units of this NetworkResponse.  # noqa: E501
        :rtype: str
        """
        return self._total_bond_units

    @total_bond_units.setter
    def total_bond_units(self, total_bond_units):
        """Sets the total_bond_units of this NetworkResponse.

        total bonded RUNE  # noqa: E501

        :param total_bond_units: The total_bond_units of this NetworkResponse.  # noqa: E501
        :type: str
        """
        if total_bond_units is None:
            raise ValueError("Invalid value for `total_bond_units`, must not be `None`")  # noqa: E501

        self._total_bond_units = total_bond_units

    @property
    def total_reserve(self):
        """Gets the total_reserve of this NetworkResponse.  # noqa: E501

        total reserve RUNE  # noqa: E501

        :return: The total_reserve of this NetworkResponse.  # noqa: E501
        :rtype: str
        """
        return self._total_reserve

    @total_reserve.setter
    def total_reserve(self, total_reserve):
        """Sets the total_reserve of this NetworkResponse.

        total reserve RUNE  # noqa: E501

        :param total_reserve: The total_reserve of this NetworkResponse.  # noqa: E501
        :type: str
        """
        if total_reserve is None:
            raise ValueError("Invalid value for `total_reserve`, must not be `None`")  # noqa: E501

        self._total_reserve = total_reserve

    @property
    def vaults_migrating(self):
        """Gets the vaults_migrating of this NetworkResponse.  # noqa: E501

        Returns true if there exist RetiringVaults which have not finished migrating funds to new ActiveVaults  # noqa: E501

        :return: The vaults_migrating of this NetworkResponse.  # noqa: E501
        :rtype: bool
        """
        return self._vaults_migrating

    @vaults_migrating.setter
    def vaults_migrating(self, vaults_migrating):
        """Sets the vaults_migrating of this NetworkResponse.

        Returns true if there exist RetiringVaults which have not finished migrating funds to new ActiveVaults  # noqa: E501

        :param vaults_migrating: The vaults_migrating of this NetworkResponse.  # noqa: E501
        :type: bool
        """
        if vaults_migrating is None:
            raise ValueError("Invalid value for `vaults_migrating`, must not be `None`")  # noqa: E501

        self._vaults_migrating = vaults_migrating

    @property
    def gas_spent_rune(self):
        """Gets the gas_spent_rune of this NetworkResponse.  # noqa: E501

        Sum of the gas the network has spent to send outbounds  # noqa: E501

        :return: The gas_spent_rune of this NetworkResponse.  # noqa: E501
        :rtype: str
        """
        return self._gas_spent_rune

    @gas_spent_rune.setter
    def gas_spent_rune(self, gas_spent_rune):
        """Sets the gas_spent_rune of this NetworkResponse.

        Sum of the gas the network has spent to send outbounds  # noqa: E501

        :param gas_spent_rune: The gas_spent_rune of this NetworkResponse.  # noqa: E501
        :type: str
        """
        if gas_spent_rune is None:
            raise ValueError("Invalid value for `gas_spent_rune`, must not be `None`")  # noqa: E501

        self._gas_spent_rune = gas_spent_rune

    @property
    def gas_withheld_rune(self):
        """Gets the gas_withheld_rune of this NetworkResponse.  # noqa: E501

        Sum of the gas withheld from users to cover outbound gas  # noqa: E501

        :return: The gas_withheld_rune of this NetworkResponse.  # noqa: E501
        :rtype: str
        """
        return self._gas_withheld_rune

    @gas_withheld_rune.setter
    def gas_withheld_rune(self, gas_withheld_rune):
        """Sets the gas_withheld_rune of this NetworkResponse.

        Sum of the gas withheld from users to cover outbound gas  # noqa: E501

        :param gas_withheld_rune: The gas_withheld_rune of this NetworkResponse.  # noqa: E501
        :type: str
        """
        if gas_withheld_rune is None:
            raise ValueError("Invalid value for `gas_withheld_rune`, must not be `None`")  # noqa: E501

        self._gas_withheld_rune = gas_withheld_rune

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

    @property
    def outbound_tx_fee_rune(self):
        """Gets the outbound_tx_fee_rune of this NetworkResponse.  # noqa: E501

        the outbound transaction fee in rune, converted from the OutboundTransactionFeeUSD mimir  # noqa: E501

        :return: The outbound_tx_fee_rune of this NetworkResponse.  # noqa: E501
        :rtype: str
        """
        return self._outbound_tx_fee_rune

    @outbound_tx_fee_rune.setter
    def outbound_tx_fee_rune(self, outbound_tx_fee_rune):
        """Sets the outbound_tx_fee_rune of this NetworkResponse.

        the outbound transaction fee in rune, converted from the OutboundTransactionFeeUSD mimir  # noqa: E501

        :param outbound_tx_fee_rune: The outbound_tx_fee_rune of this NetworkResponse.  # noqa: E501
        :type: str
        """
        if outbound_tx_fee_rune is None:
            raise ValueError("Invalid value for `outbound_tx_fee_rune`, must not be `None`")  # noqa: E501

        self._outbound_tx_fee_rune = outbound_tx_fee_rune

    @property
    def native_tx_fee_rune(self):
        """Gets the native_tx_fee_rune of this NetworkResponse.  # noqa: E501

        the native transaction fee in rune, converted from the NativeTransactionFeeUSD mimir  # noqa: E501

        :return: The native_tx_fee_rune of this NetworkResponse.  # noqa: E501
        :rtype: str
        """
        return self._native_tx_fee_rune

    @native_tx_fee_rune.setter
    def native_tx_fee_rune(self, native_tx_fee_rune):
        """Sets the native_tx_fee_rune of this NetworkResponse.

        the native transaction fee in rune, converted from the NativeTransactionFeeUSD mimir  # noqa: E501

        :param native_tx_fee_rune: The native_tx_fee_rune of this NetworkResponse.  # noqa: E501
        :type: str
        """
        if native_tx_fee_rune is None:
            raise ValueError("Invalid value for `native_tx_fee_rune`, must not be `None`")  # noqa: E501

        self._native_tx_fee_rune = native_tx_fee_rune

    @property
    def tns_register_fee_rune(self):
        """Gets the tns_register_fee_rune of this NetworkResponse.  # noqa: E501

        the thorname register fee in rune, converted from the TNSRegisterFeeUSD mimir  # noqa: E501

        :return: The tns_register_fee_rune of this NetworkResponse.  # noqa: E501
        :rtype: str
        """
        return self._tns_register_fee_rune

    @tns_register_fee_rune.setter
    def tns_register_fee_rune(self, tns_register_fee_rune):
        """Sets the tns_register_fee_rune of this NetworkResponse.

        the thorname register fee in rune, converted from the TNSRegisterFeeUSD mimir  # noqa: E501

        :param tns_register_fee_rune: The tns_register_fee_rune of this NetworkResponse.  # noqa: E501
        :type: str
        """
        if tns_register_fee_rune is None:
            raise ValueError("Invalid value for `tns_register_fee_rune`, must not be `None`")  # noqa: E501

        self._tns_register_fee_rune = tns_register_fee_rune

    @property
    def tns_fee_per_block_rune(self):
        """Gets the tns_fee_per_block_rune of this NetworkResponse.  # noqa: E501

        the thorname fee per block in rune, converted from the TNSFeePerBlockUSD mimir  # noqa: E501

        :return: The tns_fee_per_block_rune of this NetworkResponse.  # noqa: E501
        :rtype: str
        """
        return self._tns_fee_per_block_rune

    @tns_fee_per_block_rune.setter
    def tns_fee_per_block_rune(self, tns_fee_per_block_rune):
        """Sets the tns_fee_per_block_rune of this NetworkResponse.

        the thorname fee per block in rune, converted from the TNSFeePerBlockUSD mimir  # noqa: E501

        :param tns_fee_per_block_rune: The tns_fee_per_block_rune of this NetworkResponse.  # noqa: E501
        :type: str
        """
        if tns_fee_per_block_rune is None:
            raise ValueError("Invalid value for `tns_fee_per_block_rune`, must not be `None`")  # noqa: E501

        self._tns_fee_per_block_rune = tns_fee_per_block_rune

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

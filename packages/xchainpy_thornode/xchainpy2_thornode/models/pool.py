# coding: utf-8

"""
    Thornode API

    Thornode REST API.  # noqa: E501

    OpenAPI spec version: 1.125.0
    Contact: devs@thorchain.org
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

import pprint
import re  # noqa: F401

import six

class Pool(object):
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
        'short_code': 'str',
        'status': 'str',
        'decimals': 'int',
        'pending_inbound_asset': 'str',
        'pending_inbound_rune': 'str',
        'balance_asset': 'str',
        'balance_rune': 'str',
        'pool_units': 'str',
        'lp_units': 'str',
        'synth_units': 'str',
        'synth_supply': 'str',
        'savers_depth': 'str',
        'savers_units': 'str',
        'synth_mint_paused': 'bool',
        'synth_supply_remaining': 'str',
        'loan_collateral': 'str',
        'loan_cr': 'str',
        'derived_depth_bps': 'str'
    }

    attribute_map = {
        'asset': 'asset',
        'short_code': 'short_code',
        'status': 'status',
        'decimals': 'decimals',
        'pending_inbound_asset': 'pending_inbound_asset',
        'pending_inbound_rune': 'pending_inbound_rune',
        'balance_asset': 'balance_asset',
        'balance_rune': 'balance_rune',
        'pool_units': 'pool_units',
        'lp_units': 'LP_units',
        'synth_units': 'synth_units',
        'synth_supply': 'synth_supply',
        'savers_depth': 'savers_depth',
        'savers_units': 'savers_units',
        'synth_mint_paused': 'synth_mint_paused',
        'synth_supply_remaining': 'synth_supply_remaining',
        'loan_collateral': 'loan_collateral',
        'loan_cr': 'loan_cr',
        'derived_depth_bps': 'derived_depth_bps'
    }

    def __init__(self, asset=None, short_code=None, status=None, decimals=None, pending_inbound_asset=None, pending_inbound_rune=None, balance_asset=None, balance_rune=None, pool_units=None, lp_units=None, synth_units=None, synth_supply=None, savers_depth=None, savers_units=None, synth_mint_paused=None, synth_supply_remaining=None, loan_collateral=None, loan_cr=None, derived_depth_bps=None):  # noqa: E501
        """Pool - a model defined in Swagger"""  # noqa: E501
        self._asset = None
        self._short_code = None
        self._status = None
        self._decimals = None
        self._pending_inbound_asset = None
        self._pending_inbound_rune = None
        self._balance_asset = None
        self._balance_rune = None
        self._pool_units = None
        self._lp_units = None
        self._synth_units = None
        self._synth_supply = None
        self._savers_depth = None
        self._savers_units = None
        self._synth_mint_paused = None
        self._synth_supply_remaining = None
        self._loan_collateral = None
        self._loan_cr = None
        self._derived_depth_bps = None
        self.discriminator = None
        self.asset = asset
        if short_code is not None:
            self.short_code = short_code
        self.status = status
        if decimals is not None:
            self.decimals = decimals
        self.pending_inbound_asset = pending_inbound_asset
        self.pending_inbound_rune = pending_inbound_rune
        self.balance_asset = balance_asset
        self.balance_rune = balance_rune
        self.pool_units = pool_units
        self.lp_units = lp_units
        self.synth_units = synth_units
        self.synth_supply = synth_supply
        self.savers_depth = savers_depth
        self.savers_units = savers_units
        self.synth_mint_paused = synth_mint_paused
        self.synth_supply_remaining = synth_supply_remaining
        self.loan_collateral = loan_collateral
        self.loan_cr = loan_cr
        self.derived_depth_bps = derived_depth_bps

    @property
    def asset(self):
        """Gets the asset of this Pool.  # noqa: E501


        :return: The asset of this Pool.  # noqa: E501
        :rtype: str
        """
        return self._asset

    @asset.setter
    def asset(self, asset):
        """Sets the asset of this Pool.


        :param asset: The asset of this Pool.  # noqa: E501
        :type: str
        """
        if asset is None:
            raise ValueError("Invalid value for `asset`, must not be `None`")  # noqa: E501

        self._asset = asset

    @property
    def short_code(self):
        """Gets the short_code of this Pool.  # noqa: E501


        :return: The short_code of this Pool.  # noqa: E501
        :rtype: str
        """
        return self._short_code

    @short_code.setter
    def short_code(self, short_code):
        """Sets the short_code of this Pool.


        :param short_code: The short_code of this Pool.  # noqa: E501
        :type: str
        """

        self._short_code = short_code

    @property
    def status(self):
        """Gets the status of this Pool.  # noqa: E501


        :return: The status of this Pool.  # noqa: E501
        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, status):
        """Sets the status of this Pool.


        :param status: The status of this Pool.  # noqa: E501
        :type: str
        """
        if status is None:
            raise ValueError("Invalid value for `status`, must not be `None`")  # noqa: E501

        self._status = status

    @property
    def decimals(self):
        """Gets the decimals of this Pool.  # noqa: E501


        :return: The decimals of this Pool.  # noqa: E501
        :rtype: int
        """
        return self._decimals

    @decimals.setter
    def decimals(self, decimals):
        """Sets the decimals of this Pool.


        :param decimals: The decimals of this Pool.  # noqa: E501
        :type: int
        """

        self._decimals = decimals

    @property
    def pending_inbound_asset(self):
        """Gets the pending_inbound_asset of this Pool.  # noqa: E501


        :return: The pending_inbound_asset of this Pool.  # noqa: E501
        :rtype: str
        """
        return self._pending_inbound_asset

    @pending_inbound_asset.setter
    def pending_inbound_asset(self, pending_inbound_asset):
        """Sets the pending_inbound_asset of this Pool.


        :param pending_inbound_asset: The pending_inbound_asset of this Pool.  # noqa: E501
        :type: str
        """
        if pending_inbound_asset is None:
            raise ValueError("Invalid value for `pending_inbound_asset`, must not be `None`")  # noqa: E501

        self._pending_inbound_asset = pending_inbound_asset

    @property
    def pending_inbound_rune(self):
        """Gets the pending_inbound_rune of this Pool.  # noqa: E501


        :return: The pending_inbound_rune of this Pool.  # noqa: E501
        :rtype: str
        """
        return self._pending_inbound_rune

    @pending_inbound_rune.setter
    def pending_inbound_rune(self, pending_inbound_rune):
        """Sets the pending_inbound_rune of this Pool.


        :param pending_inbound_rune: The pending_inbound_rune of this Pool.  # noqa: E501
        :type: str
        """
        if pending_inbound_rune is None:
            raise ValueError("Invalid value for `pending_inbound_rune`, must not be `None`")  # noqa: E501

        self._pending_inbound_rune = pending_inbound_rune

    @property
    def balance_asset(self):
        """Gets the balance_asset of this Pool.  # noqa: E501


        :return: The balance_asset of this Pool.  # noqa: E501
        :rtype: str
        """
        return self._balance_asset

    @balance_asset.setter
    def balance_asset(self, balance_asset):
        """Sets the balance_asset of this Pool.


        :param balance_asset: The balance_asset of this Pool.  # noqa: E501
        :type: str
        """
        if balance_asset is None:
            raise ValueError("Invalid value for `balance_asset`, must not be `None`")  # noqa: E501

        self._balance_asset = balance_asset

    @property
    def balance_rune(self):
        """Gets the balance_rune of this Pool.  # noqa: E501


        :return: The balance_rune of this Pool.  # noqa: E501
        :rtype: str
        """
        return self._balance_rune

    @balance_rune.setter
    def balance_rune(self, balance_rune):
        """Sets the balance_rune of this Pool.


        :param balance_rune: The balance_rune of this Pool.  # noqa: E501
        :type: str
        """
        if balance_rune is None:
            raise ValueError("Invalid value for `balance_rune`, must not be `None`")  # noqa: E501

        self._balance_rune = balance_rune

    @property
    def pool_units(self):
        """Gets the pool_units of this Pool.  # noqa: E501

        the total pool units, this is the sum of LP and synth units  # noqa: E501

        :return: The pool_units of this Pool.  # noqa: E501
        :rtype: str
        """
        return self._pool_units

    @pool_units.setter
    def pool_units(self, pool_units):
        """Sets the pool_units of this Pool.

        the total pool units, this is the sum of LP and synth units  # noqa: E501

        :param pool_units: The pool_units of this Pool.  # noqa: E501
        :type: str
        """
        if pool_units is None:
            raise ValueError("Invalid value for `pool_units`, must not be `None`")  # noqa: E501

        self._pool_units = pool_units

    @property
    def lp_units(self):
        """Gets the lp_units of this Pool.  # noqa: E501

        the total pool liquidity provider units  # noqa: E501

        :return: The lp_units of this Pool.  # noqa: E501
        :rtype: str
        """
        return self._lp_units

    @lp_units.setter
    def lp_units(self, lp_units):
        """Sets the lp_units of this Pool.

        the total pool liquidity provider units  # noqa: E501

        :param lp_units: The lp_units of this Pool.  # noqa: E501
        :type: str
        """
        if lp_units is None:
            raise ValueError("Invalid value for `lp_units`, must not be `None`")  # noqa: E501

        self._lp_units = lp_units

    @property
    def synth_units(self):
        """Gets the synth_units of this Pool.  # noqa: E501

        the total synth units in the pool  # noqa: E501

        :return: The synth_units of this Pool.  # noqa: E501
        :rtype: str
        """
        return self._synth_units

    @synth_units.setter
    def synth_units(self, synth_units):
        """Sets the synth_units of this Pool.

        the total synth units in the pool  # noqa: E501

        :param synth_units: The synth_units of this Pool.  # noqa: E501
        :type: str
        """
        if synth_units is None:
            raise ValueError("Invalid value for `synth_units`, must not be `None`")  # noqa: E501

        self._synth_units = synth_units

    @property
    def synth_supply(self):
        """Gets the synth_supply of this Pool.  # noqa: E501

        the total supply of synths for the asset  # noqa: E501

        :return: The synth_supply of this Pool.  # noqa: E501
        :rtype: str
        """
        return self._synth_supply

    @synth_supply.setter
    def synth_supply(self, synth_supply):
        """Sets the synth_supply of this Pool.

        the total supply of synths for the asset  # noqa: E501

        :param synth_supply: The synth_supply of this Pool.  # noqa: E501
        :type: str
        """
        if synth_supply is None:
            raise ValueError("Invalid value for `synth_supply`, must not be `None`")  # noqa: E501

        self._synth_supply = synth_supply

    @property
    def savers_depth(self):
        """Gets the savers_depth of this Pool.  # noqa: E501

        the balance of L1 asset deposited into the Savers Vault  # noqa: E501

        :return: The savers_depth of this Pool.  # noqa: E501
        :rtype: str
        """
        return self._savers_depth

    @savers_depth.setter
    def savers_depth(self, savers_depth):
        """Sets the savers_depth of this Pool.

        the balance of L1 asset deposited into the Savers Vault  # noqa: E501

        :param savers_depth: The savers_depth of this Pool.  # noqa: E501
        :type: str
        """
        if savers_depth is None:
            raise ValueError("Invalid value for `savers_depth`, must not be `None`")  # noqa: E501

        self._savers_depth = savers_depth

    @property
    def savers_units(self):
        """Gets the savers_units of this Pool.  # noqa: E501

        the number of units owned by Savers  # noqa: E501

        :return: The savers_units of this Pool.  # noqa: E501
        :rtype: str
        """
        return self._savers_units

    @savers_units.setter
    def savers_units(self, savers_units):
        """Sets the savers_units of this Pool.

        the number of units owned by Savers  # noqa: E501

        :param savers_units: The savers_units of this Pool.  # noqa: E501
        :type: str
        """
        if savers_units is None:
            raise ValueError("Invalid value for `savers_units`, must not be `None`")  # noqa: E501

        self._savers_units = savers_units

    @property
    def synth_mint_paused(self):
        """Gets the synth_mint_paused of this Pool.  # noqa: E501

        whether additional synths cannot be minted  # noqa: E501

        :return: The synth_mint_paused of this Pool.  # noqa: E501
        :rtype: bool
        """
        return self._synth_mint_paused

    @synth_mint_paused.setter
    def synth_mint_paused(self, synth_mint_paused):
        """Sets the synth_mint_paused of this Pool.

        whether additional synths cannot be minted  # noqa: E501

        :param synth_mint_paused: The synth_mint_paused of this Pool.  # noqa: E501
        :type: bool
        """
        if synth_mint_paused is None:
            raise ValueError("Invalid value for `synth_mint_paused`, must not be `None`")  # noqa: E501

        self._synth_mint_paused = synth_mint_paused

    @property
    def synth_supply_remaining(self):
        """Gets the synth_supply_remaining of this Pool.  # noqa: E501

        the amount of synth supply remaining before the current max supply is reached  # noqa: E501

        :return: The synth_supply_remaining of this Pool.  # noqa: E501
        :rtype: str
        """
        return self._synth_supply_remaining

    @synth_supply_remaining.setter
    def synth_supply_remaining(self, synth_supply_remaining):
        """Sets the synth_supply_remaining of this Pool.

        the amount of synth supply remaining before the current max supply is reached  # noqa: E501

        :param synth_supply_remaining: The synth_supply_remaining of this Pool.  # noqa: E501
        :type: str
        """
        if synth_supply_remaining is None:
            raise ValueError("Invalid value for `synth_supply_remaining`, must not be `None`")  # noqa: E501

        self._synth_supply_remaining = synth_supply_remaining

    @property
    def loan_collateral(self):
        """Gets the loan_collateral of this Pool.  # noqa: E501

        the amount of collateral collects for loans  # noqa: E501

        :return: The loan_collateral of this Pool.  # noqa: E501
        :rtype: str
        """
        return self._loan_collateral

    @loan_collateral.setter
    def loan_collateral(self, loan_collateral):
        """Sets the loan_collateral of this Pool.

        the amount of collateral collects for loans  # noqa: E501

        :param loan_collateral: The loan_collateral of this Pool.  # noqa: E501
        :type: str
        """
        if loan_collateral is None:
            raise ValueError("Invalid value for `loan_collateral`, must not be `None`")  # noqa: E501

        self._loan_collateral = loan_collateral

    @property
    def loan_cr(self):
        """Gets the loan_cr of this Pool.  # noqa: E501

        the current loan collateralization ratio  # noqa: E501

        :return: The loan_cr of this Pool.  # noqa: E501
        :rtype: str
        """
        return self._loan_cr

    @loan_cr.setter
    def loan_cr(self, loan_cr):
        """Sets the loan_cr of this Pool.

        the current loan collateralization ratio  # noqa: E501

        :param loan_cr: The loan_cr of this Pool.  # noqa: E501
        :type: str
        """
        if loan_cr is None:
            raise ValueError("Invalid value for `loan_cr`, must not be `None`")  # noqa: E501

        self._loan_cr = loan_cr

    @property
    def derived_depth_bps(self):
        """Gets the derived_depth_bps of this Pool.  # noqa: E501

        the depth of the derived virtual pool relative to L1 pool (in basis points)  # noqa: E501

        :return: The derived_depth_bps of this Pool.  # noqa: E501
        :rtype: str
        """
        return self._derived_depth_bps

    @derived_depth_bps.setter
    def derived_depth_bps(self, derived_depth_bps):
        """Sets the derived_depth_bps of this Pool.

        the depth of the derived virtual pool relative to L1 pool (in basis points)  # noqa: E501

        :param derived_depth_bps: The derived_depth_bps of this Pool.  # noqa: E501
        :type: str
        """
        if derived_depth_bps is None:
            raise ValueError("Invalid value for `derived_depth_bps`, must not be `None`")  # noqa: E501

        self._derived_depth_bps = derived_depth_bps

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
        if issubclass(Pool, dict):
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
        if not isinstance(other, Pool):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other

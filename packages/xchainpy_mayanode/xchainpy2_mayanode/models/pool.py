# coding: utf-8

"""
    Mayanode API

    Mayanode REST API.  # noqa: E501

    OpenAPI spec version: 1.111.0
    Contact: devs@mayachain.org
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
        'balance_cacao': 'str',
        'balance_asset': 'str',
        'asset': 'str',
        'lp_units': 'str',
        'pool_units': 'str',
        'status': 'str',
        'decimals': 'int',
        'synth_units': 'str',
        'synth_supply': 'str',
        'pending_inbound_cacao': 'str',
        'pending_inbound_asset': 'str',
        'savers_depth': 'object',
        'savers_units': 'str',
        'synth_mint_paused': 'bool'
    }

    attribute_map = {
        'balance_cacao': 'balance_cacao',
        'balance_asset': 'balance_asset',
        'asset': 'asset',
        'lp_units': 'LP_units',
        'pool_units': 'pool_units',
        'status': 'status',
        'decimals': 'decimals',
        'synth_units': 'synth_units',
        'synth_supply': 'synth_supply',
        'pending_inbound_cacao': 'pending_inbound_cacao',
        'pending_inbound_asset': 'pending_inbound_asset',
        'savers_depth': 'savers_depth',
        'savers_units': 'savers_units',
        'synth_mint_paused': 'synth_mint_paused'
    }

    def __init__(self, balance_cacao=None, balance_asset=None, asset=None, lp_units=None, pool_units=None, status=None, decimals=None, synth_units=None, synth_supply=None, pending_inbound_cacao=None, pending_inbound_asset=None, savers_depth=None, savers_units=None, synth_mint_paused=None):  # noqa: E501
        """Pool - a model defined in Swagger"""  # noqa: E501
        self._balance_cacao = None
        self._balance_asset = None
        self._asset = None
        self._lp_units = None
        self._pool_units = None
        self._status = None
        self._decimals = None
        self._synth_units = None
        self._synth_supply = None
        self._pending_inbound_cacao = None
        self._pending_inbound_asset = None
        self._savers_depth = None
        self._savers_units = None
        self._synth_mint_paused = None
        self.discriminator = None
        self.balance_cacao = balance_cacao
        self.balance_asset = balance_asset
        self.asset = asset
        self.lp_units = lp_units
        self.pool_units = pool_units
        self.status = status
        if decimals is not None:
            self.decimals = decimals
        self.synth_units = synth_units
        self.synth_supply = synth_supply
        self.pending_inbound_cacao = pending_inbound_cacao
        self.pending_inbound_asset = pending_inbound_asset
        self.savers_depth = savers_depth
        self.savers_units = savers_units
        self.synth_mint_paused = synth_mint_paused

    @property
    def balance_cacao(self):
        """Gets the balance_cacao of this Pool.  # noqa: E501


        :return: The balance_cacao of this Pool.  # noqa: E501
        :rtype: str
        """
        return self._balance_cacao

    @balance_cacao.setter
    def balance_cacao(self, balance_cacao):
        """Sets the balance_cacao of this Pool.


        :param balance_cacao: The balance_cacao of this Pool.  # noqa: E501
        :type: str
        """
        if balance_cacao is None:
            raise ValueError("Invalid value for `balance_cacao`, must not be `None`")  # noqa: E501

        self._balance_cacao = balance_cacao

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
    def pending_inbound_cacao(self):
        """Gets the pending_inbound_cacao of this Pool.  # noqa: E501


        :return: The pending_inbound_cacao of this Pool.  # noqa: E501
        :rtype: str
        """
        return self._pending_inbound_cacao

    @pending_inbound_cacao.setter
    def pending_inbound_cacao(self, pending_inbound_cacao):
        """Sets the pending_inbound_cacao of this Pool.


        :param pending_inbound_cacao: The pending_inbound_cacao of this Pool.  # noqa: E501
        :type: str
        """
        if pending_inbound_cacao is None:
            raise ValueError("Invalid value for `pending_inbound_cacao`, must not be `None`")  # noqa: E501

        self._pending_inbound_cacao = pending_inbound_cacao

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
    def savers_depth(self):
        """Gets the savers_depth of this Pool.  # noqa: E501

        the balance of L1 asset deposited into the Savers Vault  # noqa: E501

        :return: The savers_depth of this Pool.  # noqa: E501
        :rtype: object
        """
        return self._savers_depth

    @savers_depth.setter
    def savers_depth(self, savers_depth):
        """Sets the savers_depth of this Pool.

        the balance of L1 asset deposited into the Savers Vault  # noqa: E501

        :param savers_depth: The savers_depth of this Pool.  # noqa: E501
        :type: object
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

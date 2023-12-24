# coding: utf-8

"""
    Midgard Public API

    The Midgard Public API queries THORChain and any chains linked via the Bifröst and prepares information about the network to be readily available for public users. The API parses transaction event data from THORChain and stores them in a time-series database to make time-dependent queries easy. Midgard does not hold critical information. To interact with THORChain protocol, users should query THORNode directly.  # noqa: E501

    OpenAPI spec version: 2.18.2
    Contact: devs@thorchain.org
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

import pprint
import re  # noqa: F401

import six

class PoolDetail(object):
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
        'annual_percentage_rate': 'str',
        'asset': 'str',
        'asset_depth': 'str',
        'asset_price': 'str',
        'asset_price_usd': 'str',
        'liquidity_units': 'str',
        'native_decimal': 'str',
        'pool_apy': 'str',
        'rune_depth': 'str',
        'savers_apr': 'str',
        'savers_depth': 'str',
        'savers_units': 'str',
        'status': 'str',
        'synth_supply': 'str',
        'synth_units': 'str',
        'total_collateral': 'str',
        'total_debt_tor': 'str',
        'units': 'str',
        'volume24h': 'str'
    }

    attribute_map = {
        'annual_percentage_rate': 'annualPercentageRate',
        'asset': 'asset',
        'asset_depth': 'assetDepth',
        'asset_price': 'assetPrice',
        'asset_price_usd': 'assetPriceUSD',
        'liquidity_units': 'liquidityUnits',
        'native_decimal': 'nativeDecimal',
        'pool_apy': 'poolAPY',
        'rune_depth': 'runeDepth',
        'savers_apr': 'saversAPR',
        'savers_depth': 'saversDepth',
        'savers_units': 'saversUnits',
        'status': 'status',
        'synth_supply': 'synthSupply',
        'synth_units': 'synthUnits',
        'total_collateral': 'totalCollateral',
        'total_debt_tor': 'totalDebtTor',
        'units': 'units',
        'volume24h': 'volume24h'
    }

    def __init__(self, annual_percentage_rate=None, asset=None, asset_depth=None, asset_price=None, asset_price_usd=None, liquidity_units=None, native_decimal=None, pool_apy=None, rune_depth=None, savers_apr=None, savers_depth=None, savers_units=None, status=None, synth_supply=None, synth_units=None, total_collateral=None, total_debt_tor=None, units=None, volume24h=None):  # noqa: E501
        """PoolDetail - a model defined in Swagger"""  # noqa: E501
        self._annual_percentage_rate = None
        self._asset = None
        self._asset_depth = None
        self._asset_price = None
        self._asset_price_usd = None
        self._liquidity_units = None
        self._native_decimal = None
        self._pool_apy = None
        self._rune_depth = None
        self._savers_apr = None
        self._savers_depth = None
        self._savers_units = None
        self._status = None
        self._synth_supply = None
        self._synth_units = None
        self._total_collateral = None
        self._total_debt_tor = None
        self._units = None
        self._volume24h = None
        self.discriminator = None
        self.annual_percentage_rate = annual_percentage_rate
        self.asset = asset
        self.asset_depth = asset_depth
        self.asset_price = asset_price
        self.asset_price_usd = asset_price_usd
        self.liquidity_units = liquidity_units
        self.native_decimal = native_decimal
        self.pool_apy = pool_apy
        self.rune_depth = rune_depth
        self.savers_apr = savers_apr
        self.savers_depth = savers_depth
        self.savers_units = savers_units
        self.status = status
        self.synth_supply = synth_supply
        self.synth_units = synth_units
        self.total_collateral = total_collateral
        self.total_debt_tor = total_debt_tor
        self.units = units
        self.volume24h = volume24h

    @property
    def annual_percentage_rate(self):
        """Gets the annual_percentage_rate of this PoolDetail.  # noqa: E501

        Float, Also called APR. Annual return estimated linearly (not compounded) from a period of typically the last 30 or 100 days (configurable by the period parameter, default is 30). E.g. 0.1 means 10% yearly return. Due to Impermanent Loss and Synths this might be negative, but given Impermanent Loss Protection for 100+ day members, frontends might show MAX(APR, 0).   # noqa: E501

        :return: The annual_percentage_rate of this PoolDetail.  # noqa: E501
        :rtype: str
        """
        return self._annual_percentage_rate

    @annual_percentage_rate.setter
    def annual_percentage_rate(self, annual_percentage_rate):
        """Sets the annual_percentage_rate of this PoolDetail.

        Float, Also called APR. Annual return estimated linearly (not compounded) from a period of typically the last 30 or 100 days (configurable by the period parameter, default is 30). E.g. 0.1 means 10% yearly return. Due to Impermanent Loss and Synths this might be negative, but given Impermanent Loss Protection for 100+ day members, frontends might show MAX(APR, 0).   # noqa: E501

        :param annual_percentage_rate: The annual_percentage_rate of this PoolDetail.  # noqa: E501
        :type: str
        """
        if annual_percentage_rate is None:
            raise ValueError("Invalid value for `annual_percentage_rate`, must not be `None`")  # noqa: E501

        self._annual_percentage_rate = annual_percentage_rate

    @property
    def asset(self):
        """Gets the asset of this PoolDetail.  # noqa: E501


        :return: The asset of this PoolDetail.  # noqa: E501
        :rtype: str
        """
        return self._asset

    @asset.setter
    def asset(self, asset):
        """Sets the asset of this PoolDetail.


        :param asset: The asset of this PoolDetail.  # noqa: E501
        :type: str
        """
        if asset is None:
            raise ValueError("Invalid value for `asset`, must not be `None`")  # noqa: E501

        self._asset = asset

    @property
    def asset_depth(self):
        """Gets the asset_depth of this PoolDetail.  # noqa: E501

        Int64(e8), the amount of Asset in the pool.  # noqa: E501

        :return: The asset_depth of this PoolDetail.  # noqa: E501
        :rtype: str
        """
        return self._asset_depth

    @asset_depth.setter
    def asset_depth(self, asset_depth):
        """Sets the asset_depth of this PoolDetail.

        Int64(e8), the amount of Asset in the pool.  # noqa: E501

        :param asset_depth: The asset_depth of this PoolDetail.  # noqa: E501
        :type: str
        """
        if asset_depth is None:
            raise ValueError("Invalid value for `asset_depth`, must not be `None`")  # noqa: E501

        self._asset_depth = asset_depth

    @property
    def asset_price(self):
        """Gets the asset_price of this PoolDetail.  # noqa: E501

        Float, price of asset in rune. I.e. rune amount / asset amount.  # noqa: E501

        :return: The asset_price of this PoolDetail.  # noqa: E501
        :rtype: str
        """
        return self._asset_price

    @asset_price.setter
    def asset_price(self, asset_price):
        """Sets the asset_price of this PoolDetail.

        Float, price of asset in rune. I.e. rune amount / asset amount.  # noqa: E501

        :param asset_price: The asset_price of this PoolDetail.  # noqa: E501
        :type: str
        """
        if asset_price is None:
            raise ValueError("Invalid value for `asset_price`, must not be `None`")  # noqa: E501

        self._asset_price = asset_price

    @property
    def asset_price_usd(self):
        """Gets the asset_price_usd of this PoolDetail.  # noqa: E501

        Float, the price of asset in USD (based on the deepest USD pool).  # noqa: E501

        :return: The asset_price_usd of this PoolDetail.  # noqa: E501
        :rtype: str
        """
        return self._asset_price_usd

    @asset_price_usd.setter
    def asset_price_usd(self, asset_price_usd):
        """Sets the asset_price_usd of this PoolDetail.

        Float, the price of asset in USD (based on the deepest USD pool).  # noqa: E501

        :param asset_price_usd: The asset_price_usd of this PoolDetail.  # noqa: E501
        :type: str
        """
        if asset_price_usd is None:
            raise ValueError("Invalid value for `asset_price_usd`, must not be `None`")  # noqa: E501

        self._asset_price_usd = asset_price_usd

    @property
    def liquidity_units(self):
        """Gets the liquidity_units of this PoolDetail.  # noqa: E501

        Int64, Liquidity Units in the pool.  # noqa: E501

        :return: The liquidity_units of this PoolDetail.  # noqa: E501
        :rtype: str
        """
        return self._liquidity_units

    @liquidity_units.setter
    def liquidity_units(self, liquidity_units):
        """Sets the liquidity_units of this PoolDetail.

        Int64, Liquidity Units in the pool.  # noqa: E501

        :param liquidity_units: The liquidity_units of this PoolDetail.  # noqa: E501
        :type: str
        """
        if liquidity_units is None:
            raise ValueError("Invalid value for `liquidity_units`, must not be `None`")  # noqa: E501

        self._liquidity_units = liquidity_units

    @property
    def native_decimal(self):
        """Gets the native_decimal of this PoolDetail.  # noqa: E501

        Int64, The native decimal number of the pool asset. (If the value is \"-1\", it means midgard doesn't know the pool native decimal)  # noqa: E501

        :return: The native_decimal of this PoolDetail.  # noqa: E501
        :rtype: str
        """
        return self._native_decimal

    @native_decimal.setter
    def native_decimal(self, native_decimal):
        """Sets the native_decimal of this PoolDetail.

        Int64, The native decimal number of the pool asset. (If the value is \"-1\", it means midgard doesn't know the pool native decimal)  # noqa: E501

        :param native_decimal: The native_decimal of this PoolDetail.  # noqa: E501
        :type: str
        """
        if native_decimal is None:
            raise ValueError("Invalid value for `native_decimal`, must not be `None`")  # noqa: E501

        self._native_decimal = native_decimal

    @property
    def pool_apy(self):
        """Gets the pool_apy of this PoolDetail.  # noqa: E501

        Float, MAX(AnnualPercentageRate, 0)   # noqa: E501

        :return: The pool_apy of this PoolDetail.  # noqa: E501
        :rtype: str
        """
        return self._pool_apy

    @pool_apy.setter
    def pool_apy(self, pool_apy):
        """Sets the pool_apy of this PoolDetail.

        Float, MAX(AnnualPercentageRate, 0)   # noqa: E501

        :param pool_apy: The pool_apy of this PoolDetail.  # noqa: E501
        :type: str
        """
        if pool_apy is None:
            raise ValueError("Invalid value for `pool_apy`, must not be `None`")  # noqa: E501

        self._pool_apy = pool_apy

    @property
    def rune_depth(self):
        """Gets the rune_depth of this PoolDetail.  # noqa: E501

        Int64(e8), the amount of Rune in the pool.  # noqa: E501

        :return: The rune_depth of this PoolDetail.  # noqa: E501
        :rtype: str
        """
        return self._rune_depth

    @rune_depth.setter
    def rune_depth(self, rune_depth):
        """Sets the rune_depth of this PoolDetail.

        Int64(e8), the amount of Rune in the pool.  # noqa: E501

        :param rune_depth: The rune_depth of this PoolDetail.  # noqa: E501
        :type: str
        """
        if rune_depth is None:
            raise ValueError("Invalid value for `rune_depth`, must not be `None`")  # noqa: E501

        self._rune_depth = rune_depth

    @property
    def savers_apr(self):
        """Gets the savers_apr of this PoolDetail.  # noqa: E501

        Float, Annual Return estimated linearly (not compounded) for savers from a period of typically the last 30 or 100 days (configurable by the period parameter, default is 30). E.g. 0.1 means 10% yearly return. If the savers period has not yet been reached, It will show zero instead.   # noqa: E501

        :return: The savers_apr of this PoolDetail.  # noqa: E501
        :rtype: str
        """
        return self._savers_apr

    @savers_apr.setter
    def savers_apr(self, savers_apr):
        """Sets the savers_apr of this PoolDetail.

        Float, Annual Return estimated linearly (not compounded) for savers from a period of typically the last 30 or 100 days (configurable by the period parameter, default is 30). E.g. 0.1 means 10% yearly return. If the savers period has not yet been reached, It will show zero instead.   # noqa: E501

        :param savers_apr: The savers_apr of this PoolDetail.  # noqa: E501
        :type: str
        """
        if savers_apr is None:
            raise ValueError("Invalid value for `savers_apr`, must not be `None`")  # noqa: E501

        self._savers_apr = savers_apr

    @property
    def savers_depth(self):
        """Gets the savers_depth of this PoolDetail.  # noqa: E501

        Int64, Total synth locked in saver vault.  # noqa: E501

        :return: The savers_depth of this PoolDetail.  # noqa: E501
        :rtype: str
        """
        return self._savers_depth

    @savers_depth.setter
    def savers_depth(self, savers_depth):
        """Sets the savers_depth of this PoolDetail.

        Int64, Total synth locked in saver vault.  # noqa: E501

        :param savers_depth: The savers_depth of this PoolDetail.  # noqa: E501
        :type: str
        """
        if savers_depth is None:
            raise ValueError("Invalid value for `savers_depth`, must not be `None`")  # noqa: E501

        self._savers_depth = savers_depth

    @property
    def savers_units(self):
        """Gets the savers_units of this PoolDetail.  # noqa: E501

        Int64, Units tracking savers vault ownership.  # noqa: E501

        :return: The savers_units of this PoolDetail.  # noqa: E501
        :rtype: str
        """
        return self._savers_units

    @savers_units.setter
    def savers_units(self, savers_units):
        """Sets the savers_units of this PoolDetail.

        Int64, Units tracking savers vault ownership.  # noqa: E501

        :param savers_units: The savers_units of this PoolDetail.  # noqa: E501
        :type: str
        """
        if savers_units is None:
            raise ValueError("Invalid value for `savers_units`, must not be `None`")  # noqa: E501

        self._savers_units = savers_units

    @property
    def status(self):
        """Gets the status of this PoolDetail.  # noqa: E501

        The state of the pool, e.g. Available, Staged.  # noqa: E501

        :return: The status of this PoolDetail.  # noqa: E501
        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, status):
        """Sets the status of this PoolDetail.

        The state of the pool, e.g. Available, Staged.  # noqa: E501

        :param status: The status of this PoolDetail.  # noqa: E501
        :type: str
        """
        if status is None:
            raise ValueError("Invalid value for `status`, must not be `None`")  # noqa: E501

        self._status = status

    @property
    def synth_supply(self):
        """Gets the synth_supply of this PoolDetail.  # noqa: E501

        Int64, Synth supply in the pool.  # noqa: E501

        :return: The synth_supply of this PoolDetail.  # noqa: E501
        :rtype: str
        """
        return self._synth_supply

    @synth_supply.setter
    def synth_supply(self, synth_supply):
        """Sets the synth_supply of this PoolDetail.

        Int64, Synth supply in the pool.  # noqa: E501

        :param synth_supply: The synth_supply of this PoolDetail.  # noqa: E501
        :type: str
        """
        if synth_supply is None:
            raise ValueError("Invalid value for `synth_supply`, must not be `None`")  # noqa: E501

        self._synth_supply = synth_supply

    @property
    def synth_units(self):
        """Gets the synth_units of this PoolDetail.  # noqa: E501

        Int64, Synth Units in the pool.  # noqa: E501

        :return: The synth_units of this PoolDetail.  # noqa: E501
        :rtype: str
        """
        return self._synth_units

    @synth_units.setter
    def synth_units(self, synth_units):
        """Sets the synth_units of this PoolDetail.

        Int64, Synth Units in the pool.  # noqa: E501

        :param synth_units: The synth_units of this PoolDetail.  # noqa: E501
        :type: str
        """
        if synth_units is None:
            raise ValueError("Invalid value for `synth_units`, must not be `None`")  # noqa: E501

        self._synth_units = synth_units

    @property
    def total_collateral(self):
        """Gets the total_collateral of this PoolDetail.  # noqa: E501

        Int64, Total collateral of the pool created by the borrowers.  # noqa: E501

        :return: The total_collateral of this PoolDetail.  # noqa: E501
        :rtype: str
        """
        return self._total_collateral

    @total_collateral.setter
    def total_collateral(self, total_collateral):
        """Sets the total_collateral of this PoolDetail.

        Int64, Total collateral of the pool created by the borrowers.  # noqa: E501

        :param total_collateral: The total_collateral of this PoolDetail.  # noqa: E501
        :type: str
        """
        if total_collateral is None:
            raise ValueError("Invalid value for `total_collateral`, must not be `None`")  # noqa: E501

        self._total_collateral = total_collateral

    @property
    def total_debt_tor(self):
        """Gets the total_debt_tor of this PoolDetail.  # noqa: E501

        Int64, Total debt of the pool by the borrowers.  # noqa: E501

        :return: The total_debt_tor of this PoolDetail.  # noqa: E501
        :rtype: str
        """
        return self._total_debt_tor

    @total_debt_tor.setter
    def total_debt_tor(self, total_debt_tor):
        """Sets the total_debt_tor of this PoolDetail.

        Int64, Total debt of the pool by the borrowers.  # noqa: E501

        :param total_debt_tor: The total_debt_tor of this PoolDetail.  # noqa: E501
        :type: str
        """
        if total_debt_tor is None:
            raise ValueError("Invalid value for `total_debt_tor`, must not be `None`")  # noqa: E501

        self._total_debt_tor = total_debt_tor

    @property
    def units(self):
        """Gets the units of this PoolDetail.  # noqa: E501

        Int64, Total Units (synthUnits + liquidityUnits) in the pool.  # noqa: E501

        :return: The units of this PoolDetail.  # noqa: E501
        :rtype: str
        """
        return self._units

    @units.setter
    def units(self, units):
        """Sets the units of this PoolDetail.

        Int64, Total Units (synthUnits + liquidityUnits) in the pool.  # noqa: E501

        :param units: The units of this PoolDetail.  # noqa: E501
        :type: str
        """
        if units is None:
            raise ValueError("Invalid value for `units`, must not be `None`")  # noqa: E501

        self._units = units

    @property
    def volume24h(self):
        """Gets the volume24h of this PoolDetail.  # noqa: E501

        Int64(e8), the total volume of swaps in the last 24h to and from Rune denoted in Rune. It includes synth mint or burn.   # noqa: E501

        :return: The volume24h of this PoolDetail.  # noqa: E501
        :rtype: str
        """
        return self._volume24h

    @volume24h.setter
    def volume24h(self, volume24h):
        """Sets the volume24h of this PoolDetail.

        Int64(e8), the total volume of swaps in the last 24h to and from Rune denoted in Rune. It includes synth mint or burn.   # noqa: E501

        :param volume24h: The volume24h of this PoolDetail.  # noqa: E501
        :type: str
        """
        if volume24h is None:
            raise ValueError("Invalid value for `volume24h`, must not be `None`")  # noqa: E501

        self._volume24h = volume24h

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
        if issubclass(PoolDetail, dict):
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
        if not isinstance(other, PoolDetail):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other

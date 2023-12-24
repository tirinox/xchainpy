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

class StatsData(object):
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
        'add_liquidity_count': 'str',
        'add_liquidity_volume': 'str',
        'daily_active_users': 'str',
        'impermanent_loss_protection_paid': 'str',
        'monthly_active_users': 'str',
        'rune_depth': 'str',
        'rune_price_usd': 'str',
        'swap_count': 'str',
        'swap_count24h': 'str',
        'swap_count30d': 'str',
        'swap_volume': 'str',
        'switched_rune': 'str',
        'synth_burn_count': 'str',
        'synth_mint_count': 'str',
        'to_asset_count': 'str',
        'to_rune_count': 'str',
        'unique_swapper_count': 'str',
        'withdraw_count': 'str',
        'withdraw_volume': 'str'
    }

    attribute_map = {
        'add_liquidity_count': 'addLiquidityCount',
        'add_liquidity_volume': 'addLiquidityVolume',
        'daily_active_users': 'dailyActiveUsers',
        'impermanent_loss_protection_paid': 'impermanentLossProtectionPaid',
        'monthly_active_users': 'monthlyActiveUsers',
        'rune_depth': 'runeDepth',
        'rune_price_usd': 'runePriceUSD',
        'swap_count': 'swapCount',
        'swap_count24h': 'swapCount24h',
        'swap_count30d': 'swapCount30d',
        'swap_volume': 'swapVolume',
        'switched_rune': 'switchedRune',
        'synth_burn_count': 'synthBurnCount',
        'synth_mint_count': 'synthMintCount',
        'to_asset_count': 'toAssetCount',
        'to_rune_count': 'toRuneCount',
        'unique_swapper_count': 'uniqueSwapperCount',
        'withdraw_count': 'withdrawCount',
        'withdraw_volume': 'withdrawVolume'
    }

    def __init__(self, add_liquidity_count=None, add_liquidity_volume=None, daily_active_users=None, impermanent_loss_protection_paid=None, monthly_active_users=None, rune_depth=None, rune_price_usd=None, swap_count=None, swap_count24h=None, swap_count30d=None, swap_volume=None, switched_rune=None, synth_burn_count=None, synth_mint_count=None, to_asset_count=None, to_rune_count=None, unique_swapper_count=None, withdraw_count=None, withdraw_volume=None):  # noqa: E501
        """StatsData - a model defined in Swagger"""  # noqa: E501
        self._add_liquidity_count = None
        self._add_liquidity_volume = None
        self._daily_active_users = None
        self._impermanent_loss_protection_paid = None
        self._monthly_active_users = None
        self._rune_depth = None
        self._rune_price_usd = None
        self._swap_count = None
        self._swap_count24h = None
        self._swap_count30d = None
        self._swap_volume = None
        self._switched_rune = None
        self._synth_burn_count = None
        self._synth_mint_count = None
        self._to_asset_count = None
        self._to_rune_count = None
        self._unique_swapper_count = None
        self._withdraw_count = None
        self._withdraw_volume = None
        self.discriminator = None
        self.add_liquidity_count = add_liquidity_count
        self.add_liquidity_volume = add_liquidity_volume
        self.daily_active_users = daily_active_users
        self.impermanent_loss_protection_paid = impermanent_loss_protection_paid
        self.monthly_active_users = monthly_active_users
        self.rune_depth = rune_depth
        self.rune_price_usd = rune_price_usd
        self.swap_count = swap_count
        self.swap_count24h = swap_count24h
        self.swap_count30d = swap_count30d
        self.swap_volume = swap_volume
        self.switched_rune = switched_rune
        self.synth_burn_count = synth_burn_count
        self.synth_mint_count = synth_mint_count
        self.to_asset_count = to_asset_count
        self.to_rune_count = to_rune_count
        self.unique_swapper_count = unique_swapper_count
        self.withdraw_count = withdraw_count
        self.withdraw_volume = withdraw_volume

    @property
    def add_liquidity_count(self):
        """Gets the add_liquidity_count of this StatsData.  # noqa: E501

        Int64, number of deposits since beginning.  # noqa: E501

        :return: The add_liquidity_count of this StatsData.  # noqa: E501
        :rtype: str
        """
        return self._add_liquidity_count

    @add_liquidity_count.setter
    def add_liquidity_count(self, add_liquidity_count):
        """Sets the add_liquidity_count of this StatsData.

        Int64, number of deposits since beginning.  # noqa: E501

        :param add_liquidity_count: The add_liquidity_count of this StatsData.  # noqa: E501
        :type: str
        """
        if add_liquidity_count is None:
            raise ValueError("Invalid value for `add_liquidity_count`, must not be `None`")  # noqa: E501

        self._add_liquidity_count = add_liquidity_count

    @property
    def add_liquidity_volume(self):
        """Gets the add_liquidity_volume of this StatsData.  # noqa: E501

        Int64(e8), total of deposits since beginning.   # noqa: E501

        :return: The add_liquidity_volume of this StatsData.  # noqa: E501
        :rtype: str
        """
        return self._add_liquidity_volume

    @add_liquidity_volume.setter
    def add_liquidity_volume(self, add_liquidity_volume):
        """Sets the add_liquidity_volume of this StatsData.

        Int64(e8), total of deposits since beginning.   # noqa: E501

        :param add_liquidity_volume: The add_liquidity_volume of this StatsData.  # noqa: E501
        :type: str
        """
        if add_liquidity_volume is None:
            raise ValueError("Invalid value for `add_liquidity_volume`, must not be `None`")  # noqa: E501

        self._add_liquidity_volume = add_liquidity_volume

    @property
    def daily_active_users(self):
        """Gets the daily_active_users of this StatsData.  # noqa: E501

        Deprecated, it's always 0.  # noqa: E501

        :return: The daily_active_users of this StatsData.  # noqa: E501
        :rtype: str
        """
        return self._daily_active_users

    @daily_active_users.setter
    def daily_active_users(self, daily_active_users):
        """Sets the daily_active_users of this StatsData.

        Deprecated, it's always 0.  # noqa: E501

        :param daily_active_users: The daily_active_users of this StatsData.  # noqa: E501
        :type: str
        """
        if daily_active_users is None:
            raise ValueError("Invalid value for `daily_active_users`, must not be `None`")  # noqa: E501

        self._daily_active_users = daily_active_users

    @property
    def impermanent_loss_protection_paid(self):
        """Gets the impermanent_loss_protection_paid of this StatsData.  # noqa: E501

        Int64(e8), impermanent loss protection paid out.   # noqa: E501

        :return: The impermanent_loss_protection_paid of this StatsData.  # noqa: E501
        :rtype: str
        """
        return self._impermanent_loss_protection_paid

    @impermanent_loss_protection_paid.setter
    def impermanent_loss_protection_paid(self, impermanent_loss_protection_paid):
        """Sets the impermanent_loss_protection_paid of this StatsData.

        Int64(e8), impermanent loss protection paid out.   # noqa: E501

        :param impermanent_loss_protection_paid: The impermanent_loss_protection_paid of this StatsData.  # noqa: E501
        :type: str
        """
        if impermanent_loss_protection_paid is None:
            raise ValueError("Invalid value for `impermanent_loss_protection_paid`, must not be `None`")  # noqa: E501

        self._impermanent_loss_protection_paid = impermanent_loss_protection_paid

    @property
    def monthly_active_users(self):
        """Gets the monthly_active_users of this StatsData.  # noqa: E501

        Deprecated, it's always 0.  # noqa: E501

        :return: The monthly_active_users of this StatsData.  # noqa: E501
        :rtype: str
        """
        return self._monthly_active_users

    @monthly_active_users.setter
    def monthly_active_users(self, monthly_active_users):
        """Sets the monthly_active_users of this StatsData.

        Deprecated, it's always 0.  # noqa: E501

        :param monthly_active_users: The monthly_active_users of this StatsData.  # noqa: E501
        :type: str
        """
        if monthly_active_users is None:
            raise ValueError("Invalid value for `monthly_active_users`, must not be `None`")  # noqa: E501

        self._monthly_active_users = monthly_active_users

    @property
    def rune_depth(self):
        """Gets the rune_depth of this StatsData.  # noqa: E501

        Int64(e8), current total Rune in the pools.  # noqa: E501

        :return: The rune_depth of this StatsData.  # noqa: E501
        :rtype: str
        """
        return self._rune_depth

    @rune_depth.setter
    def rune_depth(self, rune_depth):
        """Sets the rune_depth of this StatsData.

        Int64(e8), current total Rune in the pools.  # noqa: E501

        :param rune_depth: The rune_depth of this StatsData.  # noqa: E501
        :type: str
        """
        if rune_depth is None:
            raise ValueError("Invalid value for `rune_depth`, must not be `None`")  # noqa: E501

        self._rune_depth = rune_depth

    @property
    def rune_price_usd(self):
        """Gets the rune_price_usd of this StatsData.  # noqa: E501

        Float, the price of Rune based on the deepest USD pool.  # noqa: E501

        :return: The rune_price_usd of this StatsData.  # noqa: E501
        :rtype: str
        """
        return self._rune_price_usd

    @rune_price_usd.setter
    def rune_price_usd(self, rune_price_usd):
        """Sets the rune_price_usd of this StatsData.

        Float, the price of Rune based on the deepest USD pool.  # noqa: E501

        :param rune_price_usd: The rune_price_usd of this StatsData.  # noqa: E501
        :type: str
        """
        if rune_price_usd is None:
            raise ValueError("Invalid value for `rune_price_usd`, must not be `None`")  # noqa: E501

        self._rune_price_usd = rune_price_usd

    @property
    def swap_count(self):
        """Gets the swap_count of this StatsData.  # noqa: E501

        Int64, number of swaps (including synths) since beginning.  # noqa: E501

        :return: The swap_count of this StatsData.  # noqa: E501
        :rtype: str
        """
        return self._swap_count

    @swap_count.setter
    def swap_count(self, swap_count):
        """Sets the swap_count of this StatsData.

        Int64, number of swaps (including synths) since beginning.  # noqa: E501

        :param swap_count: The swap_count of this StatsData.  # noqa: E501
        :type: str
        """
        if swap_count is None:
            raise ValueError("Invalid value for `swap_count`, must not be `None`")  # noqa: E501

        self._swap_count = swap_count

    @property
    def swap_count24h(self):
        """Gets the swap_count24h of this StatsData.  # noqa: E501

        Int64(e8), number of swaps (including synths) in the last 24h.  # noqa: E501

        :return: The swap_count24h of this StatsData.  # noqa: E501
        :rtype: str
        """
        return self._swap_count24h

    @swap_count24h.setter
    def swap_count24h(self, swap_count24h):
        """Sets the swap_count24h of this StatsData.

        Int64(e8), number of swaps (including synths) in the last 24h.  # noqa: E501

        :param swap_count24h: The swap_count24h of this StatsData.  # noqa: E501
        :type: str
        """
        if swap_count24h is None:
            raise ValueError("Invalid value for `swap_count24h`, must not be `None`")  # noqa: E501

        self._swap_count24h = swap_count24h

    @property
    def swap_count30d(self):
        """Gets the swap_count30d of this StatsData.  # noqa: E501

        Int64, number of swaps (including synths) in the last 30d.  # noqa: E501

        :return: The swap_count30d of this StatsData.  # noqa: E501
        :rtype: str
        """
        return self._swap_count30d

    @swap_count30d.setter
    def swap_count30d(self, swap_count30d):
        """Sets the swap_count30d of this StatsData.

        Int64, number of swaps (including synths) in the last 30d.  # noqa: E501

        :param swap_count30d: The swap_count30d of this StatsData.  # noqa: E501
        :type: str
        """
        if swap_count30d is None:
            raise ValueError("Invalid value for `swap_count30d`, must not be `None`")  # noqa: E501

        self._swap_count30d = swap_count30d

    @property
    def swap_volume(self):
        """Gets the swap_volume of this StatsData.  # noqa: E501

        Int64(e8), total volume of swaps (including synths) denoted in Rune since beginning.   # noqa: E501

        :return: The swap_volume of this StatsData.  # noqa: E501
        :rtype: str
        """
        return self._swap_volume

    @swap_volume.setter
    def swap_volume(self, swap_volume):
        """Sets the swap_volume of this StatsData.

        Int64(e8), total volume of swaps (including synths) denoted in Rune since beginning.   # noqa: E501

        :param swap_volume: The swap_volume of this StatsData.  # noqa: E501
        :type: str
        """
        if swap_volume is None:
            raise ValueError("Invalid value for `swap_volume`, must not be `None`")  # noqa: E501

        self._swap_volume = swap_volume

    @property
    def switched_rune(self):
        """Gets the switched_rune of this StatsData.  # noqa: E501

        Int64(e8), amount of native rune switched from erc20 or bep2 rune.  # noqa: E501

        :return: The switched_rune of this StatsData.  # noqa: E501
        :rtype: str
        """
        return self._switched_rune

    @switched_rune.setter
    def switched_rune(self, switched_rune):
        """Sets the switched_rune of this StatsData.

        Int64(e8), amount of native rune switched from erc20 or bep2 rune.  # noqa: E501

        :param switched_rune: The switched_rune of this StatsData.  # noqa: E501
        :type: str
        """
        if switched_rune is None:
            raise ValueError("Invalid value for `switched_rune`, must not be `None`")  # noqa: E501

        self._switched_rune = switched_rune

    @property
    def synth_burn_count(self):
        """Gets the synth_burn_count of this StatsData.  # noqa: E501

        Int64, number of swaps from Synth to Rune since beginning.  # noqa: E501

        :return: The synth_burn_count of this StatsData.  # noqa: E501
        :rtype: str
        """
        return self._synth_burn_count

    @synth_burn_count.setter
    def synth_burn_count(self, synth_burn_count):
        """Sets the synth_burn_count of this StatsData.

        Int64, number of swaps from Synth to Rune since beginning.  # noqa: E501

        :param synth_burn_count: The synth_burn_count of this StatsData.  # noqa: E501
        :type: str
        """
        if synth_burn_count is None:
            raise ValueError("Invalid value for `synth_burn_count`, must not be `None`")  # noqa: E501

        self._synth_burn_count = synth_burn_count

    @property
    def synth_mint_count(self):
        """Gets the synth_mint_count of this StatsData.  # noqa: E501

        Int64, number of swaps from Rune to Synth since beginning.  # noqa: E501

        :return: The synth_mint_count of this StatsData.  # noqa: E501
        :rtype: str
        """
        return self._synth_mint_count

    @synth_mint_count.setter
    def synth_mint_count(self, synth_mint_count):
        """Sets the synth_mint_count of this StatsData.

        Int64, number of swaps from Rune to Synth since beginning.  # noqa: E501

        :param synth_mint_count: The synth_mint_count of this StatsData.  # noqa: E501
        :type: str
        """
        if synth_mint_count is None:
            raise ValueError("Invalid value for `synth_mint_count`, must not be `None`")  # noqa: E501

        self._synth_mint_count = synth_mint_count

    @property
    def to_asset_count(self):
        """Gets the to_asset_count of this StatsData.  # noqa: E501

        Int64, number of swaps from Rune to Asset since beginning.  # noqa: E501

        :return: The to_asset_count of this StatsData.  # noqa: E501
        :rtype: str
        """
        return self._to_asset_count

    @to_asset_count.setter
    def to_asset_count(self, to_asset_count):
        """Sets the to_asset_count of this StatsData.

        Int64, number of swaps from Rune to Asset since beginning.  # noqa: E501

        :param to_asset_count: The to_asset_count of this StatsData.  # noqa: E501
        :type: str
        """
        if to_asset_count is None:
            raise ValueError("Invalid value for `to_asset_count`, must not be `None`")  # noqa: E501

        self._to_asset_count = to_asset_count

    @property
    def to_rune_count(self):
        """Gets the to_rune_count of this StatsData.  # noqa: E501

        Int64, number of swaps from Asset to Rune since beginning.  # noqa: E501

        :return: The to_rune_count of this StatsData.  # noqa: E501
        :rtype: str
        """
        return self._to_rune_count

    @to_rune_count.setter
    def to_rune_count(self, to_rune_count):
        """Sets the to_rune_count of this StatsData.

        Int64, number of swaps from Asset to Rune since beginning.  # noqa: E501

        :param to_rune_count: The to_rune_count of this StatsData.  # noqa: E501
        :type: str
        """
        if to_rune_count is None:
            raise ValueError("Invalid value for `to_rune_count`, must not be `None`")  # noqa: E501

        self._to_rune_count = to_rune_count

    @property
    def unique_swapper_count(self):
        """Gets the unique_swapper_count of this StatsData.  # noqa: E501

        Deprecated, it's always 0.  # noqa: E501

        :return: The unique_swapper_count of this StatsData.  # noqa: E501
        :rtype: str
        """
        return self._unique_swapper_count

    @unique_swapper_count.setter
    def unique_swapper_count(self, unique_swapper_count):
        """Sets the unique_swapper_count of this StatsData.

        Deprecated, it's always 0.  # noqa: E501

        :param unique_swapper_count: The unique_swapper_count of this StatsData.  # noqa: E501
        :type: str
        """
        if unique_swapper_count is None:
            raise ValueError("Invalid value for `unique_swapper_count`, must not be `None`")  # noqa: E501

        self._unique_swapper_count = unique_swapper_count

    @property
    def withdraw_count(self):
        """Gets the withdraw_count of this StatsData.  # noqa: E501

        Int64, number of withdraws since beginning.  # noqa: E501

        :return: The withdraw_count of this StatsData.  # noqa: E501
        :rtype: str
        """
        return self._withdraw_count

    @withdraw_count.setter
    def withdraw_count(self, withdraw_count):
        """Sets the withdraw_count of this StatsData.

        Int64, number of withdraws since beginning.  # noqa: E501

        :param withdraw_count: The withdraw_count of this StatsData.  # noqa: E501
        :type: str
        """
        if withdraw_count is None:
            raise ValueError("Invalid value for `withdraw_count`, must not be `None`")  # noqa: E501

        self._withdraw_count = withdraw_count

    @property
    def withdraw_volume(self):
        """Gets the withdraw_volume of this StatsData.  # noqa: E501

        Int64(e8), total of withdraws since beginning.   # noqa: E501

        :return: The withdraw_volume of this StatsData.  # noqa: E501
        :rtype: str
        """
        return self._withdraw_volume

    @withdraw_volume.setter
    def withdraw_volume(self, withdraw_volume):
        """Sets the withdraw_volume of this StatsData.

        Int64(e8), total of withdraws since beginning.   # noqa: E501

        :param withdraw_volume: The withdraw_volume of this StatsData.  # noqa: E501
        :type: str
        """
        if withdraw_volume is None:
            raise ValueError("Invalid value for `withdraw_volume`, must not be `None`")  # noqa: E501

        self._withdraw_volume = withdraw_volume

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
        if issubclass(StatsData, dict):
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
        if not isinstance(other, StatsData):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other

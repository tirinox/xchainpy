# coding: utf-8

"""
    Midgard Public API

    The Midgard Public API queries THORChain and any chains linked via the Bifröst and prepares information about the network to be readily available for public users. The API parses transaction event data from THORChain and stores them in a time-series database to make time-dependent queries easy. Midgard does not hold critical information. To interact with THORChain protocol, users should query THORNode directly.  # noqa: E501

    OpenAPI spec version: 2.23.2
    Contact: devs@thorchain.org
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

import pprint
import re  # noqa: F401

import six

class LiquidityHistoryItem(object):
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
        'add_asset_liquidity_volume': 'str',
        'add_liquidity_count': 'str',
        'add_liquidity_volume': 'str',
        'add_rune_liquidity_volume': 'str',
        'end_time': 'str',
        'net': 'str',
        'rune_price_usd': 'str',
        'start_time': 'str',
        'withdraw_asset_volume': 'str',
        'withdraw_count': 'str',
        'withdraw_rune_volume': 'str',
        'withdraw_volume': 'str'
    }

    attribute_map = {
        'add_asset_liquidity_volume': 'addAssetLiquidityVolume',
        'add_liquidity_count': 'addLiquidityCount',
        'add_liquidity_volume': 'addLiquidityVolume',
        'add_rune_liquidity_volume': 'addRuneLiquidityVolume',
        'end_time': 'endTime',
        'net': 'net',
        'rune_price_usd': 'runePriceUSD',
        'start_time': 'startTime',
        'withdraw_asset_volume': 'withdrawAssetVolume',
        'withdraw_count': 'withdrawCount',
        'withdraw_rune_volume': 'withdrawRuneVolume',
        'withdraw_volume': 'withdrawVolume'
    }

    def __init__(self, add_asset_liquidity_volume=None, add_liquidity_count=None, add_liquidity_volume=None, add_rune_liquidity_volume=None, end_time=None, net=None, rune_price_usd=None, start_time=None, withdraw_asset_volume=None, withdraw_count=None, withdraw_rune_volume=None, withdraw_volume=None):  # noqa: E501
        """LiquidityHistoryItem - a model defined in Swagger"""  # noqa: E501
        self._add_asset_liquidity_volume = None
        self._add_liquidity_count = None
        self._add_liquidity_volume = None
        self._add_rune_liquidity_volume = None
        self._end_time = None
        self._net = None
        self._rune_price_usd = None
        self._start_time = None
        self._withdraw_asset_volume = None
        self._withdraw_count = None
        self._withdraw_rune_volume = None
        self._withdraw_volume = None
        self.discriminator = None
        self.add_asset_liquidity_volume = add_asset_liquidity_volume
        self.add_liquidity_count = add_liquidity_count
        self.add_liquidity_volume = add_liquidity_volume
        self.add_rune_liquidity_volume = add_rune_liquidity_volume
        self.end_time = end_time
        self.net = net
        self.rune_price_usd = rune_price_usd
        self.start_time = start_time
        self.withdraw_asset_volume = withdraw_asset_volume
        self.withdraw_count = withdraw_count
        self.withdraw_rune_volume = withdraw_rune_volume
        self.withdraw_volume = withdraw_volume

    @property
    def add_asset_liquidity_volume(self):
        """Gets the add_asset_liquidity_volume of this LiquidityHistoryItem.  # noqa: E501

        Int64(e8), total assets deposited during the time interval. Denoted in Rune using the price at deposit time.   # noqa: E501

        :return: The add_asset_liquidity_volume of this LiquidityHistoryItem.  # noqa: E501
        :rtype: str
        """
        return self._add_asset_liquidity_volume

    @add_asset_liquidity_volume.setter
    def add_asset_liquidity_volume(self, add_asset_liquidity_volume):
        """Sets the add_asset_liquidity_volume of this LiquidityHistoryItem.

        Int64(e8), total assets deposited during the time interval. Denoted in Rune using the price at deposit time.   # noqa: E501

        :param add_asset_liquidity_volume: The add_asset_liquidity_volume of this LiquidityHistoryItem.  # noqa: E501
        :type: str
        """
        if add_asset_liquidity_volume is None:
            raise ValueError("Invalid value for `add_asset_liquidity_volume`, must not be `None`")  # noqa: E501

        self._add_asset_liquidity_volume = add_asset_liquidity_volume

    @property
    def add_liquidity_count(self):
        """Gets the add_liquidity_count of this LiquidityHistoryItem.  # noqa: E501

        Int64, number of deposits during the time interval.   # noqa: E501

        :return: The add_liquidity_count of this LiquidityHistoryItem.  # noqa: E501
        :rtype: str
        """
        return self._add_liquidity_count

    @add_liquidity_count.setter
    def add_liquidity_count(self, add_liquidity_count):
        """Sets the add_liquidity_count of this LiquidityHistoryItem.

        Int64, number of deposits during the time interval.   # noqa: E501

        :param add_liquidity_count: The add_liquidity_count of this LiquidityHistoryItem.  # noqa: E501
        :type: str
        """
        if add_liquidity_count is None:
            raise ValueError("Invalid value for `add_liquidity_count`, must not be `None`")  # noqa: E501

        self._add_liquidity_count = add_liquidity_count

    @property
    def add_liquidity_volume(self):
        """Gets the add_liquidity_volume of this LiquidityHistoryItem.  # noqa: E501

        Int64(e8), total of rune and asset deposits. Denoted in Rune (using the price at deposit time).   # noqa: E501

        :return: The add_liquidity_volume of this LiquidityHistoryItem.  # noqa: E501
        :rtype: str
        """
        return self._add_liquidity_volume

    @add_liquidity_volume.setter
    def add_liquidity_volume(self, add_liquidity_volume):
        """Sets the add_liquidity_volume of this LiquidityHistoryItem.

        Int64(e8), total of rune and asset deposits. Denoted in Rune (using the price at deposit time).   # noqa: E501

        :param add_liquidity_volume: The add_liquidity_volume of this LiquidityHistoryItem.  # noqa: E501
        :type: str
        """
        if add_liquidity_volume is None:
            raise ValueError("Invalid value for `add_liquidity_volume`, must not be `None`")  # noqa: E501

        self._add_liquidity_volume = add_liquidity_volume

    @property
    def add_rune_liquidity_volume(self):
        """Gets the add_rune_liquidity_volume of this LiquidityHistoryItem.  # noqa: E501

        Int64(e8), total Rune deposited during the time interval.   # noqa: E501

        :return: The add_rune_liquidity_volume of this LiquidityHistoryItem.  # noqa: E501
        :rtype: str
        """
        return self._add_rune_liquidity_volume

    @add_rune_liquidity_volume.setter
    def add_rune_liquidity_volume(self, add_rune_liquidity_volume):
        """Sets the add_rune_liquidity_volume of this LiquidityHistoryItem.

        Int64(e8), total Rune deposited during the time interval.   # noqa: E501

        :param add_rune_liquidity_volume: The add_rune_liquidity_volume of this LiquidityHistoryItem.  # noqa: E501
        :type: str
        """
        if add_rune_liquidity_volume is None:
            raise ValueError("Invalid value for `add_rune_liquidity_volume`, must not be `None`")  # noqa: E501

        self._add_rune_liquidity_volume = add_rune_liquidity_volume

    @property
    def end_time(self):
        """Gets the end_time of this LiquidityHistoryItem.  # noqa: E501

        Int64, The end time of bucket in unix timestamp  # noqa: E501

        :return: The end_time of this LiquidityHistoryItem.  # noqa: E501
        :rtype: str
        """
        return self._end_time

    @end_time.setter
    def end_time(self, end_time):
        """Sets the end_time of this LiquidityHistoryItem.

        Int64, The end time of bucket in unix timestamp  # noqa: E501

        :param end_time: The end_time of this LiquidityHistoryItem.  # noqa: E501
        :type: str
        """
        if end_time is None:
            raise ValueError("Invalid value for `end_time`, must not be `None`")  # noqa: E501

        self._end_time = end_time

    @property
    def net(self):
        """Gets the net of this LiquidityHistoryItem.  # noqa: E501

        Int64(e8), net liquidity changes (withdrawals - deposits) during the time interval   # noqa: E501

        :return: The net of this LiquidityHistoryItem.  # noqa: E501
        :rtype: str
        """
        return self._net

    @net.setter
    def net(self, net):
        """Sets the net of this LiquidityHistoryItem.

        Int64(e8), net liquidity changes (withdrawals - deposits) during the time interval   # noqa: E501

        :param net: The net of this LiquidityHistoryItem.  # noqa: E501
        :type: str
        """
        if net is None:
            raise ValueError("Invalid value for `net`, must not be `None`")  # noqa: E501

        self._net = net

    @property
    def rune_price_usd(self):
        """Gets the rune_price_usd of this LiquidityHistoryItem.  # noqa: E501

        Float, the price of Rune based on the deepest USD pool at the end of the interval.   # noqa: E501

        :return: The rune_price_usd of this LiquidityHistoryItem.  # noqa: E501
        :rtype: str
        """
        return self._rune_price_usd

    @rune_price_usd.setter
    def rune_price_usd(self, rune_price_usd):
        """Sets the rune_price_usd of this LiquidityHistoryItem.

        Float, the price of Rune based on the deepest USD pool at the end of the interval.   # noqa: E501

        :param rune_price_usd: The rune_price_usd of this LiquidityHistoryItem.  # noqa: E501
        :type: str
        """
        if rune_price_usd is None:
            raise ValueError("Invalid value for `rune_price_usd`, must not be `None`")  # noqa: E501

        self._rune_price_usd = rune_price_usd

    @property
    def start_time(self):
        """Gets the start_time of this LiquidityHistoryItem.  # noqa: E501

        Int64, The beginning time of bucket in unix timestamp  # noqa: E501

        :return: The start_time of this LiquidityHistoryItem.  # noqa: E501
        :rtype: str
        """
        return self._start_time

    @start_time.setter
    def start_time(self, start_time):
        """Sets the start_time of this LiquidityHistoryItem.

        Int64, The beginning time of bucket in unix timestamp  # noqa: E501

        :param start_time: The start_time of this LiquidityHistoryItem.  # noqa: E501
        :type: str
        """
        if start_time is None:
            raise ValueError("Invalid value for `start_time`, must not be `None`")  # noqa: E501

        self._start_time = start_time

    @property
    def withdraw_asset_volume(self):
        """Gets the withdraw_asset_volume of this LiquidityHistoryItem.  # noqa: E501

        Int64(e8), total assets withdrawn during the time interval. Denoted in Rune using the price at withdraw time.   # noqa: E501

        :return: The withdraw_asset_volume of this LiquidityHistoryItem.  # noqa: E501
        :rtype: str
        """
        return self._withdraw_asset_volume

    @withdraw_asset_volume.setter
    def withdraw_asset_volume(self, withdraw_asset_volume):
        """Sets the withdraw_asset_volume of this LiquidityHistoryItem.

        Int64(e8), total assets withdrawn during the time interval. Denoted in Rune using the price at withdraw time.   # noqa: E501

        :param withdraw_asset_volume: The withdraw_asset_volume of this LiquidityHistoryItem.  # noqa: E501
        :type: str
        """
        if withdraw_asset_volume is None:
            raise ValueError("Invalid value for `withdraw_asset_volume`, must not be `None`")  # noqa: E501

        self._withdraw_asset_volume = withdraw_asset_volume

    @property
    def withdraw_count(self):
        """Gets the withdraw_count of this LiquidityHistoryItem.  # noqa: E501

        Int64, number of withdraw during the time interval.   # noqa: E501

        :return: The withdraw_count of this LiquidityHistoryItem.  # noqa: E501
        :rtype: str
        """
        return self._withdraw_count

    @withdraw_count.setter
    def withdraw_count(self, withdraw_count):
        """Sets the withdraw_count of this LiquidityHistoryItem.

        Int64, number of withdraw during the time interval.   # noqa: E501

        :param withdraw_count: The withdraw_count of this LiquidityHistoryItem.  # noqa: E501
        :type: str
        """
        if withdraw_count is None:
            raise ValueError("Invalid value for `withdraw_count`, must not be `None`")  # noqa: E501

        self._withdraw_count = withdraw_count

    @property
    def withdraw_rune_volume(self):
        """Gets the withdraw_rune_volume of this LiquidityHistoryItem.  # noqa: E501

        Int64(e8), total Rune withdrawn during the time interval.   # noqa: E501

        :return: The withdraw_rune_volume of this LiquidityHistoryItem.  # noqa: E501
        :rtype: str
        """
        return self._withdraw_rune_volume

    @withdraw_rune_volume.setter
    def withdraw_rune_volume(self, withdraw_rune_volume):
        """Sets the withdraw_rune_volume of this LiquidityHistoryItem.

        Int64(e8), total Rune withdrawn during the time interval.   # noqa: E501

        :param withdraw_rune_volume: The withdraw_rune_volume of this LiquidityHistoryItem.  # noqa: E501
        :type: str
        """
        if withdraw_rune_volume is None:
            raise ValueError("Invalid value for `withdraw_rune_volume`, must not be `None`")  # noqa: E501

        self._withdraw_rune_volume = withdraw_rune_volume

    @property
    def withdraw_volume(self):
        """Gets the withdraw_volume of this LiquidityHistoryItem.  # noqa: E501

        Int64(e8), total of rune and asset withdrawals. Denoted in Rune (using the price at withdraw time).   # noqa: E501

        :return: The withdraw_volume of this LiquidityHistoryItem.  # noqa: E501
        :rtype: str
        """
        return self._withdraw_volume

    @withdraw_volume.setter
    def withdraw_volume(self, withdraw_volume):
        """Sets the withdraw_volume of this LiquidityHistoryItem.

        Int64(e8), total of rune and asset withdrawals. Denoted in Rune (using the price at withdraw time).   # noqa: E501

        :param withdraw_volume: The withdraw_volume of this LiquidityHistoryItem.  # noqa: E501
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
        if issubclass(LiquidityHistoryItem, dict):
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
        if not isinstance(other, LiquidityHistoryItem):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other

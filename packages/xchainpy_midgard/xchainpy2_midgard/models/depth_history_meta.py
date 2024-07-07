# coding: utf-8

"""
    Midgard Public API

    The Midgard Public API queries THORChain and any chains linked via the Bifröst and prepares information about the network to be readily available for public users. The API parses transaction event data from THORChain and stores them in a time-series database to make time-dependent queries easy. Midgard does not hold critical information. To interact with THORChain protocol, users should query THORNode directly.  # noqa: E501

    OpenAPI spec version: 2.22.4
    Contact: devs@thorchain.org
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

import pprint
import re  # noqa: F401

import six

class DepthHistoryMeta(object):
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
        'end_asset_depth': 'str',
        'end_lp_units': 'str',
        'end_member_count': 'str',
        'end_rune_depth': 'str',
        'end_synth_units': 'str',
        'end_time': 'str',
        'luvi_increase': 'str',
        'price_shift_loss': 'str',
        'start_asset_depth': 'str',
        'start_lp_units': 'str',
        'start_member_count': 'str',
        'start_rune_depth': 'str',
        'start_synth_units': 'str',
        'start_time': 'str'
    }

    attribute_map = {
        'end_asset_depth': 'endAssetDepth',
        'end_lp_units': 'endLPUnits',
        'end_member_count': 'endMemberCount',
        'end_rune_depth': 'endRuneDepth',
        'end_synth_units': 'endSynthUnits',
        'end_time': 'endTime',
        'luvi_increase': 'luviIncrease',
        'price_shift_loss': 'priceShiftLoss',
        'start_asset_depth': 'startAssetDepth',
        'start_lp_units': 'startLPUnits',
        'start_member_count': 'startMemberCount',
        'start_rune_depth': 'startRuneDepth',
        'start_synth_units': 'startSynthUnits',
        'start_time': 'startTime'
    }

    def __init__(self, end_asset_depth=None, end_lp_units=None, end_member_count=None, end_rune_depth=None, end_synth_units=None, end_time=None, luvi_increase=None, price_shift_loss=None, start_asset_depth=None, start_lp_units=None, start_member_count=None, start_rune_depth=None, start_synth_units=None, start_time=None):  # noqa: E501
        """DepthHistoryMeta - a model defined in Swagger"""  # noqa: E501
        self._end_asset_depth = None
        self._end_lp_units = None
        self._end_member_count = None
        self._end_rune_depth = None
        self._end_synth_units = None
        self._end_time = None
        self._luvi_increase = None
        self._price_shift_loss = None
        self._start_asset_depth = None
        self._start_lp_units = None
        self._start_member_count = None
        self._start_rune_depth = None
        self._start_synth_units = None
        self._start_time = None
        self.discriminator = None
        self.end_asset_depth = end_asset_depth
        self.end_lp_units = end_lp_units
        self.end_member_count = end_member_count
        self.end_rune_depth = end_rune_depth
        self.end_synth_units = end_synth_units
        self.end_time = end_time
        self.luvi_increase = luvi_increase
        self.price_shift_loss = price_shift_loss
        self.start_asset_depth = start_asset_depth
        self.start_lp_units = start_lp_units
        self.start_member_count = start_member_count
        self.start_rune_depth = start_rune_depth
        self.start_synth_units = start_synth_units
        self.start_time = start_time

    @property
    def end_asset_depth(self):
        """Gets the end_asset_depth of this DepthHistoryMeta.  # noqa: E501

        Int64(e8), the amount of Asset in the pool at the end of the interval at time endTime   # noqa: E501

        :return: The end_asset_depth of this DepthHistoryMeta.  # noqa: E501
        :rtype: str
        """
        return self._end_asset_depth

    @end_asset_depth.setter
    def end_asset_depth(self, end_asset_depth):
        """Sets the end_asset_depth of this DepthHistoryMeta.

        Int64(e8), the amount of Asset in the pool at the end of the interval at time endTime   # noqa: E501

        :param end_asset_depth: The end_asset_depth of this DepthHistoryMeta.  # noqa: E501
        :type: str
        """
        if end_asset_depth is None:
            raise ValueError("Invalid value for `end_asset_depth`, must not be `None`")  # noqa: E501

        self._end_asset_depth = end_asset_depth

    @property
    def end_lp_units(self):
        """Gets the end_lp_units of this DepthHistoryMeta.  # noqa: E501

        Int64, Liquidity Units in the pool at the end of the interval at time endTime  # noqa: E501

        :return: The end_lp_units of this DepthHistoryMeta.  # noqa: E501
        :rtype: str
        """
        return self._end_lp_units

    @end_lp_units.setter
    def end_lp_units(self, end_lp_units):
        """Sets the end_lp_units of this DepthHistoryMeta.

        Int64, Liquidity Units in the pool at the end of the interval at time endTime  # noqa: E501

        :param end_lp_units: The end_lp_units of this DepthHistoryMeta.  # noqa: E501
        :type: str
        """
        if end_lp_units is None:
            raise ValueError("Invalid value for `end_lp_units`, must not be `None`")  # noqa: E501

        self._end_lp_units = end_lp_units

    @property
    def end_member_count(self):
        """Gets the end_member_count of this DepthHistoryMeta.  # noqa: E501

        Int64, Number of liquidity members in the pool at the end of the interval at time endTime  # noqa: E501

        :return: The end_member_count of this DepthHistoryMeta.  # noqa: E501
        :rtype: str
        """
        return self._end_member_count

    @end_member_count.setter
    def end_member_count(self, end_member_count):
        """Sets the end_member_count of this DepthHistoryMeta.

        Int64, Number of liquidity members in the pool at the end of the interval at time endTime  # noqa: E501

        :param end_member_count: The end_member_count of this DepthHistoryMeta.  # noqa: E501
        :type: str
        """
        if end_member_count is None:
            raise ValueError("Invalid value for `end_member_count`, must not be `None`")  # noqa: E501

        self._end_member_count = end_member_count

    @property
    def end_rune_depth(self):
        """Gets the end_rune_depth of this DepthHistoryMeta.  # noqa: E501

        Int64(e8), the amount of Rune in the pool at the end of the interval at time endTime   # noqa: E501

        :return: The end_rune_depth of this DepthHistoryMeta.  # noqa: E501
        :rtype: str
        """
        return self._end_rune_depth

    @end_rune_depth.setter
    def end_rune_depth(self, end_rune_depth):
        """Sets the end_rune_depth of this DepthHistoryMeta.

        Int64(e8), the amount of Rune in the pool at the end of the interval at time endTime   # noqa: E501

        :param end_rune_depth: The end_rune_depth of this DepthHistoryMeta.  # noqa: E501
        :type: str
        """
        if end_rune_depth is None:
            raise ValueError("Invalid value for `end_rune_depth`, must not be `None`")  # noqa: E501

        self._end_rune_depth = end_rune_depth

    @property
    def end_synth_units(self):
        """Gets the end_synth_units of this DepthHistoryMeta.  # noqa: E501

        Int64, Synth Units in the pool at the end of the interval at time endTime  # noqa: E501

        :return: The end_synth_units of this DepthHistoryMeta.  # noqa: E501
        :rtype: str
        """
        return self._end_synth_units

    @end_synth_units.setter
    def end_synth_units(self, end_synth_units):
        """Sets the end_synth_units of this DepthHistoryMeta.

        Int64, Synth Units in the pool at the end of the interval at time endTime  # noqa: E501

        :param end_synth_units: The end_synth_units of this DepthHistoryMeta.  # noqa: E501
        :type: str
        """
        if end_synth_units is None:
            raise ValueError("Invalid value for `end_synth_units`, must not be `None`")  # noqa: E501

        self._end_synth_units = end_synth_units

    @property
    def end_time(self):
        """Gets the end_time of this DepthHistoryMeta.  # noqa: E501

        Int64, The end time of bucket in unix timestamp  # noqa: E501

        :return: The end_time of this DepthHistoryMeta.  # noqa: E501
        :rtype: str
        """
        return self._end_time

    @end_time.setter
    def end_time(self, end_time):
        """Sets the end_time of this DepthHistoryMeta.

        Int64, The end time of bucket in unix timestamp  # noqa: E501

        :param end_time: The end_time of this DepthHistoryMeta.  # noqa: E501
        :type: str
        """
        if end_time is None:
            raise ValueError("Invalid value for `end_time`, must not be `None`")  # noqa: E501

        self._end_time = end_time

    @property
    def luvi_increase(self):
        """Gets the luvi_increase of this DepthHistoryMeta.  # noqa: E501

        Float, The liquidity unit value index increase between startTime and endTime   # noqa: E501

        :return: The luvi_increase of this DepthHistoryMeta.  # noqa: E501
        :rtype: str
        """
        return self._luvi_increase

    @luvi_increase.setter
    def luvi_increase(self, luvi_increase):
        """Sets the luvi_increase of this DepthHistoryMeta.

        Float, The liquidity unit value index increase between startTime and endTime   # noqa: E501

        :param luvi_increase: The luvi_increase of this DepthHistoryMeta.  # noqa: E501
        :type: str
        """
        if luvi_increase is None:
            raise ValueError("Invalid value for `luvi_increase`, must not be `None`")  # noqa: E501

        self._luvi_increase = luvi_increase

    @property
    def price_shift_loss(self):
        """Gets the price_shift_loss of this DepthHistoryMeta.  # noqa: E501

        Float, The impermanent loss between the first and last depth item  # noqa: E501

        :return: The price_shift_loss of this DepthHistoryMeta.  # noqa: E501
        :rtype: str
        """
        return self._price_shift_loss

    @price_shift_loss.setter
    def price_shift_loss(self, price_shift_loss):
        """Sets the price_shift_loss of this DepthHistoryMeta.

        Float, The impermanent loss between the first and last depth item  # noqa: E501

        :param price_shift_loss: The price_shift_loss of this DepthHistoryMeta.  # noqa: E501
        :type: str
        """
        if price_shift_loss is None:
            raise ValueError("Invalid value for `price_shift_loss`, must not be `None`")  # noqa: E501

        self._price_shift_loss = price_shift_loss

    @property
    def start_asset_depth(self):
        """Gets the start_asset_depth of this DepthHistoryMeta.  # noqa: E501

        Int64(e8), the amount of Asset in the pool at the start of the interval at time startTime   # noqa: E501

        :return: The start_asset_depth of this DepthHistoryMeta.  # noqa: E501
        :rtype: str
        """
        return self._start_asset_depth

    @start_asset_depth.setter
    def start_asset_depth(self, start_asset_depth):
        """Sets the start_asset_depth of this DepthHistoryMeta.

        Int64(e8), the amount of Asset in the pool at the start of the interval at time startTime   # noqa: E501

        :param start_asset_depth: The start_asset_depth of this DepthHistoryMeta.  # noqa: E501
        :type: str
        """
        if start_asset_depth is None:
            raise ValueError("Invalid value for `start_asset_depth`, must not be `None`")  # noqa: E501

        self._start_asset_depth = start_asset_depth

    @property
    def start_lp_units(self):
        """Gets the start_lp_units of this DepthHistoryMeta.  # noqa: E501

        Int64, Liquidity Units in the pool at the start of the interval at time startTime   # noqa: E501

        :return: The start_lp_units of this DepthHistoryMeta.  # noqa: E501
        :rtype: str
        """
        return self._start_lp_units

    @start_lp_units.setter
    def start_lp_units(self, start_lp_units):
        """Sets the start_lp_units of this DepthHistoryMeta.

        Int64, Liquidity Units in the pool at the start of the interval at time startTime   # noqa: E501

        :param start_lp_units: The start_lp_units of this DepthHistoryMeta.  # noqa: E501
        :type: str
        """
        if start_lp_units is None:
            raise ValueError("Invalid value for `start_lp_units`, must not be `None`")  # noqa: E501

        self._start_lp_units = start_lp_units

    @property
    def start_member_count(self):
        """Gets the start_member_count of this DepthHistoryMeta.  # noqa: E501

        Int64, Number of liquidity member in the pool at the start of the interval at time startTime   # noqa: E501

        :return: The start_member_count of this DepthHistoryMeta.  # noqa: E501
        :rtype: str
        """
        return self._start_member_count

    @start_member_count.setter
    def start_member_count(self, start_member_count):
        """Sets the start_member_count of this DepthHistoryMeta.

        Int64, Number of liquidity member in the pool at the start of the interval at time startTime   # noqa: E501

        :param start_member_count: The start_member_count of this DepthHistoryMeta.  # noqa: E501
        :type: str
        """
        if start_member_count is None:
            raise ValueError("Invalid value for `start_member_count`, must not be `None`")  # noqa: E501

        self._start_member_count = start_member_count

    @property
    def start_rune_depth(self):
        """Gets the start_rune_depth of this DepthHistoryMeta.  # noqa: E501

        Int64(e8), the amount of Rune in the pool at the start of the interval at time startTime   # noqa: E501

        :return: The start_rune_depth of this DepthHistoryMeta.  # noqa: E501
        :rtype: str
        """
        return self._start_rune_depth

    @start_rune_depth.setter
    def start_rune_depth(self, start_rune_depth):
        """Sets the start_rune_depth of this DepthHistoryMeta.

        Int64(e8), the amount of Rune in the pool at the start of the interval at time startTime   # noqa: E501

        :param start_rune_depth: The start_rune_depth of this DepthHistoryMeta.  # noqa: E501
        :type: str
        """
        if start_rune_depth is None:
            raise ValueError("Invalid value for `start_rune_depth`, must not be `None`")  # noqa: E501

        self._start_rune_depth = start_rune_depth

    @property
    def start_synth_units(self):
        """Gets the start_synth_units of this DepthHistoryMeta.  # noqa: E501

        Int64, Synth Units in the pool at the start of the interval at time startTime   # noqa: E501

        :return: The start_synth_units of this DepthHistoryMeta.  # noqa: E501
        :rtype: str
        """
        return self._start_synth_units

    @start_synth_units.setter
    def start_synth_units(self, start_synth_units):
        """Sets the start_synth_units of this DepthHistoryMeta.

        Int64, Synth Units in the pool at the start of the interval at time startTime   # noqa: E501

        :param start_synth_units: The start_synth_units of this DepthHistoryMeta.  # noqa: E501
        :type: str
        """
        if start_synth_units is None:
            raise ValueError("Invalid value for `start_synth_units`, must not be `None`")  # noqa: E501

        self._start_synth_units = start_synth_units

    @property
    def start_time(self):
        """Gets the start_time of this DepthHistoryMeta.  # noqa: E501

        Int64, The beginning time of bucket in unix timestamp  # noqa: E501

        :return: The start_time of this DepthHistoryMeta.  # noqa: E501
        :rtype: str
        """
        return self._start_time

    @start_time.setter
    def start_time(self, start_time):
        """Sets the start_time of this DepthHistoryMeta.

        Int64, The beginning time of bucket in unix timestamp  # noqa: E501

        :param start_time: The start_time of this DepthHistoryMeta.  # noqa: E501
        :type: str
        """
        if start_time is None:
            raise ValueError("Invalid value for `start_time`, must not be `None`")  # noqa: E501

        self._start_time = start_time

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
        if issubclass(DepthHistoryMeta, dict):
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
        if not isinstance(other, DepthHistoryMeta):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other

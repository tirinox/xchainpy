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

class StreamingSwapMeta(object):
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
        'count': 'str',
        'deposited_coin': 'Coin',
        'failed_swap_reasons': 'list[str]',
        'failed_swaps': 'list[str]',
        'in_coin': 'Coin',
        'interval': 'str',
        'last_height': 'str',
        'out_coin': 'Coin',
        'quantity': 'str'
    }

    attribute_map = {
        'count': 'count',
        'deposited_coin': 'depositedCoin',
        'failed_swap_reasons': 'failedSwapReasons',
        'failed_swaps': 'failedSwaps',
        'in_coin': 'inCoin',
        'interval': 'interval',
        'last_height': 'lastHeight',
        'out_coin': 'outCoin',
        'quantity': 'quantity'
    }

    def __init__(self, count=None, deposited_coin=None, failed_swap_reasons=None, failed_swaps=None, in_coin=None, interval=None, last_height=None, out_coin=None, quantity=None):  # noqa: E501
        """StreamingSwapMeta - a model defined in Swagger"""  # noqa: E501
        self._count = None
        self._deposited_coin = None
        self._failed_swap_reasons = None
        self._failed_swaps = None
        self._in_coin = None
        self._interval = None
        self._last_height = None
        self._out_coin = None
        self._quantity = None
        self.discriminator = None
        self.count = count
        self.deposited_coin = deposited_coin
        if failed_swap_reasons is not None:
            self.failed_swap_reasons = failed_swap_reasons
        if failed_swaps is not None:
            self.failed_swaps = failed_swaps
        self.in_coin = in_coin
        self.interval = interval
        self.last_height = last_height
        self.out_coin = out_coin
        self.quantity = quantity

    @property
    def count(self):
        """Gets the count of this StreamingSwapMeta.  # noqa: E501

        Int64, Number of swaps events which already happened.  # noqa: E501

        :return: The count of this StreamingSwapMeta.  # noqa: E501
        :rtype: str
        """
        return self._count

    @count.setter
    def count(self, count):
        """Sets the count of this StreamingSwapMeta.

        Int64, Number of swaps events which already happened.  # noqa: E501

        :param count: The count of this StreamingSwapMeta.  # noqa: E501
        :type: str
        """
        if count is None:
            raise ValueError("Invalid value for `count`, must not be `None`")  # noqa: E501

        self._count = count

    @property
    def deposited_coin(self):
        """Gets the deposited_coin of this StreamingSwapMeta.  # noqa: E501


        :return: The deposited_coin of this StreamingSwapMeta.  # noqa: E501
        :rtype: Coin
        """
        return self._deposited_coin

    @deposited_coin.setter
    def deposited_coin(self, deposited_coin):
        """Sets the deposited_coin of this StreamingSwapMeta.


        :param deposited_coin: The deposited_coin of this StreamingSwapMeta.  # noqa: E501
        :type: Coin
        """
        if deposited_coin is None:
            raise ValueError("Invalid value for `deposited_coin`, must not be `None`")  # noqa: E501

        self._deposited_coin = deposited_coin

    @property
    def failed_swap_reasons(self):
        """Gets the failed_swap_reasons of this StreamingSwapMeta.  # noqa: E501

        Array of failed swaps reasons in streaming swap.  # noqa: E501

        :return: The failed_swap_reasons of this StreamingSwapMeta.  # noqa: E501
        :rtype: list[str]
        """
        return self._failed_swap_reasons

    @failed_swap_reasons.setter
    def failed_swap_reasons(self, failed_swap_reasons):
        """Sets the failed_swap_reasons of this StreamingSwapMeta.

        Array of failed swaps reasons in streaming swap.  # noqa: E501

        :param failed_swap_reasons: The failed_swap_reasons of this StreamingSwapMeta.  # noqa: E501
        :type: list[str]
        """

        self._failed_swap_reasons = failed_swap_reasons

    @property
    def failed_swaps(self):
        """Gets the failed_swaps of this StreamingSwapMeta.  # noqa: E501

        Array of failed swaps index in streaming swap.  # noqa: E501

        :return: The failed_swaps of this StreamingSwapMeta.  # noqa: E501
        :rtype: list[str]
        """
        return self._failed_swaps

    @failed_swaps.setter
    def failed_swaps(self, failed_swaps):
        """Sets the failed_swaps of this StreamingSwapMeta.

        Array of failed swaps index in streaming swap.  # noqa: E501

        :param failed_swaps: The failed_swaps of this StreamingSwapMeta.  # noqa: E501
        :type: list[str]
        """

        self._failed_swaps = failed_swaps

    @property
    def in_coin(self):
        """Gets the in_coin of this StreamingSwapMeta.  # noqa: E501


        :return: The in_coin of this StreamingSwapMeta.  # noqa: E501
        :rtype: Coin
        """
        return self._in_coin

    @in_coin.setter
    def in_coin(self, in_coin):
        """Sets the in_coin of this StreamingSwapMeta.


        :param in_coin: The in_coin of this StreamingSwapMeta.  # noqa: E501
        :type: Coin
        """
        if in_coin is None:
            raise ValueError("Invalid value for `in_coin`, must not be `None`")  # noqa: E501

        self._in_coin = in_coin

    @property
    def interval(self):
        """Gets the interval of this StreamingSwapMeta.  # noqa: E501

        Int64, Number of blocks between swpas. (Blocks/Swap) E.g. 1 means every block.  # noqa: E501

        :return: The interval of this StreamingSwapMeta.  # noqa: E501
        :rtype: str
        """
        return self._interval

    @interval.setter
    def interval(self, interval):
        """Sets the interval of this StreamingSwapMeta.

        Int64, Number of blocks between swpas. (Blocks/Swap) E.g. 1 means every block.  # noqa: E501

        :param interval: The interval of this StreamingSwapMeta.  # noqa: E501
        :type: str
        """
        if interval is None:
            raise ValueError("Invalid value for `interval`, must not be `None`")  # noqa: E501

        self._interval = interval

    @property
    def last_height(self):
        """Gets the last_height of this StreamingSwapMeta.  # noqa: E501

        Int64, The last blockheight the final swap happened (not outbound). This field will be missing until the final swap happens.   # noqa: E501

        :return: The last_height of this StreamingSwapMeta.  # noqa: E501
        :rtype: str
        """
        return self._last_height

    @last_height.setter
    def last_height(self, last_height):
        """Sets the last_height of this StreamingSwapMeta.

        Int64, The last blockheight the final swap happened (not outbound). This field will be missing until the final swap happens.   # noqa: E501

        :param last_height: The last_height of this StreamingSwapMeta.  # noqa: E501
        :type: str
        """
        if last_height is None:
            raise ValueError("Invalid value for `last_height`, must not be `None`")  # noqa: E501

        self._last_height = last_height

    @property
    def out_coin(self):
        """Gets the out_coin of this StreamingSwapMeta.  # noqa: E501


        :return: The out_coin of this StreamingSwapMeta.  # noqa: E501
        :rtype: Coin
        """
        return self._out_coin

    @out_coin.setter
    def out_coin(self, out_coin):
        """Sets the out_coin of this StreamingSwapMeta.


        :param out_coin: The out_coin of this StreamingSwapMeta.  # noqa: E501
        :type: Coin
        """
        if out_coin is None:
            raise ValueError("Invalid value for `out_coin`, must not be `None`")  # noqa: E501

        self._out_coin = out_coin

    @property
    def quantity(self):
        """Gets the quantity of this StreamingSwapMeta.  # noqa: E501

        Int64,  Number of swaps which thorchain is planning to execute. Total count at the end might be less.   # noqa: E501

        :return: The quantity of this StreamingSwapMeta.  # noqa: E501
        :rtype: str
        """
        return self._quantity

    @quantity.setter
    def quantity(self, quantity):
        """Sets the quantity of this StreamingSwapMeta.

        Int64,  Number of swaps which thorchain is planning to execute. Total count at the end might be less.   # noqa: E501

        :param quantity: The quantity of this StreamingSwapMeta.  # noqa: E501
        :type: str
        """
        if quantity is None:
            raise ValueError("Invalid value for `quantity`, must not be `None`")  # noqa: E501

        self._quantity = quantity

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
        if issubclass(StreamingSwapMeta, dict):
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
        if not isinstance(other, StreamingSwapMeta):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other

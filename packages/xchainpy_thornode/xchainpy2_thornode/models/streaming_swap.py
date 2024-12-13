# coding: utf-8

"""
    Thornode API

    Thornode REST API.  # noqa: E501

    OpenAPI spec version: 3.0.0
    Contact: devs@thorchain.org
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

import pprint
import re  # noqa: F401

import six

class StreamingSwap(object):
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
        'tx_id': 'str',
        'interval': 'int',
        'quantity': 'int',
        'count': 'int',
        'last_height': 'int',
        'trade_target': 'str',
        'source_asset': 'str',
        'target_asset': 'str',
        'destination': 'str',
        'deposit': 'str',
        '_in': 'str',
        'out': 'str',
        'failed_swaps': 'list[int]',
        'failed_swap_reasons': 'list[str]'
    }

    attribute_map = {
        'tx_id': 'tx_id',
        'interval': 'interval',
        'quantity': 'quantity',
        'count': 'count',
        'last_height': 'last_height',
        'trade_target': 'trade_target',
        'source_asset': 'source_asset',
        'target_asset': 'target_asset',
        'destination': 'destination',
        'deposit': 'deposit',
        '_in': 'in',
        'out': 'out',
        'failed_swaps': 'failed_swaps',
        'failed_swap_reasons': 'failed_swap_reasons'
    }

    def __init__(self, tx_id=None, interval=None, quantity=None, count=None, last_height=None, trade_target=None, source_asset=None, target_asset=None, destination=None, deposit=None, _in=None, out=None, failed_swaps=None, failed_swap_reasons=None):  # noqa: E501
        """StreamingSwap - a model defined in Swagger"""  # noqa: E501
        self._tx_id = None
        self._interval = None
        self._quantity = None
        self._count = None
        self._last_height = None
        self._trade_target = None
        self._source_asset = None
        self._target_asset = None
        self._destination = None
        self._deposit = None
        self.__in = None
        self._out = None
        self._failed_swaps = None
        self._failed_swap_reasons = None
        self.discriminator = None
        if tx_id is not None:
            self.tx_id = tx_id
        if interval is not None:
            self.interval = interval
        if quantity is not None:
            self.quantity = quantity
        if count is not None:
            self.count = count
        if last_height is not None:
            self.last_height = last_height
        self.trade_target = trade_target
        if source_asset is not None:
            self.source_asset = source_asset
        if target_asset is not None:
            self.target_asset = target_asset
        if destination is not None:
            self.destination = destination
        self.deposit = deposit
        self._in = _in
        self.out = out
        if failed_swaps is not None:
            self.failed_swaps = failed_swaps
        if failed_swap_reasons is not None:
            self.failed_swap_reasons = failed_swap_reasons

    @property
    def tx_id(self):
        """Gets the tx_id of this StreamingSwap.  # noqa: E501

        the hash of a transaction  # noqa: E501

        :return: The tx_id of this StreamingSwap.  # noqa: E501
        :rtype: str
        """
        return self._tx_id

    @tx_id.setter
    def tx_id(self, tx_id):
        """Sets the tx_id of this StreamingSwap.

        the hash of a transaction  # noqa: E501

        :param tx_id: The tx_id of this StreamingSwap.  # noqa: E501
        :type: str
        """

        self._tx_id = tx_id

    @property
    def interval(self):
        """Gets the interval of this StreamingSwap.  # noqa: E501

        how often each swap is made, in blocks  # noqa: E501

        :return: The interval of this StreamingSwap.  # noqa: E501
        :rtype: int
        """
        return self._interval

    @interval.setter
    def interval(self, interval):
        """Sets the interval of this StreamingSwap.

        how often each swap is made, in blocks  # noqa: E501

        :param interval: The interval of this StreamingSwap.  # noqa: E501
        :type: int
        """

        self._interval = interval

    @property
    def quantity(self):
        """Gets the quantity of this StreamingSwap.  # noqa: E501

        the total number of swaps in a streaming swaps  # noqa: E501

        :return: The quantity of this StreamingSwap.  # noqa: E501
        :rtype: int
        """
        return self._quantity

    @quantity.setter
    def quantity(self, quantity):
        """Sets the quantity of this StreamingSwap.

        the total number of swaps in a streaming swaps  # noqa: E501

        :param quantity: The quantity of this StreamingSwap.  # noqa: E501
        :type: int
        """

        self._quantity = quantity

    @property
    def count(self):
        """Gets the count of this StreamingSwap.  # noqa: E501

        the amount of swap attempts so far  # noqa: E501

        :return: The count of this StreamingSwap.  # noqa: E501
        :rtype: int
        """
        return self._count

    @count.setter
    def count(self, count):
        """Sets the count of this StreamingSwap.

        the amount of swap attempts so far  # noqa: E501

        :param count: The count of this StreamingSwap.  # noqa: E501
        :type: int
        """

        self._count = count

    @property
    def last_height(self):
        """Gets the last_height of this StreamingSwap.  # noqa: E501

        the block height of the latest swap  # noqa: E501

        :return: The last_height of this StreamingSwap.  # noqa: E501
        :rtype: int
        """
        return self._last_height

    @last_height.setter
    def last_height(self, last_height):
        """Sets the last_height of this StreamingSwap.

        the block height of the latest swap  # noqa: E501

        :param last_height: The last_height of this StreamingSwap.  # noqa: E501
        :type: int
        """

        self._last_height = last_height

    @property
    def trade_target(self):
        """Gets the trade_target of this StreamingSwap.  # noqa: E501

        the total number of tokens the swapper wants to receive of the output asset  # noqa: E501

        :return: The trade_target of this StreamingSwap.  # noqa: E501
        :rtype: str
        """
        return self._trade_target

    @trade_target.setter
    def trade_target(self, trade_target):
        """Sets the trade_target of this StreamingSwap.

        the total number of tokens the swapper wants to receive of the output asset  # noqa: E501

        :param trade_target: The trade_target of this StreamingSwap.  # noqa: E501
        :type: str
        """
        if trade_target is None:
            raise ValueError("Invalid value for `trade_target`, must not be `None`")  # noqa: E501

        self._trade_target = trade_target

    @property
    def source_asset(self):
        """Gets the source_asset of this StreamingSwap.  # noqa: E501

        the asset to be swapped from  # noqa: E501

        :return: The source_asset of this StreamingSwap.  # noqa: E501
        :rtype: str
        """
        return self._source_asset

    @source_asset.setter
    def source_asset(self, source_asset):
        """Sets the source_asset of this StreamingSwap.

        the asset to be swapped from  # noqa: E501

        :param source_asset: The source_asset of this StreamingSwap.  # noqa: E501
        :type: str
        """

        self._source_asset = source_asset

    @property
    def target_asset(self):
        """Gets the target_asset of this StreamingSwap.  # noqa: E501

        the asset to be swapped to  # noqa: E501

        :return: The target_asset of this StreamingSwap.  # noqa: E501
        :rtype: str
        """
        return self._target_asset

    @target_asset.setter
    def target_asset(self, target_asset):
        """Sets the target_asset of this StreamingSwap.

        the asset to be swapped to  # noqa: E501

        :param target_asset: The target_asset of this StreamingSwap.  # noqa: E501
        :type: str
        """

        self._target_asset = target_asset

    @property
    def destination(self):
        """Gets the destination of this StreamingSwap.  # noqa: E501

        the destination address to receive the swap output  # noqa: E501

        :return: The destination of this StreamingSwap.  # noqa: E501
        :rtype: str
        """
        return self._destination

    @destination.setter
    def destination(self, destination):
        """Sets the destination of this StreamingSwap.

        the destination address to receive the swap output  # noqa: E501

        :param destination: The destination of this StreamingSwap.  # noqa: E501
        :type: str
        """

        self._destination = destination

    @property
    def deposit(self):
        """Gets the deposit of this StreamingSwap.  # noqa: E501

        the number of input tokens the swapper has deposited  # noqa: E501

        :return: The deposit of this StreamingSwap.  # noqa: E501
        :rtype: str
        """
        return self._deposit

    @deposit.setter
    def deposit(self, deposit):
        """Sets the deposit of this StreamingSwap.

        the number of input tokens the swapper has deposited  # noqa: E501

        :param deposit: The deposit of this StreamingSwap.  # noqa: E501
        :type: str
        """
        if deposit is None:
            raise ValueError("Invalid value for `deposit`, must not be `None`")  # noqa: E501

        self._deposit = deposit

    @property
    def _in(self):
        """Gets the _in of this StreamingSwap.  # noqa: E501

        the amount of input tokens that have been swapped so far  # noqa: E501

        :return: The _in of this StreamingSwap.  # noqa: E501
        :rtype: str
        """
        return self.__in

    @_in.setter
    def _in(self, _in):
        """Sets the _in of this StreamingSwap.

        the amount of input tokens that have been swapped so far  # noqa: E501

        :param _in: The _in of this StreamingSwap.  # noqa: E501
        :type: str
        """
        if _in is None:
            raise ValueError("Invalid value for `_in`, must not be `None`")  # noqa: E501

        self.__in = _in

    @property
    def out(self):
        """Gets the out of this StreamingSwap.  # noqa: E501

        the amount of output tokens that have been swapped so far  # noqa: E501

        :return: The out of this StreamingSwap.  # noqa: E501
        :rtype: str
        """
        return self._out

    @out.setter
    def out(self, out):
        """Sets the out of this StreamingSwap.

        the amount of output tokens that have been swapped so far  # noqa: E501

        :param out: The out of this StreamingSwap.  # noqa: E501
        :type: str
        """
        if out is None:
            raise ValueError("Invalid value for `out`, must not be `None`")  # noqa: E501

        self._out = out

    @property
    def failed_swaps(self):
        """Gets the failed_swaps of this StreamingSwap.  # noqa: E501

        the list of swap indexes that failed  # noqa: E501

        :return: The failed_swaps of this StreamingSwap.  # noqa: E501
        :rtype: list[int]
        """
        return self._failed_swaps

    @failed_swaps.setter
    def failed_swaps(self, failed_swaps):
        """Sets the failed_swaps of this StreamingSwap.

        the list of swap indexes that failed  # noqa: E501

        :param failed_swaps: The failed_swaps of this StreamingSwap.  # noqa: E501
        :type: list[int]
        """

        self._failed_swaps = failed_swaps

    @property
    def failed_swap_reasons(self):
        """Gets the failed_swap_reasons of this StreamingSwap.  # noqa: E501

        the list of reasons that sub-swaps have failed  # noqa: E501

        :return: The failed_swap_reasons of this StreamingSwap.  # noqa: E501
        :rtype: list[str]
        """
        return self._failed_swap_reasons

    @failed_swap_reasons.setter
    def failed_swap_reasons(self, failed_swap_reasons):
        """Sets the failed_swap_reasons of this StreamingSwap.

        the list of reasons that sub-swaps have failed  # noqa: E501

        :param failed_swap_reasons: The failed_swap_reasons of this StreamingSwap.  # noqa: E501
        :type: list[str]
        """

        self._failed_swap_reasons = failed_swap_reasons

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
        if issubclass(StreamingSwap, dict):
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
        if not isinstance(other, StreamingSwap):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other

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

class MsgSwap(object):
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
        'tx': 'Tx',
        'target_asset': 'str',
        'destination': 'str',
        'trade_target': 'str',
        'affiliate_address': 'str',
        'affiliate_basis_points': 'str',
        'signer': 'str',
        'aggregator': 'str',
        'aggregator_target_address': 'str',
        'aggregator_target_limit': 'str',
        'order_type': 'int',
        'stream_quantity': 'int',
        'stream_interval': 'int'
    }

    attribute_map = {
        'tx': 'tx',
        'target_asset': 'target_asset',
        'destination': 'destination',
        'trade_target': 'trade_target',
        'affiliate_address': 'affiliate_address',
        'affiliate_basis_points': 'affiliate_basis_points',
        'signer': 'signer',
        'aggregator': 'aggregator',
        'aggregator_target_address': 'aggregator_target_address',
        'aggregator_target_limit': 'aggregator_target_limit',
        'order_type': 'order_type',
        'stream_quantity': 'stream_quantity',
        'stream_interval': 'stream_interval'
    }

    def __init__(self, tx=None, target_asset=None, destination=None, trade_target=None, affiliate_address=None, affiliate_basis_points=None, signer=None, aggregator=None, aggregator_target_address=None, aggregator_target_limit=None, order_type=None, stream_quantity=None, stream_interval=None):  # noqa: E501
        """MsgSwap - a model defined in Swagger"""  # noqa: E501
        self._tx = None
        self._target_asset = None
        self._destination = None
        self._trade_target = None
        self._affiliate_address = None
        self._affiliate_basis_points = None
        self._signer = None
        self._aggregator = None
        self._aggregator_target_address = None
        self._aggregator_target_limit = None
        self._order_type = None
        self._stream_quantity = None
        self._stream_interval = None
        self.discriminator = None
        self.tx = tx
        self.target_asset = target_asset
        if destination is not None:
            self.destination = destination
        self.trade_target = trade_target
        if affiliate_address is not None:
            self.affiliate_address = affiliate_address
        self.affiliate_basis_points = affiliate_basis_points
        if signer is not None:
            self.signer = signer
        if aggregator is not None:
            self.aggregator = aggregator
        if aggregator_target_address is not None:
            self.aggregator_target_address = aggregator_target_address
        if aggregator_target_limit is not None:
            self.aggregator_target_limit = aggregator_target_limit
        if order_type is not None:
            self.order_type = order_type
        if stream_quantity is not None:
            self.stream_quantity = stream_quantity
        if stream_interval is not None:
            self.stream_interval = stream_interval

    @property
    def tx(self):
        """Gets the tx of this MsgSwap.  # noqa: E501


        :return: The tx of this MsgSwap.  # noqa: E501
        :rtype: Tx
        """
        return self._tx

    @tx.setter
    def tx(self, tx):
        """Sets the tx of this MsgSwap.


        :param tx: The tx of this MsgSwap.  # noqa: E501
        :type: Tx
        """
        if tx is None:
            raise ValueError("Invalid value for `tx`, must not be `None`")  # noqa: E501

        self._tx = tx

    @property
    def target_asset(self):
        """Gets the target_asset of this MsgSwap.  # noqa: E501

        the asset to be swapped to  # noqa: E501

        :return: The target_asset of this MsgSwap.  # noqa: E501
        :rtype: str
        """
        return self._target_asset

    @target_asset.setter
    def target_asset(self, target_asset):
        """Sets the target_asset of this MsgSwap.

        the asset to be swapped to  # noqa: E501

        :param target_asset: The target_asset of this MsgSwap.  # noqa: E501
        :type: str
        """
        if target_asset is None:
            raise ValueError("Invalid value for `target_asset`, must not be `None`")  # noqa: E501

        self._target_asset = target_asset

    @property
    def destination(self):
        """Gets the destination of this MsgSwap.  # noqa: E501

        the destination address to receive the swap output  # noqa: E501

        :return: The destination of this MsgSwap.  # noqa: E501
        :rtype: str
        """
        return self._destination

    @destination.setter
    def destination(self, destination):
        """Sets the destination of this MsgSwap.

        the destination address to receive the swap output  # noqa: E501

        :param destination: The destination of this MsgSwap.  # noqa: E501
        :type: str
        """

        self._destination = destination

    @property
    def trade_target(self):
        """Gets the trade_target of this MsgSwap.  # noqa: E501

        the minimum amount of output asset to receive (else cancelling and refunding the swap)  # noqa: E501

        :return: The trade_target of this MsgSwap.  # noqa: E501
        :rtype: str
        """
        return self._trade_target

    @trade_target.setter
    def trade_target(self, trade_target):
        """Sets the trade_target of this MsgSwap.

        the minimum amount of output asset to receive (else cancelling and refunding the swap)  # noqa: E501

        :param trade_target: The trade_target of this MsgSwap.  # noqa: E501
        :type: str
        """
        if trade_target is None:
            raise ValueError("Invalid value for `trade_target`, must not be `None`")  # noqa: E501

        self._trade_target = trade_target

    @property
    def affiliate_address(self):
        """Gets the affiliate_address of this MsgSwap.  # noqa: E501

        the affiliate address which will receive any affiliate fee  # noqa: E501

        :return: The affiliate_address of this MsgSwap.  # noqa: E501
        :rtype: str
        """
        return self._affiliate_address

    @affiliate_address.setter
    def affiliate_address(self, affiliate_address):
        """Sets the affiliate_address of this MsgSwap.

        the affiliate address which will receive any affiliate fee  # noqa: E501

        :param affiliate_address: The affiliate_address of this MsgSwap.  # noqa: E501
        :type: str
        """

        self._affiliate_address = affiliate_address

    @property
    def affiliate_basis_points(self):
        """Gets the affiliate_basis_points of this MsgSwap.  # noqa: E501

        the affiliate fee in basis points  # noqa: E501

        :return: The affiliate_basis_points of this MsgSwap.  # noqa: E501
        :rtype: str
        """
        return self._affiliate_basis_points

    @affiliate_basis_points.setter
    def affiliate_basis_points(self, affiliate_basis_points):
        """Sets the affiliate_basis_points of this MsgSwap.

        the affiliate fee in basis points  # noqa: E501

        :param affiliate_basis_points: The affiliate_basis_points of this MsgSwap.  # noqa: E501
        :type: str
        """
        if affiliate_basis_points is None:
            raise ValueError("Invalid value for `affiliate_basis_points`, must not be `None`")  # noqa: E501

        self._affiliate_basis_points = affiliate_basis_points

    @property
    def signer(self):
        """Gets the signer of this MsgSwap.  # noqa: E501

        the signer (sender) of the transaction  # noqa: E501

        :return: The signer of this MsgSwap.  # noqa: E501
        :rtype: str
        """
        return self._signer

    @signer.setter
    def signer(self, signer):
        """Sets the signer of this MsgSwap.

        the signer (sender) of the transaction  # noqa: E501

        :param signer: The signer of this MsgSwap.  # noqa: E501
        :type: str
        """

        self._signer = signer

    @property
    def aggregator(self):
        """Gets the aggregator of this MsgSwap.  # noqa: E501

        the contract address if an aggregator is specified for a non-THORChain SwapOut  # noqa: E501

        :return: The aggregator of this MsgSwap.  # noqa: E501
        :rtype: str
        """
        return self._aggregator

    @aggregator.setter
    def aggregator(self, aggregator):
        """Sets the aggregator of this MsgSwap.

        the contract address if an aggregator is specified for a non-THORChain SwapOut  # noqa: E501

        :param aggregator: The aggregator of this MsgSwap.  # noqa: E501
        :type: str
        """

        self._aggregator = aggregator

    @property
    def aggregator_target_address(self):
        """Gets the aggregator_target_address of this MsgSwap.  # noqa: E501

        the desired output asset of the aggregator SwapOut  # noqa: E501

        :return: The aggregator_target_address of this MsgSwap.  # noqa: E501
        :rtype: str
        """
        return self._aggregator_target_address

    @aggregator_target_address.setter
    def aggregator_target_address(self, aggregator_target_address):
        """Sets the aggregator_target_address of this MsgSwap.

        the desired output asset of the aggregator SwapOut  # noqa: E501

        :param aggregator_target_address: The aggregator_target_address of this MsgSwap.  # noqa: E501
        :type: str
        """

        self._aggregator_target_address = aggregator_target_address

    @property
    def aggregator_target_limit(self):
        """Gets the aggregator_target_limit of this MsgSwap.  # noqa: E501

        the minimum amount of SwapOut asset to receive (else cancelling the SwapOut and receiving THORChain's output)  # noqa: E501

        :return: The aggregator_target_limit of this MsgSwap.  # noqa: E501
        :rtype: str
        """
        return self._aggregator_target_limit

    @aggregator_target_limit.setter
    def aggregator_target_limit(self, aggregator_target_limit):
        """Sets the aggregator_target_limit of this MsgSwap.

        the minimum amount of SwapOut asset to receive (else cancelling the SwapOut and receiving THORChain's output)  # noqa: E501

        :param aggregator_target_limit: The aggregator_target_limit of this MsgSwap.  # noqa: E501
        :type: str
        """

        self._aggregator_target_limit = aggregator_target_limit

    @property
    def order_type(self):
        """Gets the order_type of this MsgSwap.  # noqa: E501

        0 if a market order (immediately completed or refunded), 1 if a limit order (held until fulfillable)  # noqa: E501

        :return: The order_type of this MsgSwap.  # noqa: E501
        :rtype: int
        """
        return self._order_type

    @order_type.setter
    def order_type(self, order_type):
        """Sets the order_type of this MsgSwap.

        0 if a market order (immediately completed or refunded), 1 if a limit order (held until fulfillable)  # noqa: E501

        :param order_type: The order_type of this MsgSwap.  # noqa: E501
        :type: int
        """

        self._order_type = order_type

    @property
    def stream_quantity(self):
        """Gets the stream_quantity of this MsgSwap.  # noqa: E501

        number of swaps to execute in a streaming swap  # noqa: E501

        :return: The stream_quantity of this MsgSwap.  # noqa: E501
        :rtype: int
        """
        return self._stream_quantity

    @stream_quantity.setter
    def stream_quantity(self, stream_quantity):
        """Sets the stream_quantity of this MsgSwap.

        number of swaps to execute in a streaming swap  # noqa: E501

        :param stream_quantity: The stream_quantity of this MsgSwap.  # noqa: E501
        :type: int
        """

        self._stream_quantity = stream_quantity

    @property
    def stream_interval(self):
        """Gets the stream_interval of this MsgSwap.  # noqa: E501

        the interval (in blocks) to execute the streaming swap  # noqa: E501

        :return: The stream_interval of this MsgSwap.  # noqa: E501
        :rtype: int
        """
        return self._stream_interval

    @stream_interval.setter
    def stream_interval(self, stream_interval):
        """Sets the stream_interval of this MsgSwap.

        the interval (in blocks) to execute the streaming swap  # noqa: E501

        :param stream_interval: The stream_interval of this MsgSwap.  # noqa: E501
        :type: int
        """

        self._stream_interval = stream_interval

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
        if issubclass(MsgSwap, dict):
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
        if not isinstance(other, MsgSwap):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other

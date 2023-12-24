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

class SwapMetadata(object):
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
        'affiliate_address': 'str',
        'affiliate_fee': 'str',
        'is_streaming_swap': 'bool',
        'liquidity_fee': 'str',
        'memo': 'str',
        'network_fees': 'NetworkFees',
        'streaming_swap_meta': 'StreamingSwapMeta',
        'swap_slip': 'str',
        'swap_target': 'str'
    }

    attribute_map = {
        'affiliate_address': 'affiliateAddress',
        'affiliate_fee': 'affiliateFee',
        'is_streaming_swap': 'isStreamingSwap',
        'liquidity_fee': 'liquidityFee',
        'memo': 'memo',
        'network_fees': 'networkFees',
        'streaming_swap_meta': 'streamingSwapMeta',
        'swap_slip': 'swapSlip',
        'swap_target': 'swapTarget'
    }

    def __init__(self, affiliate_address=None, affiliate_fee=None, is_streaming_swap=None, liquidity_fee=None, memo=None, network_fees=None, streaming_swap_meta=None, swap_slip=None, swap_target=None):  # noqa: E501
        """SwapMetadata - a model defined in Swagger"""  # noqa: E501
        self._affiliate_address = None
        self._affiliate_fee = None
        self._is_streaming_swap = None
        self._liquidity_fee = None
        self._memo = None
        self._network_fees = None
        self._streaming_swap_meta = None
        self._swap_slip = None
        self._swap_target = None
        self.discriminator = None
        self.affiliate_address = affiliate_address
        self.affiliate_fee = affiliate_fee
        self.is_streaming_swap = is_streaming_swap
        self.liquidity_fee = liquidity_fee
        self.memo = memo
        self.network_fees = network_fees
        if streaming_swap_meta is not None:
            self.streaming_swap_meta = streaming_swap_meta
        self.swap_slip = swap_slip
        self.swap_target = swap_target

    @property
    def affiliate_address(self):
        """Gets the affiliate_address of this SwapMetadata.  # noqa: E501

        Affiliate fee address of the swap, empty if fee swap  # noqa: E501

        :return: The affiliate_address of this SwapMetadata.  # noqa: E501
        :rtype: str
        """
        return self._affiliate_address

    @affiliate_address.setter
    def affiliate_address(self, affiliate_address):
        """Sets the affiliate_address of this SwapMetadata.

        Affiliate fee address of the swap, empty if fee swap  # noqa: E501

        :param affiliate_address: The affiliate_address of this SwapMetadata.  # noqa: E501
        :type: str
        """
        if affiliate_address is None:
            raise ValueError("Invalid value for `affiliate_address`, must not be `None`")  # noqa: E501

        self._affiliate_address = affiliate_address

    @property
    def affiliate_fee(self):
        """Gets the affiliate_fee of this SwapMetadata.  # noqa: E501

        Int64 (Basis points, 0-1000, where 1000=10%)  # noqa: E501

        :return: The affiliate_fee of this SwapMetadata.  # noqa: E501
        :rtype: str
        """
        return self._affiliate_fee

    @affiliate_fee.setter
    def affiliate_fee(self, affiliate_fee):
        """Sets the affiliate_fee of this SwapMetadata.

        Int64 (Basis points, 0-1000, where 1000=10%)  # noqa: E501

        :param affiliate_fee: The affiliate_fee of this SwapMetadata.  # noqa: E501
        :type: str
        """
        if affiliate_fee is None:
            raise ValueError("Invalid value for `affiliate_fee`, must not be `None`")  # noqa: E501

        self._affiliate_fee = affiliate_fee

    @property
    def is_streaming_swap(self):
        """Gets the is_streaming_swap of this SwapMetadata.  # noqa: E501

        indicate whether this action was streaming  # noqa: E501

        :return: The is_streaming_swap of this SwapMetadata.  # noqa: E501
        :rtype: bool
        """
        return self._is_streaming_swap

    @is_streaming_swap.setter
    def is_streaming_swap(self, is_streaming_swap):
        """Sets the is_streaming_swap of this SwapMetadata.

        indicate whether this action was streaming  # noqa: E501

        :param is_streaming_swap: The is_streaming_swap of this SwapMetadata.  # noqa: E501
        :type: bool
        """
        if is_streaming_swap is None:
            raise ValueError("Invalid value for `is_streaming_swap`, must not be `None`")  # noqa: E501

        self._is_streaming_swap = is_streaming_swap

    @property
    def liquidity_fee(self):
        """Gets the liquidity_fee of this SwapMetadata.  # noqa: E501

        Int64(e8), RUNE amount charged as swap liquidity fee  # noqa: E501

        :return: The liquidity_fee of this SwapMetadata.  # noqa: E501
        :rtype: str
        """
        return self._liquidity_fee

    @liquidity_fee.setter
    def liquidity_fee(self, liquidity_fee):
        """Sets the liquidity_fee of this SwapMetadata.

        Int64(e8), RUNE amount charged as swap liquidity fee  # noqa: E501

        :param liquidity_fee: The liquidity_fee of this SwapMetadata.  # noqa: E501
        :type: str
        """
        if liquidity_fee is None:
            raise ValueError("Invalid value for `liquidity_fee`, must not be `None`")  # noqa: E501

        self._liquidity_fee = liquidity_fee

    @property
    def memo(self):
        """Gets the memo of this SwapMetadata.  # noqa: E501

        Transaction memo of the swap action  # noqa: E501

        :return: The memo of this SwapMetadata.  # noqa: E501
        :rtype: str
        """
        return self._memo

    @memo.setter
    def memo(self, memo):
        """Sets the memo of this SwapMetadata.

        Transaction memo of the swap action  # noqa: E501

        :param memo: The memo of this SwapMetadata.  # noqa: E501
        :type: str
        """
        if memo is None:
            raise ValueError("Invalid value for `memo`, must not be `None`")  # noqa: E501

        self._memo = memo

    @property
    def network_fees(self):
        """Gets the network_fees of this SwapMetadata.  # noqa: E501


        :return: The network_fees of this SwapMetadata.  # noqa: E501
        :rtype: NetworkFees
        """
        return self._network_fees

    @network_fees.setter
    def network_fees(self, network_fees):
        """Sets the network_fees of this SwapMetadata.


        :param network_fees: The network_fees of this SwapMetadata.  # noqa: E501
        :type: NetworkFees
        """
        if network_fees is None:
            raise ValueError("Invalid value for `network_fees`, must not be `None`")  # noqa: E501

        self._network_fees = network_fees

    @property
    def streaming_swap_meta(self):
        """Gets the streaming_swap_meta of this SwapMetadata.  # noqa: E501


        :return: The streaming_swap_meta of this SwapMetadata.  # noqa: E501
        :rtype: StreamingSwapMeta
        """
        return self._streaming_swap_meta

    @streaming_swap_meta.setter
    def streaming_swap_meta(self, streaming_swap_meta):
        """Sets the streaming_swap_meta of this SwapMetadata.


        :param streaming_swap_meta: The streaming_swap_meta of this SwapMetadata.  # noqa: E501
        :type: StreamingSwapMeta
        """

        self._streaming_swap_meta = streaming_swap_meta

    @property
    def swap_slip(self):
        """Gets the swap_slip of this SwapMetadata.  # noqa: E501

        Int64 (Basis points, 0-10000, where 10000=100%), swap slip percentage  # noqa: E501

        :return: The swap_slip of this SwapMetadata.  # noqa: E501
        :rtype: str
        """
        return self._swap_slip

    @swap_slip.setter
    def swap_slip(self, swap_slip):
        """Sets the swap_slip of this SwapMetadata.

        Int64 (Basis points, 0-10000, where 10000=100%), swap slip percentage  # noqa: E501

        :param swap_slip: The swap_slip of this SwapMetadata.  # noqa: E501
        :type: str
        """
        if swap_slip is None:
            raise ValueError("Invalid value for `swap_slip`, must not be `None`")  # noqa: E501

        self._swap_slip = swap_slip

    @property
    def swap_target(self):
        """Gets the swap_target of this SwapMetadata.  # noqa: E501

        Int64(e8), minimum output amount specified for the swap  # noqa: E501

        :return: The swap_target of this SwapMetadata.  # noqa: E501
        :rtype: str
        """
        return self._swap_target

    @swap_target.setter
    def swap_target(self, swap_target):
        """Sets the swap_target of this SwapMetadata.

        Int64(e8), minimum output amount specified for the swap  # noqa: E501

        :param swap_target: The swap_target of this SwapMetadata.  # noqa: E501
        :type: str
        """
        if swap_target is None:
            raise ValueError("Invalid value for `swap_target`, must not be `None`")  # noqa: E501

        self._swap_target = swap_target

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
        if issubclass(SwapMetadata, dict):
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
        if not isinstance(other, SwapMetadata):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other

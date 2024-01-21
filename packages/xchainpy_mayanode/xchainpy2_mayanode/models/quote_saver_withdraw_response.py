# coding: utf-8

"""
    Mayanode API

    Mayanode REST API.  # noqa: E501

    OpenAPI spec version: 1.108.1
    Contact: devs@mayachain.org
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

import pprint
import re  # noqa: F401

import six

class QuoteSaverWithdrawResponse(object):
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
        'inbound_address': 'str',
        'memo': 'str',
        'dust_amount': 'str',
        'expected_amount_out': 'str',
        'outbound_delay_blocks': 'int',
        'outbound_delay_seconds': 'int',
        'fees': 'QuoteFees',
        'slippage_bps': 'int'
    }

    attribute_map = {
        'inbound_address': 'inbound_address',
        'memo': 'memo',
        'dust_amount': 'dust_amount',
        'expected_amount_out': 'expected_amount_out',
        'outbound_delay_blocks': 'outbound_delay_blocks',
        'outbound_delay_seconds': 'outbound_delay_seconds',
        'fees': 'fees',
        'slippage_bps': 'slippage_bps'
    }

    def __init__(self, inbound_address=None, memo=None, dust_amount=None, expected_amount_out=None, outbound_delay_blocks=None, outbound_delay_seconds=None, fees=None, slippage_bps=None):  # noqa: E501
        """QuoteSaverWithdrawResponse - a model defined in Swagger"""  # noqa: E501
        self._inbound_address = None
        self._memo = None
        self._dust_amount = None
        self._expected_amount_out = None
        self._outbound_delay_blocks = None
        self._outbound_delay_seconds = None
        self._fees = None
        self._slippage_bps = None
        self.discriminator = None
        self.inbound_address = inbound_address
        self.memo = memo
        self.dust_amount = dust_amount
        self.expected_amount_out = expected_amount_out
        self.outbound_delay_blocks = outbound_delay_blocks
        self.outbound_delay_seconds = outbound_delay_seconds
        self.fees = fees
        self.slippage_bps = slippage_bps

    @property
    def inbound_address(self):
        """Gets the inbound_address of this QuoteSaverWithdrawResponse.  # noqa: E501

        the inbound address for the transaction on the source chain  # noqa: E501

        :return: The inbound_address of this QuoteSaverWithdrawResponse.  # noqa: E501
        :rtype: str
        """
        return self._inbound_address

    @inbound_address.setter
    def inbound_address(self, inbound_address):
        """Sets the inbound_address of this QuoteSaverWithdrawResponse.

        the inbound address for the transaction on the source chain  # noqa: E501

        :param inbound_address: The inbound_address of this QuoteSaverWithdrawResponse.  # noqa: E501
        :type: str
        """
        if inbound_address is None:
            raise ValueError("Invalid value for `inbound_address`, must not be `None`")  # noqa: E501

        self._inbound_address = inbound_address

    @property
    def memo(self):
        """Gets the memo of this QuoteSaverWithdrawResponse.  # noqa: E501

        generated memo for the withdraw, the client can use this OR send the dust amount  # noqa: E501

        :return: The memo of this QuoteSaverWithdrawResponse.  # noqa: E501
        :rtype: str
        """
        return self._memo

    @memo.setter
    def memo(self, memo):
        """Sets the memo of this QuoteSaverWithdrawResponse.

        generated memo for the withdraw, the client can use this OR send the dust amount  # noqa: E501

        :param memo: The memo of this QuoteSaverWithdrawResponse.  # noqa: E501
        :type: str
        """
        if memo is None:
            raise ValueError("Invalid value for `memo`, must not be `None`")  # noqa: E501

        self._memo = memo

    @property
    def dust_amount(self):
        """Gets the dust_amount of this QuoteSaverWithdrawResponse.  # noqa: E501

        the dust amount of the target asset the user should send to initialize the withdraw, the client can send this OR provide the memo  # noqa: E501

        :return: The dust_amount of this QuoteSaverWithdrawResponse.  # noqa: E501
        :rtype: str
        """
        return self._dust_amount

    @dust_amount.setter
    def dust_amount(self, dust_amount):
        """Sets the dust_amount of this QuoteSaverWithdrawResponse.

        the dust amount of the target asset the user should send to initialize the withdraw, the client can send this OR provide the memo  # noqa: E501

        :param dust_amount: The dust_amount of this QuoteSaverWithdrawResponse.  # noqa: E501
        :type: str
        """
        if dust_amount is None:
            raise ValueError("Invalid value for `dust_amount`, must not be `None`")  # noqa: E501

        self._dust_amount = dust_amount

    @property
    def expected_amount_out(self):
        """Gets the expected_amount_out of this QuoteSaverWithdrawResponse.  # noqa: E501

        the minimum amount of the target asset the user can expect to withdraw after fees in 1e8 decimals  # noqa: E501

        :return: The expected_amount_out of this QuoteSaverWithdrawResponse.  # noqa: E501
        :rtype: str
        """
        return self._expected_amount_out

    @expected_amount_out.setter
    def expected_amount_out(self, expected_amount_out):
        """Sets the expected_amount_out of this QuoteSaverWithdrawResponse.

        the minimum amount of the target asset the user can expect to withdraw after fees in 1e8 decimals  # noqa: E501

        :param expected_amount_out: The expected_amount_out of this QuoteSaverWithdrawResponse.  # noqa: E501
        :type: str
        """
        if expected_amount_out is None:
            raise ValueError("Invalid value for `expected_amount_out`, must not be `None`")  # noqa: E501

        self._expected_amount_out = expected_amount_out

    @property
    def outbound_delay_blocks(self):
        """Gets the outbound_delay_blocks of this QuoteSaverWithdrawResponse.  # noqa: E501

        the number of mayachain blocks the outbound will be delayed  # noqa: E501

        :return: The outbound_delay_blocks of this QuoteSaverWithdrawResponse.  # noqa: E501
        :rtype: int
        """
        return self._outbound_delay_blocks

    @outbound_delay_blocks.setter
    def outbound_delay_blocks(self, outbound_delay_blocks):
        """Sets the outbound_delay_blocks of this QuoteSaverWithdrawResponse.

        the number of mayachain blocks the outbound will be delayed  # noqa: E501

        :param outbound_delay_blocks: The outbound_delay_blocks of this QuoteSaverWithdrawResponse.  # noqa: E501
        :type: int
        """
        if outbound_delay_blocks is None:
            raise ValueError("Invalid value for `outbound_delay_blocks`, must not be `None`")  # noqa: E501

        self._outbound_delay_blocks = outbound_delay_blocks

    @property
    def outbound_delay_seconds(self):
        """Gets the outbound_delay_seconds of this QuoteSaverWithdrawResponse.  # noqa: E501

        the approximate seconds for the outbound delay before it will be sent  # noqa: E501

        :return: The outbound_delay_seconds of this QuoteSaverWithdrawResponse.  # noqa: E501
        :rtype: int
        """
        return self._outbound_delay_seconds

    @outbound_delay_seconds.setter
    def outbound_delay_seconds(self, outbound_delay_seconds):
        """Sets the outbound_delay_seconds of this QuoteSaverWithdrawResponse.

        the approximate seconds for the outbound delay before it will be sent  # noqa: E501

        :param outbound_delay_seconds: The outbound_delay_seconds of this QuoteSaverWithdrawResponse.  # noqa: E501
        :type: int
        """
        if outbound_delay_seconds is None:
            raise ValueError("Invalid value for `outbound_delay_seconds`, must not be `None`")  # noqa: E501

        self._outbound_delay_seconds = outbound_delay_seconds

    @property
    def fees(self):
        """Gets the fees of this QuoteSaverWithdrawResponse.  # noqa: E501


        :return: The fees of this QuoteSaverWithdrawResponse.  # noqa: E501
        :rtype: QuoteFees
        """
        return self._fees

    @fees.setter
    def fees(self, fees):
        """Sets the fees of this QuoteSaverWithdrawResponse.


        :param fees: The fees of this QuoteSaverWithdrawResponse.  # noqa: E501
        :type: QuoteFees
        """
        if fees is None:
            raise ValueError("Invalid value for `fees`, must not be `None`")  # noqa: E501

        self._fees = fees

    @property
    def slippage_bps(self):
        """Gets the slippage_bps of this QuoteSaverWithdrawResponse.  # noqa: E501

        the swap slippage in basis points  # noqa: E501

        :return: The slippage_bps of this QuoteSaverWithdrawResponse.  # noqa: E501
        :rtype: int
        """
        return self._slippage_bps

    @slippage_bps.setter
    def slippage_bps(self, slippage_bps):
        """Sets the slippage_bps of this QuoteSaverWithdrawResponse.

        the swap slippage in basis points  # noqa: E501

        :param slippage_bps: The slippage_bps of this QuoteSaverWithdrawResponse.  # noqa: E501
        :type: int
        """
        if slippage_bps is None:
            raise ValueError("Invalid value for `slippage_bps`, must not be `None`")  # noqa: E501

        self._slippage_bps = slippage_bps

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
        if issubclass(QuoteSaverWithdrawResponse, dict):
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
        if not isinstance(other, QuoteSaverWithdrawResponse):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other

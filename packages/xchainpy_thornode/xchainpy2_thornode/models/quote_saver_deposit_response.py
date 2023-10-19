# coding: utf-8

"""
    Thornode API

    Thornode REST API.  # noqa: E501

    OpenAPI spec version: 1.122.0
    Contact: devs@thorchain.org
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

import pprint
import re  # noqa: F401

import six

class QuoteSaverDepositResponse(object):
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
        'inbound_confirmation_blocks': 'int',
        'inbound_confirmation_seconds': 'int',
        'outbound_delay_blocks': 'int',
        'outbound_delay_seconds': 'int',
        'fees': 'QuoteFees',
        'slippage_bps': 'int',
        'streaming_slippage_bps': 'int',
        'router': 'str',
        'expiry': 'int',
        'warning': 'str',
        'notes': 'str',
        'dust_threshold': 'str',
        'recommended_min_amount_in': 'str',
        'memo': 'str',
        'expected_amount_out': 'str',
        'expected_amount_deposit': 'str'
    }

    attribute_map = {
        'inbound_address': 'inbound_address',
        'inbound_confirmation_blocks': 'inbound_confirmation_blocks',
        'inbound_confirmation_seconds': 'inbound_confirmation_seconds',
        'outbound_delay_blocks': 'outbound_delay_blocks',
        'outbound_delay_seconds': 'outbound_delay_seconds',
        'fees': 'fees',
        'slippage_bps': 'slippage_bps',
        'streaming_slippage_bps': 'streaming_slippage_bps',
        'router': 'router',
        'expiry': 'expiry',
        'warning': 'warning',
        'notes': 'notes',
        'dust_threshold': 'dust_threshold',
        'recommended_min_amount_in': 'recommended_min_amount_in',
        'memo': 'memo',
        'expected_amount_out': 'expected_amount_out',
        'expected_amount_deposit': 'expected_amount_deposit'
    }

    def __init__(self, inbound_address=None, inbound_confirmation_blocks=None, inbound_confirmation_seconds=None, outbound_delay_blocks=None, outbound_delay_seconds=None, fees=None, slippage_bps=None, streaming_slippage_bps=None, router=None, expiry=None, warning=None, notes=None, dust_threshold=None, recommended_min_amount_in=None, memo=None, expected_amount_out=None, expected_amount_deposit=None):  # noqa: E501
        """QuoteSaverDepositResponse - a model defined in Swagger"""  # noqa: E501
        self._inbound_address = None
        self._inbound_confirmation_blocks = None
        self._inbound_confirmation_seconds = None
        self._outbound_delay_blocks = None
        self._outbound_delay_seconds = None
        self._fees = None
        self._slippage_bps = None
        self._streaming_slippage_bps = None
        self._router = None
        self._expiry = None
        self._warning = None
        self._notes = None
        self._dust_threshold = None
        self._recommended_min_amount_in = None
        self._memo = None
        self._expected_amount_out = None
        self._expected_amount_deposit = None
        self.discriminator = None
        self.inbound_address = inbound_address
        if inbound_confirmation_blocks is not None:
            self.inbound_confirmation_blocks = inbound_confirmation_blocks
        if inbound_confirmation_seconds is not None:
            self.inbound_confirmation_seconds = inbound_confirmation_seconds
        if outbound_delay_blocks is not None:
            self.outbound_delay_blocks = outbound_delay_blocks
        if outbound_delay_seconds is not None:
            self.outbound_delay_seconds = outbound_delay_seconds
        self.fees = fees
        self.slippage_bps = slippage_bps
        if streaming_slippage_bps is not None:
            self.streaming_slippage_bps = streaming_slippage_bps
        if router is not None:
            self.router = router
        self.expiry = expiry
        self.warning = warning
        self.notes = notes
        if dust_threshold is not None:
            self.dust_threshold = dust_threshold
        if recommended_min_amount_in is not None:
            self.recommended_min_amount_in = recommended_min_amount_in
        self.memo = memo
        if expected_amount_out is not None:
            self.expected_amount_out = expected_amount_out
        self.expected_amount_deposit = expected_amount_deposit

    @property
    def inbound_address(self):
        """Gets the inbound_address of this QuoteSaverDepositResponse.  # noqa: E501

        the inbound address for the transaction on the source chain  # noqa: E501

        :return: The inbound_address of this QuoteSaverDepositResponse.  # noqa: E501
        :rtype: str
        """
        return self._inbound_address

    @inbound_address.setter
    def inbound_address(self, inbound_address):
        """Sets the inbound_address of this QuoteSaverDepositResponse.

        the inbound address for the transaction on the source chain  # noqa: E501

        :param inbound_address: The inbound_address of this QuoteSaverDepositResponse.  # noqa: E501
        :type: str
        """
        if inbound_address is None:
            raise ValueError("Invalid value for `inbound_address`, must not be `None`")  # noqa: E501

        self._inbound_address = inbound_address

    @property
    def inbound_confirmation_blocks(self):
        """Gets the inbound_confirmation_blocks of this QuoteSaverDepositResponse.  # noqa: E501

        the approximate number of source chain blocks required before processing  # noqa: E501

        :return: The inbound_confirmation_blocks of this QuoteSaverDepositResponse.  # noqa: E501
        :rtype: int
        """
        return self._inbound_confirmation_blocks

    @inbound_confirmation_blocks.setter
    def inbound_confirmation_blocks(self, inbound_confirmation_blocks):
        """Sets the inbound_confirmation_blocks of this QuoteSaverDepositResponse.

        the approximate number of source chain blocks required before processing  # noqa: E501

        :param inbound_confirmation_blocks: The inbound_confirmation_blocks of this QuoteSaverDepositResponse.  # noqa: E501
        :type: int
        """

        self._inbound_confirmation_blocks = inbound_confirmation_blocks

    @property
    def inbound_confirmation_seconds(self):
        """Gets the inbound_confirmation_seconds of this QuoteSaverDepositResponse.  # noqa: E501

        the approximate seconds for block confirmations required before processing  # noqa: E501

        :return: The inbound_confirmation_seconds of this QuoteSaverDepositResponse.  # noqa: E501
        :rtype: int
        """
        return self._inbound_confirmation_seconds

    @inbound_confirmation_seconds.setter
    def inbound_confirmation_seconds(self, inbound_confirmation_seconds):
        """Sets the inbound_confirmation_seconds of this QuoteSaverDepositResponse.

        the approximate seconds for block confirmations required before processing  # noqa: E501

        :param inbound_confirmation_seconds: The inbound_confirmation_seconds of this QuoteSaverDepositResponse.  # noqa: E501
        :type: int
        """

        self._inbound_confirmation_seconds = inbound_confirmation_seconds

    @property
    def outbound_delay_blocks(self):
        """Gets the outbound_delay_blocks of this QuoteSaverDepositResponse.  # noqa: E501

        the number of thorchain blocks the outbound will be delayed  # noqa: E501

        :return: The outbound_delay_blocks of this QuoteSaverDepositResponse.  # noqa: E501
        :rtype: int
        """
        return self._outbound_delay_blocks

    @outbound_delay_blocks.setter
    def outbound_delay_blocks(self, outbound_delay_blocks):
        """Sets the outbound_delay_blocks of this QuoteSaverDepositResponse.

        the number of thorchain blocks the outbound will be delayed  # noqa: E501

        :param outbound_delay_blocks: The outbound_delay_blocks of this QuoteSaverDepositResponse.  # noqa: E501
        :type: int
        """

        self._outbound_delay_blocks = outbound_delay_blocks

    @property
    def outbound_delay_seconds(self):
        """Gets the outbound_delay_seconds of this QuoteSaverDepositResponse.  # noqa: E501

        the approximate seconds for the outbound delay before it will be sent  # noqa: E501

        :return: The outbound_delay_seconds of this QuoteSaverDepositResponse.  # noqa: E501
        :rtype: int
        """
        return self._outbound_delay_seconds

    @outbound_delay_seconds.setter
    def outbound_delay_seconds(self, outbound_delay_seconds):
        """Sets the outbound_delay_seconds of this QuoteSaverDepositResponse.

        the approximate seconds for the outbound delay before it will be sent  # noqa: E501

        :param outbound_delay_seconds: The outbound_delay_seconds of this QuoteSaverDepositResponse.  # noqa: E501
        :type: int
        """

        self._outbound_delay_seconds = outbound_delay_seconds

    @property
    def fees(self):
        """Gets the fees of this QuoteSaverDepositResponse.  # noqa: E501


        :return: The fees of this QuoteSaverDepositResponse.  # noqa: E501
        :rtype: QuoteFees
        """
        return self._fees

    @fees.setter
    def fees(self, fees):
        """Sets the fees of this QuoteSaverDepositResponse.


        :param fees: The fees of this QuoteSaverDepositResponse.  # noqa: E501
        :type: QuoteFees
        """
        if fees is None:
            raise ValueError("Invalid value for `fees`, must not be `None`")  # noqa: E501

        self._fees = fees

    @property
    def slippage_bps(self):
        """Gets the slippage_bps of this QuoteSaverDepositResponse.  # noqa: E501

        Deprecated - migrate to fees object.  # noqa: E501

        :return: The slippage_bps of this QuoteSaverDepositResponse.  # noqa: E501
        :rtype: int
        """
        return self._slippage_bps

    @slippage_bps.setter
    def slippage_bps(self, slippage_bps):
        """Sets the slippage_bps of this QuoteSaverDepositResponse.

        Deprecated - migrate to fees object.  # noqa: E501

        :param slippage_bps: The slippage_bps of this QuoteSaverDepositResponse.  # noqa: E501
        :type: int
        """
        if slippage_bps is None:
            raise ValueError("Invalid value for `slippage_bps`, must not be `None`")  # noqa: E501

        self._slippage_bps = slippage_bps

    @property
    def streaming_slippage_bps(self):
        """Gets the streaming_slippage_bps of this QuoteSaverDepositResponse.  # noqa: E501

        Deprecated - migrate to fees object.  # noqa: E501

        :return: The streaming_slippage_bps of this QuoteSaverDepositResponse.  # noqa: E501
        :rtype: int
        """
        return self._streaming_slippage_bps

    @streaming_slippage_bps.setter
    def streaming_slippage_bps(self, streaming_slippage_bps):
        """Sets the streaming_slippage_bps of this QuoteSaverDepositResponse.

        Deprecated - migrate to fees object.  # noqa: E501

        :param streaming_slippage_bps: The streaming_slippage_bps of this QuoteSaverDepositResponse.  # noqa: E501
        :type: int
        """

        self._streaming_slippage_bps = streaming_slippage_bps

    @property
    def router(self):
        """Gets the router of this QuoteSaverDepositResponse.  # noqa: E501

        the EVM chain router contract address  # noqa: E501

        :return: The router of this QuoteSaverDepositResponse.  # noqa: E501
        :rtype: str
        """
        return self._router

    @router.setter
    def router(self, router):
        """Sets the router of this QuoteSaverDepositResponse.

        the EVM chain router contract address  # noqa: E501

        :param router: The router of this QuoteSaverDepositResponse.  # noqa: E501
        :type: str
        """

        self._router = router

    @property
    def expiry(self):
        """Gets the expiry of this QuoteSaverDepositResponse.  # noqa: E501

        expiration timestamp in unix seconds  # noqa: E501

        :return: The expiry of this QuoteSaverDepositResponse.  # noqa: E501
        :rtype: int
        """
        return self._expiry

    @expiry.setter
    def expiry(self, expiry):
        """Sets the expiry of this QuoteSaverDepositResponse.

        expiration timestamp in unix seconds  # noqa: E501

        :param expiry: The expiry of this QuoteSaverDepositResponse.  # noqa: E501
        :type: int
        """
        if expiry is None:
            raise ValueError("Invalid value for `expiry`, must not be `None`")  # noqa: E501

        self._expiry = expiry

    @property
    def warning(self):
        """Gets the warning of this QuoteSaverDepositResponse.  # noqa: E501

        static warning message  # noqa: E501

        :return: The warning of this QuoteSaverDepositResponse.  # noqa: E501
        :rtype: str
        """
        return self._warning

    @warning.setter
    def warning(self, warning):
        """Sets the warning of this QuoteSaverDepositResponse.

        static warning message  # noqa: E501

        :param warning: The warning of this QuoteSaverDepositResponse.  # noqa: E501
        :type: str
        """
        if warning is None:
            raise ValueError("Invalid value for `warning`, must not be `None`")  # noqa: E501

        self._warning = warning

    @property
    def notes(self):
        """Gets the notes of this QuoteSaverDepositResponse.  # noqa: E501

        chain specific quote notes  # noqa: E501

        :return: The notes of this QuoteSaverDepositResponse.  # noqa: E501
        :rtype: str
        """
        return self._notes

    @notes.setter
    def notes(self, notes):
        """Sets the notes of this QuoteSaverDepositResponse.

        chain specific quote notes  # noqa: E501

        :param notes: The notes of this QuoteSaverDepositResponse.  # noqa: E501
        :type: str
        """
        if notes is None:
            raise ValueError("Invalid value for `notes`, must not be `None`")  # noqa: E501

        self._notes = notes

    @property
    def dust_threshold(self):
        """Gets the dust_threshold of this QuoteSaverDepositResponse.  # noqa: E501

        Defines the minimum transaction size for the chain in base units (sats, wei, uatom). Transctions with asset amounts lower than the dust_threshold are ignored.  # noqa: E501

        :return: The dust_threshold of this QuoteSaverDepositResponse.  # noqa: E501
        :rtype: str
        """
        return self._dust_threshold

    @dust_threshold.setter
    def dust_threshold(self, dust_threshold):
        """Sets the dust_threshold of this QuoteSaverDepositResponse.

        Defines the minimum transaction size for the chain in base units (sats, wei, uatom). Transctions with asset amounts lower than the dust_threshold are ignored.  # noqa: E501

        :param dust_threshold: The dust_threshold of this QuoteSaverDepositResponse.  # noqa: E501
        :type: str
        """

        self._dust_threshold = dust_threshold

    @property
    def recommended_min_amount_in(self):
        """Gets the recommended_min_amount_in of this QuoteSaverDepositResponse.  # noqa: E501

        The recommended minimum inbound amount for this transaction type & inbound asset. Sending less than this amount could result in failed refunds.  # noqa: E501

        :return: The recommended_min_amount_in of this QuoteSaverDepositResponse.  # noqa: E501
        :rtype: str
        """
        return self._recommended_min_amount_in

    @recommended_min_amount_in.setter
    def recommended_min_amount_in(self, recommended_min_amount_in):
        """Sets the recommended_min_amount_in of this QuoteSaverDepositResponse.

        The recommended minimum inbound amount for this transaction type & inbound asset. Sending less than this amount could result in failed refunds.  # noqa: E501

        :param recommended_min_amount_in: The recommended_min_amount_in of this QuoteSaverDepositResponse.  # noqa: E501
        :type: str
        """

        self._recommended_min_amount_in = recommended_min_amount_in

    @property
    def memo(self):
        """Gets the memo of this QuoteSaverDepositResponse.  # noqa: E501

        generated memo for the deposit  # noqa: E501

        :return: The memo of this QuoteSaverDepositResponse.  # noqa: E501
        :rtype: str
        """
        return self._memo

    @memo.setter
    def memo(self, memo):
        """Sets the memo of this QuoteSaverDepositResponse.

        generated memo for the deposit  # noqa: E501

        :param memo: The memo of this QuoteSaverDepositResponse.  # noqa: E501
        :type: str
        """
        if memo is None:
            raise ValueError("Invalid value for `memo`, must not be `None`")  # noqa: E501

        self._memo = memo

    @property
    def expected_amount_out(self):
        """Gets the expected_amount_out of this QuoteSaverDepositResponse.  # noqa: E501

        same as expected_amount_deposit, to be deprecated in favour of expected_amount_deposit  # noqa: E501

        :return: The expected_amount_out of this QuoteSaverDepositResponse.  # noqa: E501
        :rtype: str
        """
        return self._expected_amount_out

    @expected_amount_out.setter
    def expected_amount_out(self, expected_amount_out):
        """Sets the expected_amount_out of this QuoteSaverDepositResponse.

        same as expected_amount_deposit, to be deprecated in favour of expected_amount_deposit  # noqa: E501

        :param expected_amount_out: The expected_amount_out of this QuoteSaverDepositResponse.  # noqa: E501
        :type: str
        """

        self._expected_amount_out = expected_amount_out

    @property
    def expected_amount_deposit(self):
        """Gets the expected_amount_deposit of this QuoteSaverDepositResponse.  # noqa: E501

        the amount of the target asset the user can expect to deposit after fees  # noqa: E501

        :return: The expected_amount_deposit of this QuoteSaverDepositResponse.  # noqa: E501
        :rtype: str
        """
        return self._expected_amount_deposit

    @expected_amount_deposit.setter
    def expected_amount_deposit(self, expected_amount_deposit):
        """Sets the expected_amount_deposit of this QuoteSaverDepositResponse.

        the amount of the target asset the user can expect to deposit after fees  # noqa: E501

        :param expected_amount_deposit: The expected_amount_deposit of this QuoteSaverDepositResponse.  # noqa: E501
        :type: str
        """
        if expected_amount_deposit is None:
            raise ValueError("Invalid value for `expected_amount_deposit`, must not be `None`")  # noqa: E501

        self._expected_amount_deposit = expected_amount_deposit

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
        if issubclass(QuoteSaverDepositResponse, dict):
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
        if not isinstance(other, QuoteSaverDepositResponse):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other

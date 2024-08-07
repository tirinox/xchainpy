# coding: utf-8

"""
    Mayanode API

    Mayanode REST API.  # noqa: E501

    OpenAPI spec version: 1.110.0
    Contact: devs@mayachain.org
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

import pprint
import re  # noqa: F401

import six

class QuoteSwapResponse(object):
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
        'router': 'str',
        'expiry': 'int',
        'warning': 'str',
        'notes': 'str',
        'dust_threshold': 'str',
        'recommended_min_amount_in': 'str',
        'recommended_gas_rate': 'str',
        'gas_rate_units': 'str',
        'memo': 'str',
        'expected_amount_out': 'str',
        'max_streaming_quantity': 'int',
        'streaming_swap_blocks': 'int',
        'streaming_swap_seconds': 'int',
        'total_swap_seconds': 'int'
    }

    attribute_map = {
        'inbound_address': 'inbound_address',
        'inbound_confirmation_blocks': 'inbound_confirmation_blocks',
        'inbound_confirmation_seconds': 'inbound_confirmation_seconds',
        'outbound_delay_blocks': 'outbound_delay_blocks',
        'outbound_delay_seconds': 'outbound_delay_seconds',
        'fees': 'fees',
        'router': 'router',
        'expiry': 'expiry',
        'warning': 'warning',
        'notes': 'notes',
        'dust_threshold': 'dust_threshold',
        'recommended_min_amount_in': 'recommended_min_amount_in',
        'recommended_gas_rate': 'recommended_gas_rate',
        'gas_rate_units': 'gas_rate_units',
        'memo': 'memo',
        'expected_amount_out': 'expected_amount_out',
        'max_streaming_quantity': 'max_streaming_quantity',
        'streaming_swap_blocks': 'streaming_swap_blocks',
        'streaming_swap_seconds': 'streaming_swap_seconds',
        'total_swap_seconds': 'total_swap_seconds'
    }

    def __init__(self, inbound_address=None, inbound_confirmation_blocks=None, inbound_confirmation_seconds=None, outbound_delay_blocks=None, outbound_delay_seconds=None, fees=None, router=None, expiry=None, warning=None, notes=None, dust_threshold=None, recommended_min_amount_in=None, recommended_gas_rate=None, gas_rate_units=None, memo=None, expected_amount_out=None, max_streaming_quantity=None, streaming_swap_blocks=None, streaming_swap_seconds=None, total_swap_seconds=None):  # noqa: E501
        """QuoteSwapResponse - a model defined in Swagger"""  # noqa: E501
        self._inbound_address = None
        self._inbound_confirmation_blocks = None
        self._inbound_confirmation_seconds = None
        self._outbound_delay_blocks = None
        self._outbound_delay_seconds = None
        self._fees = None
        self._router = None
        self._expiry = None
        self._warning = None
        self._notes = None
        self._dust_threshold = None
        self._recommended_min_amount_in = None
        self._recommended_gas_rate = None
        self._gas_rate_units = None
        self._memo = None
        self._expected_amount_out = None
        self._max_streaming_quantity = None
        self._streaming_swap_blocks = None
        self._streaming_swap_seconds = None
        self._total_swap_seconds = None
        self.discriminator = None
        if inbound_address is not None:
            self.inbound_address = inbound_address
        if inbound_confirmation_blocks is not None:
            self.inbound_confirmation_blocks = inbound_confirmation_blocks
        if inbound_confirmation_seconds is not None:
            self.inbound_confirmation_seconds = inbound_confirmation_seconds
        self.outbound_delay_blocks = outbound_delay_blocks
        self.outbound_delay_seconds = outbound_delay_seconds
        self.fees = fees
        if router is not None:
            self.router = router
        self.expiry = expiry
        self.warning = warning
        self.notes = notes
        if dust_threshold is not None:
            self.dust_threshold = dust_threshold
        if recommended_min_amount_in is not None:
            self.recommended_min_amount_in = recommended_min_amount_in
        if recommended_gas_rate is not None:
            self.recommended_gas_rate = recommended_gas_rate
        if gas_rate_units is not None:
            self.gas_rate_units = gas_rate_units
        if memo is not None:
            self.memo = memo
        self.expected_amount_out = expected_amount_out
        if max_streaming_quantity is not None:
            self.max_streaming_quantity = max_streaming_quantity
        if streaming_swap_blocks is not None:
            self.streaming_swap_blocks = streaming_swap_blocks
        if streaming_swap_seconds is not None:
            self.streaming_swap_seconds = streaming_swap_seconds
        if total_swap_seconds is not None:
            self.total_swap_seconds = total_swap_seconds

    @property
    def inbound_address(self):
        """Gets the inbound_address of this QuoteSwapResponse.  # noqa: E501

        the inbound address for the transaction on the source chain  # noqa: E501

        :return: The inbound_address of this QuoteSwapResponse.  # noqa: E501
        :rtype: str
        """
        return self._inbound_address

    @inbound_address.setter
    def inbound_address(self, inbound_address):
        """Sets the inbound_address of this QuoteSwapResponse.

        the inbound address for the transaction on the source chain  # noqa: E501

        :param inbound_address: The inbound_address of this QuoteSwapResponse.  # noqa: E501
        :type: str
        """

        self._inbound_address = inbound_address

    @property
    def inbound_confirmation_blocks(self):
        """Gets the inbound_confirmation_blocks of this QuoteSwapResponse.  # noqa: E501

        the approximate number of source chain blocks required before processing  # noqa: E501

        :return: The inbound_confirmation_blocks of this QuoteSwapResponse.  # noqa: E501
        :rtype: int
        """
        return self._inbound_confirmation_blocks

    @inbound_confirmation_blocks.setter
    def inbound_confirmation_blocks(self, inbound_confirmation_blocks):
        """Sets the inbound_confirmation_blocks of this QuoteSwapResponse.

        the approximate number of source chain blocks required before processing  # noqa: E501

        :param inbound_confirmation_blocks: The inbound_confirmation_blocks of this QuoteSwapResponse.  # noqa: E501
        :type: int
        """

        self._inbound_confirmation_blocks = inbound_confirmation_blocks

    @property
    def inbound_confirmation_seconds(self):
        """Gets the inbound_confirmation_seconds of this QuoteSwapResponse.  # noqa: E501

        the approximate seconds for block confirmations required before processing  # noqa: E501

        :return: The inbound_confirmation_seconds of this QuoteSwapResponse.  # noqa: E501
        :rtype: int
        """
        return self._inbound_confirmation_seconds

    @inbound_confirmation_seconds.setter
    def inbound_confirmation_seconds(self, inbound_confirmation_seconds):
        """Sets the inbound_confirmation_seconds of this QuoteSwapResponse.

        the approximate seconds for block confirmations required before processing  # noqa: E501

        :param inbound_confirmation_seconds: The inbound_confirmation_seconds of this QuoteSwapResponse.  # noqa: E501
        :type: int
        """

        self._inbound_confirmation_seconds = inbound_confirmation_seconds

    @property
    def outbound_delay_blocks(self):
        """Gets the outbound_delay_blocks of this QuoteSwapResponse.  # noqa: E501

        the number of mayachain blocks the outbound will be delayed  # noqa: E501

        :return: The outbound_delay_blocks of this QuoteSwapResponse.  # noqa: E501
        :rtype: int
        """
        return self._outbound_delay_blocks

    @outbound_delay_blocks.setter
    def outbound_delay_blocks(self, outbound_delay_blocks):
        """Sets the outbound_delay_blocks of this QuoteSwapResponse.

        the number of mayachain blocks the outbound will be delayed  # noqa: E501

        :param outbound_delay_blocks: The outbound_delay_blocks of this QuoteSwapResponse.  # noqa: E501
        :type: int
        """
        if outbound_delay_blocks is None:
            raise ValueError("Invalid value for `outbound_delay_blocks`, must not be `None`")  # noqa: E501

        self._outbound_delay_blocks = outbound_delay_blocks

    @property
    def outbound_delay_seconds(self):
        """Gets the outbound_delay_seconds of this QuoteSwapResponse.  # noqa: E501

        the approximate seconds for the outbound delay before it will be sent  # noqa: E501

        :return: The outbound_delay_seconds of this QuoteSwapResponse.  # noqa: E501
        :rtype: int
        """
        return self._outbound_delay_seconds

    @outbound_delay_seconds.setter
    def outbound_delay_seconds(self, outbound_delay_seconds):
        """Sets the outbound_delay_seconds of this QuoteSwapResponse.

        the approximate seconds for the outbound delay before it will be sent  # noqa: E501

        :param outbound_delay_seconds: The outbound_delay_seconds of this QuoteSwapResponse.  # noqa: E501
        :type: int
        """
        if outbound_delay_seconds is None:
            raise ValueError("Invalid value for `outbound_delay_seconds`, must not be `None`")  # noqa: E501

        self._outbound_delay_seconds = outbound_delay_seconds

    @property
    def fees(self):
        """Gets the fees of this QuoteSwapResponse.  # noqa: E501


        :return: The fees of this QuoteSwapResponse.  # noqa: E501
        :rtype: QuoteFees
        """
        return self._fees

    @fees.setter
    def fees(self, fees):
        """Sets the fees of this QuoteSwapResponse.


        :param fees: The fees of this QuoteSwapResponse.  # noqa: E501
        :type: QuoteFees
        """
        if fees is None:
            raise ValueError("Invalid value for `fees`, must not be `None`")  # noqa: E501

        self._fees = fees

    @property
    def router(self):
        """Gets the router of this QuoteSwapResponse.  # noqa: E501

        the EVM chain router contract address  # noqa: E501

        :return: The router of this QuoteSwapResponse.  # noqa: E501
        :rtype: str
        """
        return self._router

    @router.setter
    def router(self, router):
        """Sets the router of this QuoteSwapResponse.

        the EVM chain router contract address  # noqa: E501

        :param router: The router of this QuoteSwapResponse.  # noqa: E501
        :type: str
        """

        self._router = router

    @property
    def expiry(self):
        """Gets the expiry of this QuoteSwapResponse.  # noqa: E501

        expiration timestamp in unix seconds  # noqa: E501

        :return: The expiry of this QuoteSwapResponse.  # noqa: E501
        :rtype: int
        """
        return self._expiry

    @expiry.setter
    def expiry(self, expiry):
        """Sets the expiry of this QuoteSwapResponse.

        expiration timestamp in unix seconds  # noqa: E501

        :param expiry: The expiry of this QuoteSwapResponse.  # noqa: E501
        :type: int
        """
        if expiry is None:
            raise ValueError("Invalid value for `expiry`, must not be `None`")  # noqa: E501

        self._expiry = expiry

    @property
    def warning(self):
        """Gets the warning of this QuoteSwapResponse.  # noqa: E501

        static warning message  # noqa: E501

        :return: The warning of this QuoteSwapResponse.  # noqa: E501
        :rtype: str
        """
        return self._warning

    @warning.setter
    def warning(self, warning):
        """Sets the warning of this QuoteSwapResponse.

        static warning message  # noqa: E501

        :param warning: The warning of this QuoteSwapResponse.  # noqa: E501
        :type: str
        """
        if warning is None:
            raise ValueError("Invalid value for `warning`, must not be `None`")  # noqa: E501

        self._warning = warning

    @property
    def notes(self):
        """Gets the notes of this QuoteSwapResponse.  # noqa: E501

        chain specific quote notes  # noqa: E501

        :return: The notes of this QuoteSwapResponse.  # noqa: E501
        :rtype: str
        """
        return self._notes

    @notes.setter
    def notes(self, notes):
        """Sets the notes of this QuoteSwapResponse.

        chain specific quote notes  # noqa: E501

        :param notes: The notes of this QuoteSwapResponse.  # noqa: E501
        :type: str
        """
        if notes is None:
            raise ValueError("Invalid value for `notes`, must not be `None`")  # noqa: E501

        self._notes = notes

    @property
    def dust_threshold(self):
        """Gets the dust_threshold of this QuoteSwapResponse.  # noqa: E501

        Defines the minimum transaction size for the chain in base units (sats, wei, uatom). Transactions with asset amounts lower than the dust_threshold are ignored.  # noqa: E501

        :return: The dust_threshold of this QuoteSwapResponse.  # noqa: E501
        :rtype: str
        """
        return self._dust_threshold

    @dust_threshold.setter
    def dust_threshold(self, dust_threshold):
        """Sets the dust_threshold of this QuoteSwapResponse.

        Defines the minimum transaction size for the chain in base units (sats, wei, uatom). Transactions with asset amounts lower than the dust_threshold are ignored.  # noqa: E501

        :param dust_threshold: The dust_threshold of this QuoteSwapResponse.  # noqa: E501
        :type: str
        """

        self._dust_threshold = dust_threshold

    @property
    def recommended_min_amount_in(self):
        """Gets the recommended_min_amount_in of this QuoteSwapResponse.  # noqa: E501

        The recommended minimum inbound amount for this transaction type & inbound asset. Sending less than this amount could result in failed refunds.  # noqa: E501

        :return: The recommended_min_amount_in of this QuoteSwapResponse.  # noqa: E501
        :rtype: str
        """
        return self._recommended_min_amount_in

    @recommended_min_amount_in.setter
    def recommended_min_amount_in(self, recommended_min_amount_in):
        """Sets the recommended_min_amount_in of this QuoteSwapResponse.

        The recommended minimum inbound amount for this transaction type & inbound asset. Sending less than this amount could result in failed refunds.  # noqa: E501

        :param recommended_min_amount_in: The recommended_min_amount_in of this QuoteSwapResponse.  # noqa: E501
        :type: str
        """

        self._recommended_min_amount_in = recommended_min_amount_in

    @property
    def recommended_gas_rate(self):
        """Gets the recommended_gas_rate of this QuoteSwapResponse.  # noqa: E501

        the recommended gas rate to use for the inbound to ensure timely confirmation  # noqa: E501

        :return: The recommended_gas_rate of this QuoteSwapResponse.  # noqa: E501
        :rtype: str
        """
        return self._recommended_gas_rate

    @recommended_gas_rate.setter
    def recommended_gas_rate(self, recommended_gas_rate):
        """Sets the recommended_gas_rate of this QuoteSwapResponse.

        the recommended gas rate to use for the inbound to ensure timely confirmation  # noqa: E501

        :param recommended_gas_rate: The recommended_gas_rate of this QuoteSwapResponse.  # noqa: E501
        :type: str
        """

        self._recommended_gas_rate = recommended_gas_rate

    @property
    def gas_rate_units(self):
        """Gets the gas_rate_units of this QuoteSwapResponse.  # noqa: E501

        the units of the recommended gas rate  # noqa: E501

        :return: The gas_rate_units of this QuoteSwapResponse.  # noqa: E501
        :rtype: str
        """
        return self._gas_rate_units

    @gas_rate_units.setter
    def gas_rate_units(self, gas_rate_units):
        """Sets the gas_rate_units of this QuoteSwapResponse.

        the units of the recommended gas rate  # noqa: E501

        :param gas_rate_units: The gas_rate_units of this QuoteSwapResponse.  # noqa: E501
        :type: str
        """

        self._gas_rate_units = gas_rate_units

    @property
    def memo(self):
        """Gets the memo of this QuoteSwapResponse.  # noqa: E501

        generated memo for the swap  # noqa: E501

        :return: The memo of this QuoteSwapResponse.  # noqa: E501
        :rtype: str
        """
        return self._memo

    @memo.setter
    def memo(self, memo):
        """Sets the memo of this QuoteSwapResponse.

        generated memo for the swap  # noqa: E501

        :param memo: The memo of this QuoteSwapResponse.  # noqa: E501
        :type: str
        """

        self._memo = memo

    @property
    def expected_amount_out(self):
        """Gets the expected_amount_out of this QuoteSwapResponse.  # noqa: E501

        the amount of the target asset the user can expect to receive after fees  # noqa: E501

        :return: The expected_amount_out of this QuoteSwapResponse.  # noqa: E501
        :rtype: str
        """
        return self._expected_amount_out

    @expected_amount_out.setter
    def expected_amount_out(self, expected_amount_out):
        """Sets the expected_amount_out of this QuoteSwapResponse.

        the amount of the target asset the user can expect to receive after fees  # noqa: E501

        :param expected_amount_out: The expected_amount_out of this QuoteSwapResponse.  # noqa: E501
        :type: str
        """
        if expected_amount_out is None:
            raise ValueError("Invalid value for `expected_amount_out`, must not be `None`")  # noqa: E501

        self._expected_amount_out = expected_amount_out

    @property
    def max_streaming_quantity(self):
        """Gets the max_streaming_quantity of this QuoteSwapResponse.  # noqa: E501

        the maximum amount of trades a streaming swap can do for a trade  # noqa: E501

        :return: The max_streaming_quantity of this QuoteSwapResponse.  # noqa: E501
        :rtype: int
        """
        return self._max_streaming_quantity

    @max_streaming_quantity.setter
    def max_streaming_quantity(self, max_streaming_quantity):
        """Sets the max_streaming_quantity of this QuoteSwapResponse.

        the maximum amount of trades a streaming swap can do for a trade  # noqa: E501

        :param max_streaming_quantity: The max_streaming_quantity of this QuoteSwapResponse.  # noqa: E501
        :type: int
        """

        self._max_streaming_quantity = max_streaming_quantity

    @property
    def streaming_swap_blocks(self):
        """Gets the streaming_swap_blocks of this QuoteSwapResponse.  # noqa: E501

        the number of blocks the streaming swap will execute over  # noqa: E501

        :return: The streaming_swap_blocks of this QuoteSwapResponse.  # noqa: E501
        :rtype: int
        """
        return self._streaming_swap_blocks

    @streaming_swap_blocks.setter
    def streaming_swap_blocks(self, streaming_swap_blocks):
        """Sets the streaming_swap_blocks of this QuoteSwapResponse.

        the number of blocks the streaming swap will execute over  # noqa: E501

        :param streaming_swap_blocks: The streaming_swap_blocks of this QuoteSwapResponse.  # noqa: E501
        :type: int
        """

        self._streaming_swap_blocks = streaming_swap_blocks

    @property
    def streaming_swap_seconds(self):
        """Gets the streaming_swap_seconds of this QuoteSwapResponse.  # noqa: E501

        approx the number of seconds the streaming swap will execute over  # noqa: E501

        :return: The streaming_swap_seconds of this QuoteSwapResponse.  # noqa: E501
        :rtype: int
        """
        return self._streaming_swap_seconds

    @streaming_swap_seconds.setter
    def streaming_swap_seconds(self, streaming_swap_seconds):
        """Sets the streaming_swap_seconds of this QuoteSwapResponse.

        approx the number of seconds the streaming swap will execute over  # noqa: E501

        :param streaming_swap_seconds: The streaming_swap_seconds of this QuoteSwapResponse.  # noqa: E501
        :type: int
        """

        self._streaming_swap_seconds = streaming_swap_seconds

    @property
    def total_swap_seconds(self):
        """Gets the total_swap_seconds of this QuoteSwapResponse.  # noqa: E501

        total number of seconds a swap is expected to take (inbound conf + streaming swap + outbound delay)  # noqa: E501

        :return: The total_swap_seconds of this QuoteSwapResponse.  # noqa: E501
        :rtype: int
        """
        return self._total_swap_seconds

    @total_swap_seconds.setter
    def total_swap_seconds(self, total_swap_seconds):
        """Sets the total_swap_seconds of this QuoteSwapResponse.

        total number of seconds a swap is expected to take (inbound conf + streaming swap + outbound delay)  # noqa: E501

        :param total_swap_seconds: The total_swap_seconds of this QuoteSwapResponse.  # noqa: E501
        :type: int
        """

        self._total_swap_seconds = total_swap_seconds

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
        if issubclass(QuoteSwapResponse, dict):
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
        if not isinstance(other, QuoteSwapResponse):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other

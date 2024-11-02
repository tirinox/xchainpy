# coding: utf-8

"""
    Thornode API

    Thornode REST API.  # noqa: E501

    OpenAPI spec version: 2.137.1
    Contact: devs@thorchain.org
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

import pprint
import re  # noqa: F401

import six

class TxStagesResponse(object):
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
        'inbound_observed': 'InboundObservedStage',
        'inbound_confirmation_counted': 'InboundConfirmationCountedStage',
        'inbound_finalised': 'InboundFinalisedStage',
        'swap_status': 'SwapStatus',
        'swap_finalised': 'SwapFinalisedStage',
        'outbound_delay': 'OutboundDelayStage',
        'outbound_signed': 'OutboundSignedStage'
    }

    attribute_map = {
        'inbound_observed': 'inbound_observed',
        'inbound_confirmation_counted': 'inbound_confirmation_counted',
        'inbound_finalised': 'inbound_finalised',
        'swap_status': 'swap_status',
        'swap_finalised': 'swap_finalised',
        'outbound_delay': 'outbound_delay',
        'outbound_signed': 'outbound_signed'
    }

    def __init__(self, inbound_observed=None, inbound_confirmation_counted=None, inbound_finalised=None, swap_status=None, swap_finalised=None, outbound_delay=None, outbound_signed=None):  # noqa: E501
        """TxStagesResponse - a model defined in Swagger"""  # noqa: E501
        self._inbound_observed = None
        self._inbound_confirmation_counted = None
        self._inbound_finalised = None
        self._swap_status = None
        self._swap_finalised = None
        self._outbound_delay = None
        self._outbound_signed = None
        self.discriminator = None
        self.inbound_observed = inbound_observed
        if inbound_confirmation_counted is not None:
            self.inbound_confirmation_counted = inbound_confirmation_counted
        if inbound_finalised is not None:
            self.inbound_finalised = inbound_finalised
        if swap_status is not None:
            self.swap_status = swap_status
        if swap_finalised is not None:
            self.swap_finalised = swap_finalised
        if outbound_delay is not None:
            self.outbound_delay = outbound_delay
        if outbound_signed is not None:
            self.outbound_signed = outbound_signed

    @property
    def inbound_observed(self):
        """Gets the inbound_observed of this TxStagesResponse.  # noqa: E501


        :return: The inbound_observed of this TxStagesResponse.  # noqa: E501
        :rtype: InboundObservedStage
        """
        return self._inbound_observed

    @inbound_observed.setter
    def inbound_observed(self, inbound_observed):
        """Sets the inbound_observed of this TxStagesResponse.


        :param inbound_observed: The inbound_observed of this TxStagesResponse.  # noqa: E501
        :type: InboundObservedStage
        """
        if inbound_observed is None:
            raise ValueError("Invalid value for `inbound_observed`, must not be `None`")  # noqa: E501

        self._inbound_observed = inbound_observed

    @property
    def inbound_confirmation_counted(self):
        """Gets the inbound_confirmation_counted of this TxStagesResponse.  # noqa: E501


        :return: The inbound_confirmation_counted of this TxStagesResponse.  # noqa: E501
        :rtype: InboundConfirmationCountedStage
        """
        return self._inbound_confirmation_counted

    @inbound_confirmation_counted.setter
    def inbound_confirmation_counted(self, inbound_confirmation_counted):
        """Sets the inbound_confirmation_counted of this TxStagesResponse.


        :param inbound_confirmation_counted: The inbound_confirmation_counted of this TxStagesResponse.  # noqa: E501
        :type: InboundConfirmationCountedStage
        """

        self._inbound_confirmation_counted = inbound_confirmation_counted

    @property
    def inbound_finalised(self):
        """Gets the inbound_finalised of this TxStagesResponse.  # noqa: E501


        :return: The inbound_finalised of this TxStagesResponse.  # noqa: E501
        :rtype: InboundFinalisedStage
        """
        return self._inbound_finalised

    @inbound_finalised.setter
    def inbound_finalised(self, inbound_finalised):
        """Sets the inbound_finalised of this TxStagesResponse.


        :param inbound_finalised: The inbound_finalised of this TxStagesResponse.  # noqa: E501
        :type: InboundFinalisedStage
        """

        self._inbound_finalised = inbound_finalised

    @property
    def swap_status(self):
        """Gets the swap_status of this TxStagesResponse.  # noqa: E501


        :return: The swap_status of this TxStagesResponse.  # noqa: E501
        :rtype: SwapStatus
        """
        return self._swap_status

    @swap_status.setter
    def swap_status(self, swap_status):
        """Sets the swap_status of this TxStagesResponse.


        :param swap_status: The swap_status of this TxStagesResponse.  # noqa: E501
        :type: SwapStatus
        """

        self._swap_status = swap_status

    @property
    def swap_finalised(self):
        """Gets the swap_finalised of this TxStagesResponse.  # noqa: E501


        :return: The swap_finalised of this TxStagesResponse.  # noqa: E501
        :rtype: SwapFinalisedStage
        """
        return self._swap_finalised

    @swap_finalised.setter
    def swap_finalised(self, swap_finalised):
        """Sets the swap_finalised of this TxStagesResponse.


        :param swap_finalised: The swap_finalised of this TxStagesResponse.  # noqa: E501
        :type: SwapFinalisedStage
        """

        self._swap_finalised = swap_finalised

    @property
    def outbound_delay(self):
        """Gets the outbound_delay of this TxStagesResponse.  # noqa: E501


        :return: The outbound_delay of this TxStagesResponse.  # noqa: E501
        :rtype: OutboundDelayStage
        """
        return self._outbound_delay

    @outbound_delay.setter
    def outbound_delay(self, outbound_delay):
        """Sets the outbound_delay of this TxStagesResponse.


        :param outbound_delay: The outbound_delay of this TxStagesResponse.  # noqa: E501
        :type: OutboundDelayStage
        """

        self._outbound_delay = outbound_delay

    @property
    def outbound_signed(self):
        """Gets the outbound_signed of this TxStagesResponse.  # noqa: E501


        :return: The outbound_signed of this TxStagesResponse.  # noqa: E501
        :rtype: OutboundSignedStage
        """
        return self._outbound_signed

    @outbound_signed.setter
    def outbound_signed(self, outbound_signed):
        """Sets the outbound_signed of this TxStagesResponse.


        :param outbound_signed: The outbound_signed of this TxStagesResponse.  # noqa: E501
        :type: OutboundSignedStage
        """

        self._outbound_signed = outbound_signed

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
        if issubclass(TxStagesResponse, dict):
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
        if not isinstance(other, TxStagesResponse):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other

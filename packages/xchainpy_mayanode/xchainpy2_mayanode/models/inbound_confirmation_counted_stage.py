# coding: utf-8

"""
    Mayanode API

    Mayanode REST API.  # noqa: E501

    OpenAPI spec version: 1.111.0
    Contact: devs@mayachain.org
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

import pprint
import re  # noqa: F401

import six

class InboundConfirmationCountedStage(object):
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
        'counting_start_height': 'int',
        'chain': 'str',
        'external_observed_height': 'int',
        'external_confirmation_delay_height': 'int',
        'remaining_confirmation_seconds': 'int',
        'completed': 'bool'
    }

    attribute_map = {
        'counting_start_height': 'counting_start_height',
        'chain': 'chain',
        'external_observed_height': 'external_observed_height',
        'external_confirmation_delay_height': 'external_confirmation_delay_height',
        'remaining_confirmation_seconds': 'remaining_confirmation_seconds',
        'completed': 'completed'
    }

    def __init__(self, counting_start_height=None, chain=None, external_observed_height=None, external_confirmation_delay_height=None, remaining_confirmation_seconds=None, completed=None):  # noqa: E501
        """InboundConfirmationCountedStage - a model defined in Swagger"""  # noqa: E501
        self._counting_start_height = None
        self._chain = None
        self._external_observed_height = None
        self._external_confirmation_delay_height = None
        self._remaining_confirmation_seconds = None
        self._completed = None
        self.discriminator = None
        if counting_start_height is not None:
            self.counting_start_height = counting_start_height
        if chain is not None:
            self.chain = chain
        if external_observed_height is not None:
            self.external_observed_height = external_observed_height
        if external_confirmation_delay_height is not None:
            self.external_confirmation_delay_height = external_confirmation_delay_height
        if remaining_confirmation_seconds is not None:
            self.remaining_confirmation_seconds = remaining_confirmation_seconds
        self.completed = completed

    @property
    def counting_start_height(self):
        """Gets the counting_start_height of this InboundConfirmationCountedStage.  # noqa: E501

        the MAYAChain block height when confirmation counting began  # noqa: E501

        :return: The counting_start_height of this InboundConfirmationCountedStage.  # noqa: E501
        :rtype: int
        """
        return self._counting_start_height

    @counting_start_height.setter
    def counting_start_height(self, counting_start_height):
        """Sets the counting_start_height of this InboundConfirmationCountedStage.

        the MAYAChain block height when confirmation counting began  # noqa: E501

        :param counting_start_height: The counting_start_height of this InboundConfirmationCountedStage.  # noqa: E501
        :type: int
        """

        self._counting_start_height = counting_start_height

    @property
    def chain(self):
        """Gets the chain of this InboundConfirmationCountedStage.  # noqa: E501

        the external source chain for which confirmation counting takes place  # noqa: E501

        :return: The chain of this InboundConfirmationCountedStage.  # noqa: E501
        :rtype: str
        """
        return self._chain

    @chain.setter
    def chain(self, chain):
        """Sets the chain of this InboundConfirmationCountedStage.

        the external source chain for which confirmation counting takes place  # noqa: E501

        :param chain: The chain of this InboundConfirmationCountedStage.  # noqa: E501
        :type: str
        """

        self._chain = chain

    @property
    def external_observed_height(self):
        """Gets the external_observed_height of this InboundConfirmationCountedStage.  # noqa: E501

        the block height on the external source chain when the transaction was observed  # noqa: E501

        :return: The external_observed_height of this InboundConfirmationCountedStage.  # noqa: E501
        :rtype: int
        """
        return self._external_observed_height

    @external_observed_height.setter
    def external_observed_height(self, external_observed_height):
        """Sets the external_observed_height of this InboundConfirmationCountedStage.

        the block height on the external source chain when the transaction was observed  # noqa: E501

        :param external_observed_height: The external_observed_height of this InboundConfirmationCountedStage.  # noqa: E501
        :type: int
        """

        self._external_observed_height = external_observed_height

    @property
    def external_confirmation_delay_height(self):
        """Gets the external_confirmation_delay_height of this InboundConfirmationCountedStage.  # noqa: E501

        the block height on the external source chain when confirmation counting will be complete  # noqa: E501

        :return: The external_confirmation_delay_height of this InboundConfirmationCountedStage.  # noqa: E501
        :rtype: int
        """
        return self._external_confirmation_delay_height

    @external_confirmation_delay_height.setter
    def external_confirmation_delay_height(self, external_confirmation_delay_height):
        """Sets the external_confirmation_delay_height of this InboundConfirmationCountedStage.

        the block height on the external source chain when confirmation counting will be complete  # noqa: E501

        :param external_confirmation_delay_height: The external_confirmation_delay_height of this InboundConfirmationCountedStage.  # noqa: E501
        :type: int
        """

        self._external_confirmation_delay_height = external_confirmation_delay_height

    @property
    def remaining_confirmation_seconds(self):
        """Gets the remaining_confirmation_seconds of this InboundConfirmationCountedStage.  # noqa: E501

        the estimated remaining seconds before confirmation counting completes  # noqa: E501

        :return: The remaining_confirmation_seconds of this InboundConfirmationCountedStage.  # noqa: E501
        :rtype: int
        """
        return self._remaining_confirmation_seconds

    @remaining_confirmation_seconds.setter
    def remaining_confirmation_seconds(self, remaining_confirmation_seconds):
        """Sets the remaining_confirmation_seconds of this InboundConfirmationCountedStage.

        the estimated remaining seconds before confirmation counting completes  # noqa: E501

        :param remaining_confirmation_seconds: The remaining_confirmation_seconds of this InboundConfirmationCountedStage.  # noqa: E501
        :type: int
        """

        self._remaining_confirmation_seconds = remaining_confirmation_seconds

    @property
    def completed(self):
        """Gets the completed of this InboundConfirmationCountedStage.  # noqa: E501

        returns true if no transaction confirmation counting remains to be done  # noqa: E501

        :return: The completed of this InboundConfirmationCountedStage.  # noqa: E501
        :rtype: bool
        """
        return self._completed

    @completed.setter
    def completed(self, completed):
        """Sets the completed of this InboundConfirmationCountedStage.

        returns true if no transaction confirmation counting remains to be done  # noqa: E501

        :param completed: The completed of this InboundConfirmationCountedStage.  # noqa: E501
        :type: bool
        """
        if completed is None:
            raise ValueError("Invalid value for `completed`, must not be `None`")  # noqa: E501

        self._completed = completed

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
        if issubclass(InboundConfirmationCountedStage, dict):
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
        if not isinstance(other, InboundConfirmationCountedStage):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other

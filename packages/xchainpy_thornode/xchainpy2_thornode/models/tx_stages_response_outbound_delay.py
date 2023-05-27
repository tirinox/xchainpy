# coding: utf-8

"""
    Thornode API

    Thornode REST API.  # noqa: E501

    OpenAPI spec version: 1.110.0
    Contact: devs@thorchain.org
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

import pprint
import re  # noqa: F401

import six

class TxStagesResponseOutboundDelay(object):
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
        'remaining_delay_blocks': 'int',
        'remaining_delay_seconds': 'int',
        'completed': 'bool'
    }

    attribute_map = {
        'remaining_delay_blocks': 'remaining_delay_blocks',
        'remaining_delay_seconds': 'remaining_delay_seconds',
        'completed': 'completed'
    }

    def __init__(self, remaining_delay_blocks=None, remaining_delay_seconds=None, completed=None):  # noqa: E501
        """TxStagesResponseOutboundDelay - a model defined in Swagger"""  # noqa: E501
        self._remaining_delay_blocks = None
        self._remaining_delay_seconds = None
        self._completed = None
        self.discriminator = None
        if remaining_delay_blocks is not None:
            self.remaining_delay_blocks = remaining_delay_blocks
        if remaining_delay_seconds is not None:
            self.remaining_delay_seconds = remaining_delay_seconds
        self.completed = completed

    @property
    def remaining_delay_blocks(self):
        """Gets the remaining_delay_blocks of this TxStagesResponseOutboundDelay.  # noqa: E501

        the number of remaining THORChain blocks the outbound will be delayed  # noqa: E501

        :return: The remaining_delay_blocks of this TxStagesResponseOutboundDelay.  # noqa: E501
        :rtype: int
        """
        return self._remaining_delay_blocks

    @remaining_delay_blocks.setter
    def remaining_delay_blocks(self, remaining_delay_blocks):
        """Sets the remaining_delay_blocks of this TxStagesResponseOutboundDelay.

        the number of remaining THORChain blocks the outbound will be delayed  # noqa: E501

        :param remaining_delay_blocks: The remaining_delay_blocks of this TxStagesResponseOutboundDelay.  # noqa: E501
        :type: int
        """

        self._remaining_delay_blocks = remaining_delay_blocks

    @property
    def remaining_delay_seconds(self):
        """Gets the remaining_delay_seconds of this TxStagesResponseOutboundDelay.  # noqa: E501

        the estimated remaining seconds of the outbound delay before it will be sent  # noqa: E501

        :return: The remaining_delay_seconds of this TxStagesResponseOutboundDelay.  # noqa: E501
        :rtype: int
        """
        return self._remaining_delay_seconds

    @remaining_delay_seconds.setter
    def remaining_delay_seconds(self, remaining_delay_seconds):
        """Sets the remaining_delay_seconds of this TxStagesResponseOutboundDelay.

        the estimated remaining seconds of the outbound delay before it will be sent  # noqa: E501

        :param remaining_delay_seconds: The remaining_delay_seconds of this TxStagesResponseOutboundDelay.  # noqa: E501
        :type: int
        """

        self._remaining_delay_seconds = remaining_delay_seconds

    @property
    def completed(self):
        """Gets the completed of this TxStagesResponseOutboundDelay.  # noqa: E501

        returns true if no transaction outbound delay remains  # noqa: E501

        :return: The completed of this TxStagesResponseOutboundDelay.  # noqa: E501
        :rtype: bool
        """
        return self._completed

    @completed.setter
    def completed(self, completed):
        """Sets the completed of this TxStagesResponseOutboundDelay.

        returns true if no transaction outbound delay remains  # noqa: E501

        :param completed: The completed of this TxStagesResponseOutboundDelay.  # noqa: E501
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
        if issubclass(TxStagesResponseOutboundDelay, dict):
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
        if not isinstance(other, TxStagesResponseOutboundDelay):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other

# coding: utf-8

"""
    Thornode API

    Thornode REST API.  # noqa: E501

    OpenAPI spec version: 1.121.0
    Contact: devs@thorchain.org
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

import pprint
import re  # noqa: F401

import six

class TxStagesResponseOutboundSigned(object):
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
        'scheduled_outbound_height': 'int',
        'blocks_since_scheduled': 'int',
        'completed': 'bool'
    }

    attribute_map = {
        'scheduled_outbound_height': 'scheduled_outbound_height',
        'blocks_since_scheduled': 'blocks_since_scheduled',
        'completed': 'completed'
    }

    def __init__(self, scheduled_outbound_height=None, blocks_since_scheduled=None, completed=None):  # noqa: E501
        """TxStagesResponseOutboundSigned - a model defined in Swagger"""  # noqa: E501
        self._scheduled_outbound_height = None
        self._blocks_since_scheduled = None
        self._completed = None
        self.discriminator = None
        if scheduled_outbound_height is not None:
            self.scheduled_outbound_height = scheduled_outbound_height
        if blocks_since_scheduled is not None:
            self.blocks_since_scheduled = blocks_since_scheduled
        self.completed = completed

    @property
    def scheduled_outbound_height(self):
        """Gets the scheduled_outbound_height of this TxStagesResponseOutboundSigned.  # noqa: E501

        THORChain height for which the external outbound is scheduled  # noqa: E501

        :return: The scheduled_outbound_height of this TxStagesResponseOutboundSigned.  # noqa: E501
        :rtype: int
        """
        return self._scheduled_outbound_height

    @scheduled_outbound_height.setter
    def scheduled_outbound_height(self, scheduled_outbound_height):
        """Sets the scheduled_outbound_height of this TxStagesResponseOutboundSigned.

        THORChain height for which the external outbound is scheduled  # noqa: E501

        :param scheduled_outbound_height: The scheduled_outbound_height of this TxStagesResponseOutboundSigned.  # noqa: E501
        :type: int
        """

        self._scheduled_outbound_height = scheduled_outbound_height

    @property
    def blocks_since_scheduled(self):
        """Gets the blocks_since_scheduled of this TxStagesResponseOutboundSigned.  # noqa: E501

        THORChain blocks since the scheduled outbound height  # noqa: E501

        :return: The blocks_since_scheduled of this TxStagesResponseOutboundSigned.  # noqa: E501
        :rtype: int
        """
        return self._blocks_since_scheduled

    @blocks_since_scheduled.setter
    def blocks_since_scheduled(self, blocks_since_scheduled):
        """Sets the blocks_since_scheduled of this TxStagesResponseOutboundSigned.

        THORChain blocks since the scheduled outbound height  # noqa: E501

        :param blocks_since_scheduled: The blocks_since_scheduled of this TxStagesResponseOutboundSigned.  # noqa: E501
        :type: int
        """

        self._blocks_since_scheduled = blocks_since_scheduled

    @property
    def completed(self):
        """Gets the completed of this TxStagesResponseOutboundSigned.  # noqa: E501

        returns true if an external transaction has been signed and broadcast (and observed in its mempool)  # noqa: E501

        :return: The completed of this TxStagesResponseOutboundSigned.  # noqa: E501
        :rtype: bool
        """
        return self._completed

    @completed.setter
    def completed(self, completed):
        """Sets the completed of this TxStagesResponseOutboundSigned.

        returns true if an external transaction has been signed and broadcast (and observed in its mempool)  # noqa: E501

        :param completed: The completed of this TxStagesResponseOutboundSigned.  # noqa: E501
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
        if issubclass(TxStagesResponseOutboundSigned, dict):
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
        if not isinstance(other, TxStagesResponseOutboundSigned):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other

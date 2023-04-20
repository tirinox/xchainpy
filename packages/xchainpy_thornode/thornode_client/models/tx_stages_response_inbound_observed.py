# coding: utf-8

"""
    Thornode API

    Thornode REST API.  # noqa: E501

    OpenAPI spec version: 1.108.3
    Contact: devs@thorchain.org
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

import pprint
import re  # noqa: F401

import six

class TxStagesResponseInboundObserved(object):
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
        'started': 'bool',
        'completed': 'bool'
    }

    attribute_map = {
        'started': 'started',
        'completed': 'completed'
    }

    def __init__(self, started=None, completed=None):  # noqa: E501
        """TxStagesResponseInboundObserved - a model defined in Swagger"""  # noqa: E501
        self._started = None
        self._completed = None
        self.discriminator = None
        if started is not None:
            self.started = started
        self.completed = completed

    @property
    def started(self):
        """Gets the started of this TxStagesResponseInboundObserved.  # noqa: E501

        returns true if any nodes have observed the transaction  # noqa: E501

        :return: The started of this TxStagesResponseInboundObserved.  # noqa: E501
        :rtype: bool
        """
        return self._started

    @started.setter
    def started(self, started):
        """Sets the started of this TxStagesResponseInboundObserved.

        returns true if any nodes have observed the transaction  # noqa: E501

        :param started: The started of this TxStagesResponseInboundObserved.  # noqa: E501
        :type: bool
        """

        self._started = started

    @property
    def completed(self):
        """Gets the completed of this TxStagesResponseInboundObserved.  # noqa: E501

        returns true if no transaction observation remains to be done  # noqa: E501

        :return: The completed of this TxStagesResponseInboundObserved.  # noqa: E501
        :rtype: bool
        """
        return self._completed

    @completed.setter
    def completed(self, completed):
        """Sets the completed of this TxStagesResponseInboundObserved.

        returns true if no transaction observation remains to be done  # noqa: E501

        :param completed: The completed of this TxStagesResponseInboundObserved.  # noqa: E501
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
        if issubclass(TxStagesResponseInboundObserved, dict):
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
        if not isinstance(other, TxStagesResponseInboundObserved):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other

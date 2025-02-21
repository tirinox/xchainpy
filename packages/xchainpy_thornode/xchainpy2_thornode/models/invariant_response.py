# coding: utf-8

"""
    Thornode API

    Thornode REST API.  # noqa: E501

    OpenAPI spec version: 3.0.0
    Contact: devs@thorchain.org
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

import pprint
import re  # noqa: F401

import six

class InvariantResponse(object):
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
        'invariant': 'str',
        'broken': 'bool',
        'msg': 'list[str]'
    }

    attribute_map = {
        'invariant': 'invariant',
        'broken': 'broken',
        'msg': 'msg'
    }

    def __init__(self, invariant=None, broken=None, msg=None):  # noqa: E501
        """InvariantResponse - a model defined in Swagger"""  # noqa: E501
        self._invariant = None
        self._broken = None
        self._msg = None
        self.discriminator = None
        self.invariant = invariant
        self.broken = broken
        self.msg = msg

    @property
    def invariant(self):
        """Gets the invariant of this InvariantResponse.  # noqa: E501

        The name of the invariant.  # noqa: E501

        :return: The invariant of this InvariantResponse.  # noqa: E501
        :rtype: str
        """
        return self._invariant

    @invariant.setter
    def invariant(self, invariant):
        """Sets the invariant of this InvariantResponse.

        The name of the invariant.  # noqa: E501

        :param invariant: The invariant of this InvariantResponse.  # noqa: E501
        :type: str
        """
        if invariant is None:
            raise ValueError("Invalid value for `invariant`, must not be `None`")  # noqa: E501

        self._invariant = invariant

    @property
    def broken(self):
        """Gets the broken of this InvariantResponse.  # noqa: E501

        Returns true if the invariant is broken.  # noqa: E501

        :return: The broken of this InvariantResponse.  # noqa: E501
        :rtype: bool
        """
        return self._broken

    @broken.setter
    def broken(self, broken):
        """Sets the broken of this InvariantResponse.

        Returns true if the invariant is broken.  # noqa: E501

        :param broken: The broken of this InvariantResponse.  # noqa: E501
        :type: bool
        """
        if broken is None:
            raise ValueError("Invalid value for `broken`, must not be `None`")  # noqa: E501

        self._broken = broken

    @property
    def msg(self):
        """Gets the msg of this InvariantResponse.  # noqa: E501

        Informative message about the invariant result.  # noqa: E501

        :return: The msg of this InvariantResponse.  # noqa: E501
        :rtype: list[str]
        """
        return self._msg

    @msg.setter
    def msg(self, msg):
        """Sets the msg of this InvariantResponse.

        Informative message about the invariant result.  # noqa: E501

        :param msg: The msg of this InvariantResponse.  # noqa: E501
        :type: list[str]
        """
        if msg is None:
            raise ValueError("Invalid value for `msg`, must not be `None`")  # noqa: E501

        self._msg = msg

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
        if issubclass(InvariantResponse, dict):
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
        if not isinstance(other, InvariantResponse):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other

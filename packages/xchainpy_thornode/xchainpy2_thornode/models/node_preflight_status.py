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

class NodePreflightStatus(object):
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
        'status': 'str',
        'reason': 'str',
        'code': 'int'
    }

    attribute_map = {
        'status': 'status',
        'reason': 'reason',
        'code': 'code'
    }

    def __init__(self, status=None, reason=None, code=None):  # noqa: E501
        """NodePreflightStatus - a model defined in Swagger"""  # noqa: E501
        self._status = None
        self._reason = None
        self._code = None
        self.discriminator = None
        self.status = status
        self.reason = reason
        self.code = code

    @property
    def status(self):
        """Gets the status of this NodePreflightStatus.  # noqa: E501

        the next status of the node  # noqa: E501

        :return: The status of this NodePreflightStatus.  # noqa: E501
        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, status):
        """Sets the status of this NodePreflightStatus.

        the next status of the node  # noqa: E501

        :param status: The status of this NodePreflightStatus.  # noqa: E501
        :type: str
        """
        if status is None:
            raise ValueError("Invalid value for `status`, must not be `None`")  # noqa: E501

        self._status = status

    @property
    def reason(self):
        """Gets the reason of this NodePreflightStatus.  # noqa: E501

        the reason for the transition to the next status  # noqa: E501

        :return: The reason of this NodePreflightStatus.  # noqa: E501
        :rtype: str
        """
        return self._reason

    @reason.setter
    def reason(self, reason):
        """Sets the reason of this NodePreflightStatus.

        the reason for the transition to the next status  # noqa: E501

        :param reason: The reason of this NodePreflightStatus.  # noqa: E501
        :type: str
        """
        if reason is None:
            raise ValueError("Invalid value for `reason`, must not be `None`")  # noqa: E501

        self._reason = reason

    @property
    def code(self):
        """Gets the code of this NodePreflightStatus.  # noqa: E501


        :return: The code of this NodePreflightStatus.  # noqa: E501
        :rtype: int
        """
        return self._code

    @code.setter
    def code(self, code):
        """Sets the code of this NodePreflightStatus.


        :param code: The code of this NodePreflightStatus.  # noqa: E501
        :type: int
        """
        if code is None:
            raise ValueError("Invalid value for `code`, must not be `None`")  # noqa: E501

        self._code = code

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
        if issubclass(NodePreflightStatus, dict):
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
        if not isinstance(other, NodePreflightStatus):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other

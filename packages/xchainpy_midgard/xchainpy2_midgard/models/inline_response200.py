# coding: utf-8

"""
    Midgard Public API

    The Midgard Public API queries THORChain and any chains linked via the Bifröst and prepares information about the network to be readily available for public users. The API parses transaction event data from THORChain and stores them in a time-series database to make time-dependent queries easy. Midgard does not hold critical information. To interact with THORChain protocol, users should query THORNode directly.  # noqa: E501

    OpenAPI spec version: 2.22.4
    Contact: devs@thorchain.org
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

import pprint
import re  # noqa: F401

import six

class InlineResponse200(object):
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
        'actions': 'list[Action]',
        'count': 'str',
        'meta': 'ActionMeta'
    }

    attribute_map = {
        'actions': 'actions',
        'count': 'count',
        'meta': 'meta'
    }

    def __init__(self, actions=None, count=None, meta=None):  # noqa: E501
        """InlineResponse200 - a model defined in Swagger"""  # noqa: E501
        self._actions = None
        self._count = None
        self._meta = None
        self.discriminator = None
        self.actions = actions
        if count is not None:
            self.count = count
        self.meta = meta

    @property
    def actions(self):
        """Gets the actions of this InlineResponse200.  # noqa: E501


        :return: The actions of this InlineResponse200.  # noqa: E501
        :rtype: list[Action]
        """
        return self._actions

    @actions.setter
    def actions(self, actions):
        """Sets the actions of this InlineResponse200.


        :param actions: The actions of this InlineResponse200.  # noqa: E501
        :type: list[Action]
        """
        if actions is None:
            raise ValueError("Invalid value for `actions`, must not be `None`")  # noqa: E501

        self._actions = actions

    @property
    def count(self):
        """Gets the count of this InlineResponse200.  # noqa: E501

        Int64, number of results matching the given filters. It may be -1 if Midgard is having trouble counting the results and has to cancel the count query (temporary fix). Also, if new action parameters is used it won't be returned.   # noqa: E501

        :return: The count of this InlineResponse200.  # noqa: E501
        :rtype: str
        """
        return self._count

    @count.setter
    def count(self, count):
        """Sets the count of this InlineResponse200.

        Int64, number of results matching the given filters. It may be -1 if Midgard is having trouble counting the results and has to cancel the count query (temporary fix). Also, if new action parameters is used it won't be returned.   # noqa: E501

        :param count: The count of this InlineResponse200.  # noqa: E501
        :type: str
        """

        self._count = count

    @property
    def meta(self):
        """Gets the meta of this InlineResponse200.  # noqa: E501


        :return: The meta of this InlineResponse200.  # noqa: E501
        :rtype: ActionMeta
        """
        return self._meta

    @meta.setter
    def meta(self, meta):
        """Sets the meta of this InlineResponse200.


        :param meta: The meta of this InlineResponse200.  # noqa: E501
        :type: ActionMeta
        """
        if meta is None:
            raise ValueError("Invalid value for `meta`, must not be `None`")  # noqa: E501

        self._meta = meta

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
        if issubclass(InlineResponse200, dict):
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
        if not isinstance(other, InlineResponse200):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other

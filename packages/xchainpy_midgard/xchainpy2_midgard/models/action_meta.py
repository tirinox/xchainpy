# coding: utf-8

"""
    Midgard Public API

    The Midgard Public API queries THORChain and any chains linked via the Bifröst and prepares information about the network to be readily available for public users. The API parses transaction event data from THORChain and stores them in a time-series database to make time-dependent queries easy. Midgard does not hold critical information. To interact with THORChain protocol, users should query THORNode directly.  # noqa: E501

    OpenAPI spec version: 2.18.2
    Contact: devs@thorchain.org
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

import pprint
import re  # noqa: F401

import six

class ActionMeta(object):
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
        'next_page_token': 'str',
        'prev_page_token': 'str'
    }

    attribute_map = {
        'next_page_token': 'nextPageToken',
        'prev_page_token': 'prevPageToken'
    }

    def __init__(self, next_page_token=None, prev_page_token=None):  # noqa: E501
        """ActionMeta - a model defined in Swagger"""  # noqa: E501
        self._next_page_token = None
        self._prev_page_token = None
        self.discriminator = None
        self.next_page_token = next_page_token
        self.prev_page_token = prev_page_token

    @property
    def next_page_token(self):
        """Gets the next_page_token of this ActionMeta.  # noqa: E501

        Int64, The last action event_id that can be used for pagination.  This token is needed to be given for next page.   # noqa: E501

        :return: The next_page_token of this ActionMeta.  # noqa: E501
        :rtype: str
        """
        return self._next_page_token

    @next_page_token.setter
    def next_page_token(self, next_page_token):
        """Sets the next_page_token of this ActionMeta.

        Int64, The last action event_id that can be used for pagination.  This token is needed to be given for next page.   # noqa: E501

        :param next_page_token: The next_page_token of this ActionMeta.  # noqa: E501
        :type: str
        """
        if next_page_token is None:
            raise ValueError("Invalid value for `next_page_token`, must not be `None`")  # noqa: E501

        self._next_page_token = next_page_token

    @property
    def prev_page_token(self):
        """Gets the prev_page_token of this ActionMeta.  # noqa: E501

        Int64, The first action event_id that can be used for previous pagination. This token is needed to be given for previous page.   # noqa: E501

        :return: The prev_page_token of this ActionMeta.  # noqa: E501
        :rtype: str
        """
        return self._prev_page_token

    @prev_page_token.setter
    def prev_page_token(self, prev_page_token):
        """Sets the prev_page_token of this ActionMeta.

        Int64, The first action event_id that can be used for previous pagination. This token is needed to be given for previous page.   # noqa: E501

        :param prev_page_token: The prev_page_token of this ActionMeta.  # noqa: E501
        :type: str
        """
        if prev_page_token is None:
            raise ValueError("Invalid value for `prev_page_token`, must not be `None`")  # noqa: E501

        self._prev_page_token = prev_page_token

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
        if issubclass(ActionMeta, dict):
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
        if not isinstance(other, ActionMeta):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other

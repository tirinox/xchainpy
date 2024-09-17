# coding: utf-8

"""
    Thornode API

    Thornode REST API.  # noqa: E501

    OpenAPI spec version: 2.135.0
    Contact: devs@thorchain.org
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

import pprint
import re  # noqa: F401

import six

class BlockResponseHeaderVersion(object):
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
        'block': 'str',
        'app': 'str'
    }

    attribute_map = {
        'block': 'block',
        'app': 'app'
    }

    def __init__(self, block=None, app=None):  # noqa: E501
        """BlockResponseHeaderVersion - a model defined in Swagger"""  # noqa: E501
        self._block = None
        self._app = None
        self.discriminator = None
        self.block = block
        self.app = app

    @property
    def block(self):
        """Gets the block of this BlockResponseHeaderVersion.  # noqa: E501


        :return: The block of this BlockResponseHeaderVersion.  # noqa: E501
        :rtype: str
        """
        return self._block

    @block.setter
    def block(self, block):
        """Sets the block of this BlockResponseHeaderVersion.


        :param block: The block of this BlockResponseHeaderVersion.  # noqa: E501
        :type: str
        """
        if block is None:
            raise ValueError("Invalid value for `block`, must not be `None`")  # noqa: E501

        self._block = block

    @property
    def app(self):
        """Gets the app of this BlockResponseHeaderVersion.  # noqa: E501


        :return: The app of this BlockResponseHeaderVersion.  # noqa: E501
        :rtype: str
        """
        return self._app

    @app.setter
    def app(self, app):
        """Sets the app of this BlockResponseHeaderVersion.


        :param app: The app of this BlockResponseHeaderVersion.  # noqa: E501
        :type: str
        """
        if app is None:
            raise ValueError("Invalid value for `app`, must not be `None`")  # noqa: E501

        self._app = app

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
        if issubclass(BlockResponseHeaderVersion, dict):
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
        if not isinstance(other, BlockResponseHeaderVersion):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other

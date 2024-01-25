# coding: utf-8

"""
    Thornode API

    Thornode REST API.  # noqa: E501

    OpenAPI spec version: 1.127.0
    Contact: devs@thorchain.org
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

import pprint
import re  # noqa: F401

import six

class MimirV2IDsResponse(object):
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
        'id': 'ModelInt',
        'name': 'str',
        'legacy_key': 'str',
        'vote_key': 'str',
        'votes': 'object'
    }

    attribute_map = {
        'id': 'id',
        'name': 'name',
        'legacy_key': 'legacy_key',
        'vote_key': 'vote_key',
        'votes': 'votes'
    }

    def __init__(self, id=None, name=None, legacy_key=None, vote_key=None, votes=None):  # noqa: E501
        """MimirV2IDsResponse - a model defined in Swagger"""  # noqa: E501
        self._id = None
        self._name = None
        self._legacy_key = None
        self._vote_key = None
        self._votes = None
        self.discriminator = None
        if id is not None:
            self.id = id
        if name is not None:
            self.name = name
        if legacy_key is not None:
            self.legacy_key = legacy_key
        if vote_key is not None:
            self.vote_key = vote_key
        if votes is not None:
            self.votes = votes

    @property
    def id(self):
        """Gets the id of this MimirV2IDsResponse.  # noqa: E501


        :return: The id of this MimirV2IDsResponse.  # noqa: E501
        :rtype: ModelInt
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this MimirV2IDsResponse.


        :param id: The id of this MimirV2IDsResponse.  # noqa: E501
        :type: ModelInt
        """

        self._id = id

    @property
    def name(self):
        """Gets the name of this MimirV2IDsResponse.  # noqa: E501


        :return: The name of this MimirV2IDsResponse.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this MimirV2IDsResponse.


        :param name: The name of this MimirV2IDsResponse.  # noqa: E501
        :type: str
        """

        self._name = name

    @property
    def legacy_key(self):
        """Gets the legacy_key of this MimirV2IDsResponse.  # noqa: E501


        :return: The legacy_key of this MimirV2IDsResponse.  # noqa: E501
        :rtype: str
        """
        return self._legacy_key

    @legacy_key.setter
    def legacy_key(self, legacy_key):
        """Sets the legacy_key of this MimirV2IDsResponse.


        :param legacy_key: The legacy_key of this MimirV2IDsResponse.  # noqa: E501
        :type: str
        """

        self._legacy_key = legacy_key

    @property
    def vote_key(self):
        """Gets the vote_key of this MimirV2IDsResponse.  # noqa: E501


        :return: The vote_key of this MimirV2IDsResponse.  # noqa: E501
        :rtype: str
        """
        return self._vote_key

    @vote_key.setter
    def vote_key(self, vote_key):
        """Sets the vote_key of this MimirV2IDsResponse.


        :param vote_key: The vote_key of this MimirV2IDsResponse.  # noqa: E501
        :type: str
        """

        self._vote_key = vote_key

    @property
    def votes(self):
        """Gets the votes of this MimirV2IDsResponse.  # noqa: E501


        :return: The votes of this MimirV2IDsResponse.  # noqa: E501
        :rtype: object
        """
        return self._votes

    @votes.setter
    def votes(self, votes):
        """Sets the votes of this MimirV2IDsResponse.


        :param votes: The votes of this MimirV2IDsResponse.  # noqa: E501
        :type: object
        """

        self._votes = votes

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
        if issubclass(MimirV2IDsResponse, dict):
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
        if not isinstance(other, MimirV2IDsResponse):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other

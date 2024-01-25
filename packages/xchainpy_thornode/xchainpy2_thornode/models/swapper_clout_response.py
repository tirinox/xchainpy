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

class SwapperCloutResponse(object):
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
        'address': 'str',
        'score': 'str',
        'reclaimed': 'str',
        'spent': 'str',
        'last_spent_height': 'int',
        'last_reclaim_height': 'int'
    }

    attribute_map = {
        'address': 'address',
        'score': 'score',
        'reclaimed': 'reclaimed',
        'spent': 'spent',
        'last_spent_height': 'last_spent_height',
        'last_reclaim_height': 'last_reclaim_height'
    }

    def __init__(self, address=None, score=None, reclaimed=None, spent=None, last_spent_height=None, last_reclaim_height=None):  # noqa: E501
        """SwapperCloutResponse - a model defined in Swagger"""  # noqa: E501
        self._address = None
        self._score = None
        self._reclaimed = None
        self._spent = None
        self._last_spent_height = None
        self._last_reclaim_height = None
        self.discriminator = None
        self.address = address
        if score is not None:
            self.score = score
        if reclaimed is not None:
            self.reclaimed = reclaimed
        if spent is not None:
            self.spent = spent
        if last_spent_height is not None:
            self.last_spent_height = last_spent_height
        if last_reclaim_height is not None:
            self.last_reclaim_height = last_reclaim_height

    @property
    def address(self):
        """Gets the address of this SwapperCloutResponse.  # noqa: E501

        address associated with this clout account  # noqa: E501

        :return: The address of this SwapperCloutResponse.  # noqa: E501
        :rtype: str
        """
        return self._address

    @address.setter
    def address(self, address):
        """Sets the address of this SwapperCloutResponse.

        address associated with this clout account  # noqa: E501

        :param address: The address of this SwapperCloutResponse.  # noqa: E501
        :type: str
        """
        if address is None:
            raise ValueError("Invalid value for `address`, must not be `None`")  # noqa: E501

        self._address = address

    @property
    def score(self):
        """Gets the score of this SwapperCloutResponse.  # noqa: E501

        clout score, which is the amount of rune spent on swap fees  # noqa: E501

        :return: The score of this SwapperCloutResponse.  # noqa: E501
        :rtype: str
        """
        return self._score

    @score.setter
    def score(self, score):
        """Sets the score of this SwapperCloutResponse.

        clout score, which is the amount of rune spent on swap fees  # noqa: E501

        :param score: The score of this SwapperCloutResponse.  # noqa: E501
        :type: str
        """

        self._score = score

    @property
    def reclaimed(self):
        """Gets the reclaimed of this SwapperCloutResponse.  # noqa: E501

        amount of clout that has been reclaimed in total over time (observed clout spent)  # noqa: E501

        :return: The reclaimed of this SwapperCloutResponse.  # noqa: E501
        :rtype: str
        """
        return self._reclaimed

    @reclaimed.setter
    def reclaimed(self, reclaimed):
        """Sets the reclaimed of this SwapperCloutResponse.

        amount of clout that has been reclaimed in total over time (observed clout spent)  # noqa: E501

        :param reclaimed: The reclaimed of this SwapperCloutResponse.  # noqa: E501
        :type: str
        """

        self._reclaimed = reclaimed

    @property
    def spent(self):
        """Gets the spent of this SwapperCloutResponse.  # noqa: E501

        amount of clout that has been spent in total over time  # noqa: E501

        :return: The spent of this SwapperCloutResponse.  # noqa: E501
        :rtype: str
        """
        return self._spent

    @spent.setter
    def spent(self, spent):
        """Sets the spent of this SwapperCloutResponse.

        amount of clout that has been spent in total over time  # noqa: E501

        :param spent: The spent of this SwapperCloutResponse.  # noqa: E501
        :type: str
        """

        self._spent = spent

    @property
    def last_spent_height(self):
        """Gets the last_spent_height of this SwapperCloutResponse.  # noqa: E501

        last block height that clout was spent  # noqa: E501

        :return: The last_spent_height of this SwapperCloutResponse.  # noqa: E501
        :rtype: int
        """
        return self._last_spent_height

    @last_spent_height.setter
    def last_spent_height(self, last_spent_height):
        """Sets the last_spent_height of this SwapperCloutResponse.

        last block height that clout was spent  # noqa: E501

        :param last_spent_height: The last_spent_height of this SwapperCloutResponse.  # noqa: E501
        :type: int
        """

        self._last_spent_height = last_spent_height

    @property
    def last_reclaim_height(self):
        """Gets the last_reclaim_height of this SwapperCloutResponse.  # noqa: E501

        last block height that clout was reclaimed  # noqa: E501

        :return: The last_reclaim_height of this SwapperCloutResponse.  # noqa: E501
        :rtype: int
        """
        return self._last_reclaim_height

    @last_reclaim_height.setter
    def last_reclaim_height(self, last_reclaim_height):
        """Sets the last_reclaim_height of this SwapperCloutResponse.

        last block height that clout was reclaimed  # noqa: E501

        :param last_reclaim_height: The last_reclaim_height of this SwapperCloutResponse.  # noqa: E501
        :type: int
        """

        self._last_reclaim_height = last_reclaim_height

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
        if issubclass(SwapperCloutResponse, dict):
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
        if not isinstance(other, SwapperCloutResponse):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other

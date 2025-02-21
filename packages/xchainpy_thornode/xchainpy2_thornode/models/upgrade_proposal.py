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

class UpgradeProposal(object):
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
        'name': 'str',
        'height': 'int',
        'info': 'str',
        'approved': 'bool',
        'approved_percent': 'str',
        'validators_to_quorum': 'int'
    }

    attribute_map = {
        'name': 'name',
        'height': 'height',
        'info': 'info',
        'approved': 'approved',
        'approved_percent': 'approved_percent',
        'validators_to_quorum': 'validators_to_quorum'
    }

    def __init__(self, name=None, height=None, info=None, approved=None, approved_percent=None, validators_to_quorum=None):  # noqa: E501
        """UpgradeProposal - a model defined in Swagger"""  # noqa: E501
        self._name = None
        self._height = None
        self._info = None
        self._approved = None
        self._approved_percent = None
        self._validators_to_quorum = None
        self.discriminator = None
        self.name = name
        self.height = height
        self.info = info
        if approved is not None:
            self.approved = approved
        if approved_percent is not None:
            self.approved_percent = approved_percent
        if validators_to_quorum is not None:
            self.validators_to_quorum = validators_to_quorum

    @property
    def name(self):
        """Gets the name of this UpgradeProposal.  # noqa: E501

        the name of the upgrade  # noqa: E501

        :return: The name of this UpgradeProposal.  # noqa: E501
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """Sets the name of this UpgradeProposal.

        the name of the upgrade  # noqa: E501

        :param name: The name of this UpgradeProposal.  # noqa: E501
        :type: str
        """
        if name is None:
            raise ValueError("Invalid value for `name`, must not be `None`")  # noqa: E501

        self._name = name

    @property
    def height(self):
        """Gets the height of this UpgradeProposal.  # noqa: E501

        the block height at which the upgrade will occur  # noqa: E501

        :return: The height of this UpgradeProposal.  # noqa: E501
        :rtype: int
        """
        return self._height

    @height.setter
    def height(self, height):
        """Sets the height of this UpgradeProposal.

        the block height at which the upgrade will occur  # noqa: E501

        :param height: The height of this UpgradeProposal.  # noqa: E501
        :type: int
        """
        if height is None:
            raise ValueError("Invalid value for `height`, must not be `None`")  # noqa: E501

        self._height = height

    @property
    def info(self):
        """Gets the info of this UpgradeProposal.  # noqa: E501

        the description of the upgrade, typically json with URLs to binaries for use with automation tools  # noqa: E501

        :return: The info of this UpgradeProposal.  # noqa: E501
        :rtype: str
        """
        return self._info

    @info.setter
    def info(self, info):
        """Sets the info of this UpgradeProposal.

        the description of the upgrade, typically json with URLs to binaries for use with automation tools  # noqa: E501

        :param info: The info of this UpgradeProposal.  # noqa: E501
        :type: str
        """
        if info is None:
            raise ValueError("Invalid value for `info`, must not be `None`")  # noqa: E501

        self._info = info

    @property
    def approved(self):
        """Gets the approved of this UpgradeProposal.  # noqa: E501

        whether the upgrade has been approved by the active validators  # noqa: E501

        :return: The approved of this UpgradeProposal.  # noqa: E501
        :rtype: bool
        """
        return self._approved

    @approved.setter
    def approved(self, approved):
        """Sets the approved of this UpgradeProposal.

        whether the upgrade has been approved by the active validators  # noqa: E501

        :param approved: The approved of this UpgradeProposal.  # noqa: E501
        :type: bool
        """

        self._approved = approved

    @property
    def approved_percent(self):
        """Gets the approved_percent of this UpgradeProposal.  # noqa: E501

        the percentage of active validators that have approved the upgrade  # noqa: E501

        :return: The approved_percent of this UpgradeProposal.  # noqa: E501
        :rtype: str
        """
        return self._approved_percent

    @approved_percent.setter
    def approved_percent(self, approved_percent):
        """Sets the approved_percent of this UpgradeProposal.

        the percentage of active validators that have approved the upgrade  # noqa: E501

        :param approved_percent: The approved_percent of this UpgradeProposal.  # noqa: E501
        :type: str
        """

        self._approved_percent = approved_percent

    @property
    def validators_to_quorum(self):
        """Gets the validators_to_quorum of this UpgradeProposal.  # noqa: E501

        the amount of additional active validators required to reach quorum for the upgrade  # noqa: E501

        :return: The validators_to_quorum of this UpgradeProposal.  # noqa: E501
        :rtype: int
        """
        return self._validators_to_quorum

    @validators_to_quorum.setter
    def validators_to_quorum(self, validators_to_quorum):
        """Sets the validators_to_quorum of this UpgradeProposal.

        the amount of additional active validators required to reach quorum for the upgrade  # noqa: E501

        :param validators_to_quorum: The validators_to_quorum of this UpgradeProposal.  # noqa: E501
        :type: int
        """

        self._validators_to_quorum = validators_to_quorum

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
        if issubclass(UpgradeProposal, dict):
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
        if not isinstance(other, UpgradeProposal):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other

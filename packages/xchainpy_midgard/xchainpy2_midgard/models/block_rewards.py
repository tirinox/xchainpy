# coding: utf-8

"""
    Midgard Public API

    The Midgard Public API queries THORChain and any chains linked via the Bifröst and prepares information about the network to be readily available for public users. The API parses transaction event data from THORChain and stores them in a time-series database to make time-dependent queries easy. Midgard does not hold critical information. To interact with THORChain protocol, users should query THORNode directly.  # noqa: E501

    OpenAPI spec version: 2.23.2
    Contact: devs@thorchain.org
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

import pprint
import re  # noqa: F401

import six

class BlockRewards(object):
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
        'block_reward': 'str',
        'bond_reward': 'str',
        'pool_reward': 'str'
    }

    attribute_map = {
        'block_reward': 'blockReward',
        'bond_reward': 'bondReward',
        'pool_reward': 'poolReward'
    }

    def __init__(self, block_reward=None, bond_reward=None, pool_reward=None):  # noqa: E501
        """BlockRewards - a model defined in Swagger"""  # noqa: E501
        self._block_reward = None
        self._bond_reward = None
        self._pool_reward = None
        self.discriminator = None
        self.block_reward = block_reward
        self.bond_reward = bond_reward
        self.pool_reward = pool_reward

    @property
    def block_reward(self):
        """Gets the block_reward of this BlockRewards.  # noqa: E501


        :return: The block_reward of this BlockRewards.  # noqa: E501
        :rtype: str
        """
        return self._block_reward

    @block_reward.setter
    def block_reward(self, block_reward):
        """Sets the block_reward of this BlockRewards.


        :param block_reward: The block_reward of this BlockRewards.  # noqa: E501
        :type: str
        """
        if block_reward is None:
            raise ValueError("Invalid value for `block_reward`, must not be `None`")  # noqa: E501

        self._block_reward = block_reward

    @property
    def bond_reward(self):
        """Gets the bond_reward of this BlockRewards.  # noqa: E501


        :return: The bond_reward of this BlockRewards.  # noqa: E501
        :rtype: str
        """
        return self._bond_reward

    @bond_reward.setter
    def bond_reward(self, bond_reward):
        """Sets the bond_reward of this BlockRewards.


        :param bond_reward: The bond_reward of this BlockRewards.  # noqa: E501
        :type: str
        """
        if bond_reward is None:
            raise ValueError("Invalid value for `bond_reward`, must not be `None`")  # noqa: E501

        self._bond_reward = bond_reward

    @property
    def pool_reward(self):
        """Gets the pool_reward of this BlockRewards.  # noqa: E501


        :return: The pool_reward of this BlockRewards.  # noqa: E501
        :rtype: str
        """
        return self._pool_reward

    @pool_reward.setter
    def pool_reward(self, pool_reward):
        """Sets the pool_reward of this BlockRewards.


        :param pool_reward: The pool_reward of this BlockRewards.  # noqa: E501
        :type: str
        """
        if pool_reward is None:
            raise ValueError("Invalid value for `pool_reward`, must not be `None`")  # noqa: E501

        self._pool_reward = pool_reward

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
        if issubclass(BlockRewards, dict):
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
        if not isinstance(other, BlockRewards):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other

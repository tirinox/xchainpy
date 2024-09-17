# coding: utf-8

"""
    Mayanode API

    Mayanode REST API.  # noqa: E501

    OpenAPI spec version: 1.111.0
    Contact: devs@mayachain.org
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

import pprint
import re  # noqa: F401

import six

class Vault(object):
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
        'block_height': 'int',
        'pub_key': 'str',
        'coins': 'list[Coin]',
        'type': 'str',
        'status': 'str',
        'status_since': 'int',
        'membership': 'list[str]',
        'chains': 'list[str]',
        'inbound_tx_count': 'int',
        'outbound_tx_count': 'int',
        'pending_tx_block_heights': 'list[int]',
        'routers': 'list[VaultRouter]',
        'addresses': 'list[VaultAddress]',
        'frozen': 'list[str]'
    }

    attribute_map = {
        'block_height': 'block_height',
        'pub_key': 'pub_key',
        'coins': 'coins',
        'type': 'type',
        'status': 'status',
        'status_since': 'status_since',
        'membership': 'membership',
        'chains': 'chains',
        'inbound_tx_count': 'inbound_tx_count',
        'outbound_tx_count': 'outbound_tx_count',
        'pending_tx_block_heights': 'pending_tx_block_heights',
        'routers': 'routers',
        'addresses': 'addresses',
        'frozen': 'frozen'
    }

    def __init__(self, block_height=None, pub_key=None, coins=None, type=None, status=None, status_since=None, membership=None, chains=None, inbound_tx_count=None, outbound_tx_count=None, pending_tx_block_heights=None, routers=None, addresses=None, frozen=None):  # noqa: E501
        """Vault - a model defined in Swagger"""  # noqa: E501
        self._block_height = None
        self._pub_key = None
        self._coins = None
        self._type = None
        self._status = None
        self._status_since = None
        self._membership = None
        self._chains = None
        self._inbound_tx_count = None
        self._outbound_tx_count = None
        self._pending_tx_block_heights = None
        self._routers = None
        self._addresses = None
        self._frozen = None
        self.discriminator = None
        if block_height is not None:
            self.block_height = block_height
        if pub_key is not None:
            self.pub_key = pub_key
        self.coins = coins
        if type is not None:
            self.type = type
        self.status = status
        if status_since is not None:
            self.status_since = status_since
        if membership is not None:
            self.membership = membership
        if chains is not None:
            self.chains = chains
        if inbound_tx_count is not None:
            self.inbound_tx_count = inbound_tx_count
        if outbound_tx_count is not None:
            self.outbound_tx_count = outbound_tx_count
        if pending_tx_block_heights is not None:
            self.pending_tx_block_heights = pending_tx_block_heights
        self.routers = routers
        self.addresses = addresses
        if frozen is not None:
            self.frozen = frozen

    @property
    def block_height(self):
        """Gets the block_height of this Vault.  # noqa: E501


        :return: The block_height of this Vault.  # noqa: E501
        :rtype: int
        """
        return self._block_height

    @block_height.setter
    def block_height(self, block_height):
        """Sets the block_height of this Vault.


        :param block_height: The block_height of this Vault.  # noqa: E501
        :type: int
        """

        self._block_height = block_height

    @property
    def pub_key(self):
        """Gets the pub_key of this Vault.  # noqa: E501


        :return: The pub_key of this Vault.  # noqa: E501
        :rtype: str
        """
        return self._pub_key

    @pub_key.setter
    def pub_key(self, pub_key):
        """Sets the pub_key of this Vault.


        :param pub_key: The pub_key of this Vault.  # noqa: E501
        :type: str
        """

        self._pub_key = pub_key

    @property
    def coins(self):
        """Gets the coins of this Vault.  # noqa: E501


        :return: The coins of this Vault.  # noqa: E501
        :rtype: list[Coin]
        """
        return self._coins

    @coins.setter
    def coins(self, coins):
        """Sets the coins of this Vault.


        :param coins: The coins of this Vault.  # noqa: E501
        :type: list[Coin]
        """
        if coins is None:
            raise ValueError("Invalid value for `coins`, must not be `None`")  # noqa: E501

        self._coins = coins

    @property
    def type(self):
        """Gets the type of this Vault.  # noqa: E501


        :return: The type of this Vault.  # noqa: E501
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """Sets the type of this Vault.


        :param type: The type of this Vault.  # noqa: E501
        :type: str
        """
        allowed_values = ["AsgardVault", "YggdrasilVault"]  # noqa: E501
        if type not in allowed_values:
            raise ValueError(
                "Invalid value for `type` ({0}), must be one of {1}"  # noqa: E501
                .format(type, allowed_values)
            )

        self._type = type

    @property
    def status(self):
        """Gets the status of this Vault.  # noqa: E501


        :return: The status of this Vault.  # noqa: E501
        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, status):
        """Sets the status of this Vault.


        :param status: The status of this Vault.  # noqa: E501
        :type: str
        """
        if status is None:
            raise ValueError("Invalid value for `status`, must not be `None`")  # noqa: E501

        self._status = status

    @property
    def status_since(self):
        """Gets the status_since of this Vault.  # noqa: E501


        :return: The status_since of this Vault.  # noqa: E501
        :rtype: int
        """
        return self._status_since

    @status_since.setter
    def status_since(self, status_since):
        """Sets the status_since of this Vault.


        :param status_since: The status_since of this Vault.  # noqa: E501
        :type: int
        """

        self._status_since = status_since

    @property
    def membership(self):
        """Gets the membership of this Vault.  # noqa: E501

        the list of node public keys which are members of the vault  # noqa: E501

        :return: The membership of this Vault.  # noqa: E501
        :rtype: list[str]
        """
        return self._membership

    @membership.setter
    def membership(self, membership):
        """Sets the membership of this Vault.

        the list of node public keys which are members of the vault  # noqa: E501

        :param membership: The membership of this Vault.  # noqa: E501
        :type: list[str]
        """

        self._membership = membership

    @property
    def chains(self):
        """Gets the chains of this Vault.  # noqa: E501


        :return: The chains of this Vault.  # noqa: E501
        :rtype: list[str]
        """
        return self._chains

    @chains.setter
    def chains(self, chains):
        """Sets the chains of this Vault.


        :param chains: The chains of this Vault.  # noqa: E501
        :type: list[str]
        """

        self._chains = chains

    @property
    def inbound_tx_count(self):
        """Gets the inbound_tx_count of this Vault.  # noqa: E501


        :return: The inbound_tx_count of this Vault.  # noqa: E501
        :rtype: int
        """
        return self._inbound_tx_count

    @inbound_tx_count.setter
    def inbound_tx_count(self, inbound_tx_count):
        """Sets the inbound_tx_count of this Vault.


        :param inbound_tx_count: The inbound_tx_count of this Vault.  # noqa: E501
        :type: int
        """

        self._inbound_tx_count = inbound_tx_count

    @property
    def outbound_tx_count(self):
        """Gets the outbound_tx_count of this Vault.  # noqa: E501


        :return: The outbound_tx_count of this Vault.  # noqa: E501
        :rtype: int
        """
        return self._outbound_tx_count

    @outbound_tx_count.setter
    def outbound_tx_count(self, outbound_tx_count):
        """Sets the outbound_tx_count of this Vault.


        :param outbound_tx_count: The outbound_tx_count of this Vault.  # noqa: E501
        :type: int
        """

        self._outbound_tx_count = outbound_tx_count

    @property
    def pending_tx_block_heights(self):
        """Gets the pending_tx_block_heights of this Vault.  # noqa: E501


        :return: The pending_tx_block_heights of this Vault.  # noqa: E501
        :rtype: list[int]
        """
        return self._pending_tx_block_heights

    @pending_tx_block_heights.setter
    def pending_tx_block_heights(self, pending_tx_block_heights):
        """Sets the pending_tx_block_heights of this Vault.


        :param pending_tx_block_heights: The pending_tx_block_heights of this Vault.  # noqa: E501
        :type: list[int]
        """

        self._pending_tx_block_heights = pending_tx_block_heights

    @property
    def routers(self):
        """Gets the routers of this Vault.  # noqa: E501


        :return: The routers of this Vault.  # noqa: E501
        :rtype: list[VaultRouter]
        """
        return self._routers

    @routers.setter
    def routers(self, routers):
        """Sets the routers of this Vault.


        :param routers: The routers of this Vault.  # noqa: E501
        :type: list[VaultRouter]
        """
        if routers is None:
            raise ValueError("Invalid value for `routers`, must not be `None`")  # noqa: E501

        self._routers = routers

    @property
    def addresses(self):
        """Gets the addresses of this Vault.  # noqa: E501


        :return: The addresses of this Vault.  # noqa: E501
        :rtype: list[VaultAddress]
        """
        return self._addresses

    @addresses.setter
    def addresses(self, addresses):
        """Sets the addresses of this Vault.


        :param addresses: The addresses of this Vault.  # noqa: E501
        :type: list[VaultAddress]
        """
        if addresses is None:
            raise ValueError("Invalid value for `addresses`, must not be `None`")  # noqa: E501

        self._addresses = addresses

    @property
    def frozen(self):
        """Gets the frozen of this Vault.  # noqa: E501


        :return: The frozen of this Vault.  # noqa: E501
        :rtype: list[str]
        """
        return self._frozen

    @frozen.setter
    def frozen(self, frozen):
        """Sets the frozen of this Vault.


        :param frozen: The frozen of this Vault.  # noqa: E501
        :type: list[str]
        """

        self._frozen = frozen

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
        if issubclass(Vault, dict):
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
        if not isinstance(other, Vault):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other

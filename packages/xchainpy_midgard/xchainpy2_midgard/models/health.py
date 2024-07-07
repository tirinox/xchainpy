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

class Health(object):
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
        'database': 'bool',
        'genesis_info': 'GenesisInf',
        'in_sync': 'bool',
        'last_aggregated': 'HeightTS',
        'last_committed': 'HeightTS',
        'last_fetched': 'HeightTS',
        'last_thor_node': 'HeightTS',
        'scanner_height': 'str'
    }

    attribute_map = {
        'database': 'database',
        'genesis_info': 'genesisInfo',
        'in_sync': 'inSync',
        'last_aggregated': 'lastAggregated',
        'last_committed': 'lastCommitted',
        'last_fetched': 'lastFetched',
        'last_thor_node': 'lastThorNode',
        'scanner_height': 'scannerHeight'
    }

    def __init__(self, database=None, genesis_info=None, in_sync=None, last_aggregated=None, last_committed=None, last_fetched=None, last_thor_node=None, scanner_height=None):  # noqa: E501
        """Health - a model defined in Swagger"""  # noqa: E501
        self._database = None
        self._genesis_info = None
        self._in_sync = None
        self._last_aggregated = None
        self._last_committed = None
        self._last_fetched = None
        self._last_thor_node = None
        self._scanner_height = None
        self.discriminator = None
        self.database = database
        if genesis_info is not None:
            self.genesis_info = genesis_info
        self.in_sync = in_sync
        self.last_aggregated = last_aggregated
        self.last_committed = last_committed
        self.last_fetched = last_fetched
        self.last_thor_node = last_thor_node
        self.scanner_height = scanner_height

    @property
    def database(self):
        """Gets the database of this Health.  # noqa: E501

        True means healthy, connected to database  # noqa: E501

        :return: The database of this Health.  # noqa: E501
        :rtype: bool
        """
        return self._database

    @database.setter
    def database(self, database):
        """Sets the database of this Health.

        True means healthy, connected to database  # noqa: E501

        :param database: The database of this Health.  # noqa: E501
        :type: bool
        """
        if database is None:
            raise ValueError("Invalid value for `database`, must not be `None`")  # noqa: E501

        self._database = database

    @property
    def genesis_info(self):
        """Gets the genesis_info of this Health.  # noqa: E501


        :return: The genesis_info of this Health.  # noqa: E501
        :rtype: GenesisInf
        """
        return self._genesis_info

    @genesis_info.setter
    def genesis_info(self, genesis_info):
        """Sets the genesis_info of this Health.


        :param genesis_info: The genesis_info of this Health.  # noqa: E501
        :type: GenesisInf
        """

        self._genesis_info = genesis_info

    @property
    def in_sync(self):
        """Gets the in_sync of this Health.  # noqa: E501

        True means healthy. False means Midgard is still catching up to the chain  # noqa: E501

        :return: The in_sync of this Health.  # noqa: E501
        :rtype: bool
        """
        return self._in_sync

    @in_sync.setter
    def in_sync(self, in_sync):
        """Sets the in_sync of this Health.

        True means healthy. False means Midgard is still catching up to the chain  # noqa: E501

        :param in_sync: The in_sync of this Health.  # noqa: E501
        :type: bool
        """
        if in_sync is None:
            raise ValueError("Invalid value for `in_sync`, must not be `None`")  # noqa: E501

        self._in_sync = in_sync

    @property
    def last_aggregated(self):
        """Gets the last_aggregated of this Health.  # noqa: E501


        :return: The last_aggregated of this Health.  # noqa: E501
        :rtype: HeightTS
        """
        return self._last_aggregated

    @last_aggregated.setter
    def last_aggregated(self, last_aggregated):
        """Sets the last_aggregated of this Health.


        :param last_aggregated: The last_aggregated of this Health.  # noqa: E501
        :type: HeightTS
        """
        if last_aggregated is None:
            raise ValueError("Invalid value for `last_aggregated`, must not be `None`")  # noqa: E501

        self._last_aggregated = last_aggregated

    @property
    def last_committed(self):
        """Gets the last_committed of this Health.  # noqa: E501


        :return: The last_committed of this Health.  # noqa: E501
        :rtype: HeightTS
        """
        return self._last_committed

    @last_committed.setter
    def last_committed(self, last_committed):
        """Sets the last_committed of this Health.


        :param last_committed: The last_committed of this Health.  # noqa: E501
        :type: HeightTS
        """
        if last_committed is None:
            raise ValueError("Invalid value for `last_committed`, must not be `None`")  # noqa: E501

        self._last_committed = last_committed

    @property
    def last_fetched(self):
        """Gets the last_fetched of this Health.  # noqa: E501


        :return: The last_fetched of this Health.  # noqa: E501
        :rtype: HeightTS
        """
        return self._last_fetched

    @last_fetched.setter
    def last_fetched(self, last_fetched):
        """Sets the last_fetched of this Health.


        :param last_fetched: The last_fetched of this Health.  # noqa: E501
        :type: HeightTS
        """
        if last_fetched is None:
            raise ValueError("Invalid value for `last_fetched`, must not be `None`")  # noqa: E501

        self._last_fetched = last_fetched

    @property
    def last_thor_node(self):
        """Gets the last_thor_node of this Health.  # noqa: E501


        :return: The last_thor_node of this Health.  # noqa: E501
        :rtype: HeightTS
        """
        return self._last_thor_node

    @last_thor_node.setter
    def last_thor_node(self, last_thor_node):
        """Sets the last_thor_node of this Health.


        :param last_thor_node: The last_thor_node of this Health.  # noqa: E501
        :type: HeightTS
        """
        if last_thor_node is None:
            raise ValueError("Invalid value for `last_thor_node`, must not be `None`")  # noqa: E501

        self._last_thor_node = last_thor_node

    @property
    def scanner_height(self):
        """Gets the scanner_height of this Health.  # noqa: E501

        Int64, the current block count  # noqa: E501

        :return: The scanner_height of this Health.  # noqa: E501
        :rtype: str
        """
        return self._scanner_height

    @scanner_height.setter
    def scanner_height(self, scanner_height):
        """Sets the scanner_height of this Health.

        Int64, the current block count  # noqa: E501

        :param scanner_height: The scanner_height of this Health.  # noqa: E501
        :type: str
        """
        if scanner_height is None:
            raise ValueError("Invalid value for `scanner_height`, must not be `None`")  # noqa: E501

        self._scanner_height = scanner_height

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
        if issubclass(Health, dict):
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
        if not isinstance(other, Health):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other

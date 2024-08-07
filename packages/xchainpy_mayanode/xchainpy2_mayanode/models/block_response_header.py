# coding: utf-8

"""
    Mayanode API

    Mayanode REST API.  # noqa: E501

    OpenAPI spec version: 1.110.0
    Contact: devs@mayachain.org
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

import pprint
import re  # noqa: F401

import six

class BlockResponseHeader(object):
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
        'version': 'BlockResponseHeaderVersion',
        'chain_id': 'str',
        'height': 'int',
        'time': 'str',
        'last_block_id': 'BlockResponseId',
        'last_commit_hash': 'str',
        'data_hash': 'str',
        'validators_hash': 'str',
        'next_validators_hash': 'str',
        'consensus_hash': 'str',
        'app_hash': 'str',
        'last_results_hash': 'str',
        'evidence_hash': 'str',
        'proposer_address': 'str'
    }

    attribute_map = {
        'version': 'version',
        'chain_id': 'chain_id',
        'height': 'height',
        'time': 'time',
        'last_block_id': 'last_block_id',
        'last_commit_hash': 'last_commit_hash',
        'data_hash': 'data_hash',
        'validators_hash': 'validators_hash',
        'next_validators_hash': 'next_validators_hash',
        'consensus_hash': 'consensus_hash',
        'app_hash': 'app_hash',
        'last_results_hash': 'last_results_hash',
        'evidence_hash': 'evidence_hash',
        'proposer_address': 'proposer_address'
    }

    def __init__(self, version=None, chain_id=None, height=None, time=None, last_block_id=None, last_commit_hash=None, data_hash=None, validators_hash=None, next_validators_hash=None, consensus_hash=None, app_hash=None, last_results_hash=None, evidence_hash=None, proposer_address=None):  # noqa: E501
        """BlockResponseHeader - a model defined in Swagger"""  # noqa: E501
        self._version = None
        self._chain_id = None
        self._height = None
        self._time = None
        self._last_block_id = None
        self._last_commit_hash = None
        self._data_hash = None
        self._validators_hash = None
        self._next_validators_hash = None
        self._consensus_hash = None
        self._app_hash = None
        self._last_results_hash = None
        self._evidence_hash = None
        self._proposer_address = None
        self.discriminator = None
        self.version = version
        self.chain_id = chain_id
        self.height = height
        self.time = time
        self.last_block_id = last_block_id
        self.last_commit_hash = last_commit_hash
        self.data_hash = data_hash
        self.validators_hash = validators_hash
        self.next_validators_hash = next_validators_hash
        self.consensus_hash = consensus_hash
        self.app_hash = app_hash
        self.last_results_hash = last_results_hash
        self.evidence_hash = evidence_hash
        self.proposer_address = proposer_address

    @property
    def version(self):
        """Gets the version of this BlockResponseHeader.  # noqa: E501


        :return: The version of this BlockResponseHeader.  # noqa: E501
        :rtype: BlockResponseHeaderVersion
        """
        return self._version

    @version.setter
    def version(self, version):
        """Sets the version of this BlockResponseHeader.


        :param version: The version of this BlockResponseHeader.  # noqa: E501
        :type: BlockResponseHeaderVersion
        """
        if version is None:
            raise ValueError("Invalid value for `version`, must not be `None`")  # noqa: E501

        self._version = version

    @property
    def chain_id(self):
        """Gets the chain_id of this BlockResponseHeader.  # noqa: E501


        :return: The chain_id of this BlockResponseHeader.  # noqa: E501
        :rtype: str
        """
        return self._chain_id

    @chain_id.setter
    def chain_id(self, chain_id):
        """Sets the chain_id of this BlockResponseHeader.


        :param chain_id: The chain_id of this BlockResponseHeader.  # noqa: E501
        :type: str
        """
        if chain_id is None:
            raise ValueError("Invalid value for `chain_id`, must not be `None`")  # noqa: E501

        self._chain_id = chain_id

    @property
    def height(self):
        """Gets the height of this BlockResponseHeader.  # noqa: E501


        :return: The height of this BlockResponseHeader.  # noqa: E501
        :rtype: int
        """
        return self._height

    @height.setter
    def height(self, height):
        """Sets the height of this BlockResponseHeader.


        :param height: The height of this BlockResponseHeader.  # noqa: E501
        :type: int
        """
        if height is None:
            raise ValueError("Invalid value for `height`, must not be `None`")  # noqa: E501

        self._height = height

    @property
    def time(self):
        """Gets the time of this BlockResponseHeader.  # noqa: E501


        :return: The time of this BlockResponseHeader.  # noqa: E501
        :rtype: str
        """
        return self._time

    @time.setter
    def time(self, time):
        """Sets the time of this BlockResponseHeader.


        :param time: The time of this BlockResponseHeader.  # noqa: E501
        :type: str
        """
        if time is None:
            raise ValueError("Invalid value for `time`, must not be `None`")  # noqa: E501

        self._time = time

    @property
    def last_block_id(self):
        """Gets the last_block_id of this BlockResponseHeader.  # noqa: E501


        :return: The last_block_id of this BlockResponseHeader.  # noqa: E501
        :rtype: BlockResponseId
        """
        return self._last_block_id

    @last_block_id.setter
    def last_block_id(self, last_block_id):
        """Sets the last_block_id of this BlockResponseHeader.


        :param last_block_id: The last_block_id of this BlockResponseHeader.  # noqa: E501
        :type: BlockResponseId
        """
        if last_block_id is None:
            raise ValueError("Invalid value for `last_block_id`, must not be `None`")  # noqa: E501

        self._last_block_id = last_block_id

    @property
    def last_commit_hash(self):
        """Gets the last_commit_hash of this BlockResponseHeader.  # noqa: E501


        :return: The last_commit_hash of this BlockResponseHeader.  # noqa: E501
        :rtype: str
        """
        return self._last_commit_hash

    @last_commit_hash.setter
    def last_commit_hash(self, last_commit_hash):
        """Sets the last_commit_hash of this BlockResponseHeader.


        :param last_commit_hash: The last_commit_hash of this BlockResponseHeader.  # noqa: E501
        :type: str
        """
        if last_commit_hash is None:
            raise ValueError("Invalid value for `last_commit_hash`, must not be `None`")  # noqa: E501

        self._last_commit_hash = last_commit_hash

    @property
    def data_hash(self):
        """Gets the data_hash of this BlockResponseHeader.  # noqa: E501


        :return: The data_hash of this BlockResponseHeader.  # noqa: E501
        :rtype: str
        """
        return self._data_hash

    @data_hash.setter
    def data_hash(self, data_hash):
        """Sets the data_hash of this BlockResponseHeader.


        :param data_hash: The data_hash of this BlockResponseHeader.  # noqa: E501
        :type: str
        """
        if data_hash is None:
            raise ValueError("Invalid value for `data_hash`, must not be `None`")  # noqa: E501

        self._data_hash = data_hash

    @property
    def validators_hash(self):
        """Gets the validators_hash of this BlockResponseHeader.  # noqa: E501


        :return: The validators_hash of this BlockResponseHeader.  # noqa: E501
        :rtype: str
        """
        return self._validators_hash

    @validators_hash.setter
    def validators_hash(self, validators_hash):
        """Sets the validators_hash of this BlockResponseHeader.


        :param validators_hash: The validators_hash of this BlockResponseHeader.  # noqa: E501
        :type: str
        """
        if validators_hash is None:
            raise ValueError("Invalid value for `validators_hash`, must not be `None`")  # noqa: E501

        self._validators_hash = validators_hash

    @property
    def next_validators_hash(self):
        """Gets the next_validators_hash of this BlockResponseHeader.  # noqa: E501


        :return: The next_validators_hash of this BlockResponseHeader.  # noqa: E501
        :rtype: str
        """
        return self._next_validators_hash

    @next_validators_hash.setter
    def next_validators_hash(self, next_validators_hash):
        """Sets the next_validators_hash of this BlockResponseHeader.


        :param next_validators_hash: The next_validators_hash of this BlockResponseHeader.  # noqa: E501
        :type: str
        """
        if next_validators_hash is None:
            raise ValueError("Invalid value for `next_validators_hash`, must not be `None`")  # noqa: E501

        self._next_validators_hash = next_validators_hash

    @property
    def consensus_hash(self):
        """Gets the consensus_hash of this BlockResponseHeader.  # noqa: E501


        :return: The consensus_hash of this BlockResponseHeader.  # noqa: E501
        :rtype: str
        """
        return self._consensus_hash

    @consensus_hash.setter
    def consensus_hash(self, consensus_hash):
        """Sets the consensus_hash of this BlockResponseHeader.


        :param consensus_hash: The consensus_hash of this BlockResponseHeader.  # noqa: E501
        :type: str
        """
        if consensus_hash is None:
            raise ValueError("Invalid value for `consensus_hash`, must not be `None`")  # noqa: E501

        self._consensus_hash = consensus_hash

    @property
    def app_hash(self):
        """Gets the app_hash of this BlockResponseHeader.  # noqa: E501


        :return: The app_hash of this BlockResponseHeader.  # noqa: E501
        :rtype: str
        """
        return self._app_hash

    @app_hash.setter
    def app_hash(self, app_hash):
        """Sets the app_hash of this BlockResponseHeader.


        :param app_hash: The app_hash of this BlockResponseHeader.  # noqa: E501
        :type: str
        """
        if app_hash is None:
            raise ValueError("Invalid value for `app_hash`, must not be `None`")  # noqa: E501

        self._app_hash = app_hash

    @property
    def last_results_hash(self):
        """Gets the last_results_hash of this BlockResponseHeader.  # noqa: E501


        :return: The last_results_hash of this BlockResponseHeader.  # noqa: E501
        :rtype: str
        """
        return self._last_results_hash

    @last_results_hash.setter
    def last_results_hash(self, last_results_hash):
        """Sets the last_results_hash of this BlockResponseHeader.


        :param last_results_hash: The last_results_hash of this BlockResponseHeader.  # noqa: E501
        :type: str
        """
        if last_results_hash is None:
            raise ValueError("Invalid value for `last_results_hash`, must not be `None`")  # noqa: E501

        self._last_results_hash = last_results_hash

    @property
    def evidence_hash(self):
        """Gets the evidence_hash of this BlockResponseHeader.  # noqa: E501


        :return: The evidence_hash of this BlockResponseHeader.  # noqa: E501
        :rtype: str
        """
        return self._evidence_hash

    @evidence_hash.setter
    def evidence_hash(self, evidence_hash):
        """Sets the evidence_hash of this BlockResponseHeader.


        :param evidence_hash: The evidence_hash of this BlockResponseHeader.  # noqa: E501
        :type: str
        """
        if evidence_hash is None:
            raise ValueError("Invalid value for `evidence_hash`, must not be `None`")  # noqa: E501

        self._evidence_hash = evidence_hash

    @property
    def proposer_address(self):
        """Gets the proposer_address of this BlockResponseHeader.  # noqa: E501


        :return: The proposer_address of this BlockResponseHeader.  # noqa: E501
        :rtype: str
        """
        return self._proposer_address

    @proposer_address.setter
    def proposer_address(self, proposer_address):
        """Sets the proposer_address of this BlockResponseHeader.


        :param proposer_address: The proposer_address of this BlockResponseHeader.  # noqa: E501
        :type: str
        """
        if proposer_address is None:
            raise ValueError("Invalid value for `proposer_address`, must not be `None`")  # noqa: E501

        self._proposer_address = proposer_address

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
        if issubclass(BlockResponseHeader, dict):
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
        if not isinstance(other, BlockResponseHeader):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other

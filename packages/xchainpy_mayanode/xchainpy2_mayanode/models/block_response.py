# coding: utf-8

"""
    Mayanode API

    Mayanode REST API.  # noqa: E501

    OpenAPI spec version: 1.112.0
    Contact: devs@mayachain.org
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

import pprint
import re  # noqa: F401

import six

class BlockResponse(object):
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
        'id': 'BlockResponseId',
        'header': 'BlockResponseHeader',
        'begin_block_events': 'list[dict(str, str)]',
        'end_block_events': 'list[dict(str, str)]',
        'txs': 'list[BlockTx]'
    }

    attribute_map = {
        'id': 'id',
        'header': 'header',
        'begin_block_events': 'begin_block_events',
        'end_block_events': 'end_block_events',
        'txs': 'txs'
    }

    def __init__(self, id=None, header=None, begin_block_events=None, end_block_events=None, txs=None):  # noqa: E501
        """BlockResponse - a model defined in Swagger"""  # noqa: E501
        self._id = None
        self._header = None
        self._begin_block_events = None
        self._end_block_events = None
        self._txs = None
        self.discriminator = None
        self.id = id
        self.header = header
        self.begin_block_events = begin_block_events
        self.end_block_events = end_block_events
        self.txs = txs

    @property
    def id(self):
        """Gets the id of this BlockResponse.  # noqa: E501


        :return: The id of this BlockResponse.  # noqa: E501
        :rtype: BlockResponseId
        """
        return self._id

    @id.setter
    def id(self, id):
        """Sets the id of this BlockResponse.


        :param id: The id of this BlockResponse.  # noqa: E501
        :type: BlockResponseId
        """
        if id is None:
            raise ValueError("Invalid value for `id`, must not be `None`")  # noqa: E501

        self._id = id

    @property
    def header(self):
        """Gets the header of this BlockResponse.  # noqa: E501


        :return: The header of this BlockResponse.  # noqa: E501
        :rtype: BlockResponseHeader
        """
        return self._header

    @header.setter
    def header(self, header):
        """Sets the header of this BlockResponse.


        :param header: The header of this BlockResponse.  # noqa: E501
        :type: BlockResponseHeader
        """
        if header is None:
            raise ValueError("Invalid value for `header`, must not be `None`")  # noqa: E501

        self._header = header

    @property
    def begin_block_events(self):
        """Gets the begin_block_events of this BlockResponse.  # noqa: E501


        :return: The begin_block_events of this BlockResponse.  # noqa: E501
        :rtype: list[dict(str, str)]
        """
        return self._begin_block_events

    @begin_block_events.setter
    def begin_block_events(self, begin_block_events):
        """Sets the begin_block_events of this BlockResponse.


        :param begin_block_events: The begin_block_events of this BlockResponse.  # noqa: E501
        :type: list[dict(str, str)]
        """
        if begin_block_events is None:
            raise ValueError("Invalid value for `begin_block_events`, must not be `None`")  # noqa: E501

        self._begin_block_events = begin_block_events

    @property
    def end_block_events(self):
        """Gets the end_block_events of this BlockResponse.  # noqa: E501


        :return: The end_block_events of this BlockResponse.  # noqa: E501
        :rtype: list[dict(str, str)]
        """
        return self._end_block_events

    @end_block_events.setter
    def end_block_events(self, end_block_events):
        """Sets the end_block_events of this BlockResponse.


        :param end_block_events: The end_block_events of this BlockResponse.  # noqa: E501
        :type: list[dict(str, str)]
        """
        if end_block_events is None:
            raise ValueError("Invalid value for `end_block_events`, must not be `None`")  # noqa: E501

        self._end_block_events = end_block_events

    @property
    def txs(self):
        """Gets the txs of this BlockResponse.  # noqa: E501


        :return: The txs of this BlockResponse.  # noqa: E501
        :rtype: list[BlockTx]
        """
        return self._txs

    @txs.setter
    def txs(self, txs):
        """Sets the txs of this BlockResponse.


        :param txs: The txs of this BlockResponse.  # noqa: E501
        :type: list[BlockTx]
        """
        if txs is None:
            raise ValueError("Invalid value for `txs`, must not be `None`")  # noqa: E501

        self._txs = txs

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
        if issubclass(BlockResponse, dict):
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
        if not isinstance(other, BlockResponse):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other

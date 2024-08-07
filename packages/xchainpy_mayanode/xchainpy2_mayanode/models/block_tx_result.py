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

class BlockTxResult(object):
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
        'code': 'int',
        'data': 'str',
        'log': 'str',
        'info': 'str',
        'gas_wanted': 'str',
        'gas_used': 'str',
        'events': 'list[dict(str, str)]',
        'codespace': 'str'
    }

    attribute_map = {
        'code': 'code',
        'data': 'data',
        'log': 'log',
        'info': 'info',
        'gas_wanted': 'gas_wanted',
        'gas_used': 'gas_used',
        'events': 'events',
        'codespace': 'codespace'
    }

    def __init__(self, code=None, data=None, log=None, info=None, gas_wanted=None, gas_used=None, events=None, codespace=None):  # noqa: E501
        """BlockTxResult - a model defined in Swagger"""  # noqa: E501
        self._code = None
        self._data = None
        self._log = None
        self._info = None
        self._gas_wanted = None
        self._gas_used = None
        self._events = None
        self._codespace = None
        self.discriminator = None
        if code is not None:
            self.code = code
        if data is not None:
            self.data = data
        if log is not None:
            self.log = log
        if info is not None:
            self.info = info
        if gas_wanted is not None:
            self.gas_wanted = gas_wanted
        if gas_used is not None:
            self.gas_used = gas_used
        if events is not None:
            self.events = events
        if codespace is not None:
            self.codespace = codespace

    @property
    def code(self):
        """Gets the code of this BlockTxResult.  # noqa: E501


        :return: The code of this BlockTxResult.  # noqa: E501
        :rtype: int
        """
        return self._code

    @code.setter
    def code(self, code):
        """Sets the code of this BlockTxResult.


        :param code: The code of this BlockTxResult.  # noqa: E501
        :type: int
        """

        self._code = code

    @property
    def data(self):
        """Gets the data of this BlockTxResult.  # noqa: E501


        :return: The data of this BlockTxResult.  # noqa: E501
        :rtype: str
        """
        return self._data

    @data.setter
    def data(self, data):
        """Sets the data of this BlockTxResult.


        :param data: The data of this BlockTxResult.  # noqa: E501
        :type: str
        """

        self._data = data

    @property
    def log(self):
        """Gets the log of this BlockTxResult.  # noqa: E501


        :return: The log of this BlockTxResult.  # noqa: E501
        :rtype: str
        """
        return self._log

    @log.setter
    def log(self, log):
        """Sets the log of this BlockTxResult.


        :param log: The log of this BlockTxResult.  # noqa: E501
        :type: str
        """

        self._log = log

    @property
    def info(self):
        """Gets the info of this BlockTxResult.  # noqa: E501


        :return: The info of this BlockTxResult.  # noqa: E501
        :rtype: str
        """
        return self._info

    @info.setter
    def info(self, info):
        """Sets the info of this BlockTxResult.


        :param info: The info of this BlockTxResult.  # noqa: E501
        :type: str
        """

        self._info = info

    @property
    def gas_wanted(self):
        """Gets the gas_wanted of this BlockTxResult.  # noqa: E501


        :return: The gas_wanted of this BlockTxResult.  # noqa: E501
        :rtype: str
        """
        return self._gas_wanted

    @gas_wanted.setter
    def gas_wanted(self, gas_wanted):
        """Sets the gas_wanted of this BlockTxResult.


        :param gas_wanted: The gas_wanted of this BlockTxResult.  # noqa: E501
        :type: str
        """

        self._gas_wanted = gas_wanted

    @property
    def gas_used(self):
        """Gets the gas_used of this BlockTxResult.  # noqa: E501


        :return: The gas_used of this BlockTxResult.  # noqa: E501
        :rtype: str
        """
        return self._gas_used

    @gas_used.setter
    def gas_used(self, gas_used):
        """Sets the gas_used of this BlockTxResult.


        :param gas_used: The gas_used of this BlockTxResult.  # noqa: E501
        :type: str
        """

        self._gas_used = gas_used

    @property
    def events(self):
        """Gets the events of this BlockTxResult.  # noqa: E501


        :return: The events of this BlockTxResult.  # noqa: E501
        :rtype: list[dict(str, str)]
        """
        return self._events

    @events.setter
    def events(self, events):
        """Sets the events of this BlockTxResult.


        :param events: The events of this BlockTxResult.  # noqa: E501
        :type: list[dict(str, str)]
        """

        self._events = events

    @property
    def codespace(self):
        """Gets the codespace of this BlockTxResult.  # noqa: E501


        :return: The codespace of this BlockTxResult.  # noqa: E501
        :rtype: str
        """
        return self._codespace

    @codespace.setter
    def codespace(self, codespace):
        """Sets the codespace of this BlockTxResult.


        :param codespace: The codespace of this BlockTxResult.  # noqa: E501
        :type: str
        """

        self._codespace = codespace

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
        if issubclass(BlockTxResult, dict):
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
        if not isinstance(other, BlockTxResult):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other

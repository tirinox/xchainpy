# coding: utf-8

"""
    Midgard Public API

    The Midgard Public API queries THORChain and any chains linked via the Bifröst and prepares information about the network to be readily available for public users. The API parses transaction event data from THORChain and stores them in a time-series database to make time-dependent queries easy. Midgard does not hold critical information. To interact with THORChain protocol, users should query THORNode directly.  # noqa: E501

    OpenAPI spec version: 2.20.1
    Contact: devs@thorchain.org
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

import pprint
import re  # noqa: F401

import six

class Action(object):
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
        '_date': 'str',
        'height': 'str',
        '_in': 'list[Transaction]',
        'metadata': 'Metadata',
        'out': 'list[Transaction]',
        'pools': 'list[str]',
        'status': 'str',
        'type': 'str'
    }

    attribute_map = {
        '_date': 'date',
        'height': 'height',
        '_in': 'in',
        'metadata': 'metadata',
        'out': 'out',
        'pools': 'pools',
        'status': 'status',
        'type': 'type'
    }

    def __init__(self, _date=None, height=None, _in=None, metadata=None, out=None, pools=None, status=None, type=None):  # noqa: E501
        """Action - a model defined in Swagger"""  # noqa: E501
        self.__date = None
        self._height = None
        self.__in = None
        self._metadata = None
        self._out = None
        self._pools = None
        self._status = None
        self._type = None
        self.discriminator = None
        self._date = _date
        self.height = height
        self._in = _in
        self.metadata = metadata
        self.out = out
        self.pools = pools
        self.status = status
        self.type = type

    @property
    def _date(self):
        """Gets the _date of this Action.  # noqa: E501

        Int64, nano timestamp of the block at which the action was registered  # noqa: E501

        :return: The _date of this Action.  # noqa: E501
        :rtype: str
        """
        return self.__date

    @_date.setter
    def _date(self, _date):
        """Sets the _date of this Action.

        Int64, nano timestamp of the block at which the action was registered  # noqa: E501

        :param _date: The _date of this Action.  # noqa: E501
        :type: str
        """
        if _date is None:
            raise ValueError("Invalid value for `_date`, must not be `None`")  # noqa: E501

        self.__date = _date

    @property
    def height(self):
        """Gets the height of this Action.  # noqa: E501

        Int64, height of the block at which the action was registered  # noqa: E501

        :return: The height of this Action.  # noqa: E501
        :rtype: str
        """
        return self._height

    @height.setter
    def height(self, height):
        """Sets the height of this Action.

        Int64, height of the block at which the action was registered  # noqa: E501

        :param height: The height of this Action.  # noqa: E501
        :type: str
        """
        if height is None:
            raise ValueError("Invalid value for `height`, must not be `None`")  # noqa: E501

        self._height = height

    @property
    def _in(self):
        """Gets the _in of this Action.  # noqa: E501

        Inbound transactions related to the action  # noqa: E501

        :return: The _in of this Action.  # noqa: E501
        :rtype: list[Transaction]
        """
        return self.__in

    @_in.setter
    def _in(self, _in):
        """Sets the _in of this Action.

        Inbound transactions related to the action  # noqa: E501

        :param _in: The _in of this Action.  # noqa: E501
        :type: list[Transaction]
        """
        if _in is None:
            raise ValueError("Invalid value for `_in`, must not be `None`")  # noqa: E501

        self.__in = _in

    @property
    def metadata(self):
        """Gets the metadata of this Action.  # noqa: E501


        :return: The metadata of this Action.  # noqa: E501
        :rtype: Metadata
        """
        return self._metadata

    @metadata.setter
    def metadata(self, metadata):
        """Sets the metadata of this Action.


        :param metadata: The metadata of this Action.  # noqa: E501
        :type: Metadata
        """
        if metadata is None:
            raise ValueError("Invalid value for `metadata`, must not be `None`")  # noqa: E501

        self._metadata = metadata

    @property
    def out(self):
        """Gets the out of this Action.  # noqa: E501

        Outbound transactions related to the action  # noqa: E501

        :return: The out of this Action.  # noqa: E501
        :rtype: list[Transaction]
        """
        return self._out

    @out.setter
    def out(self, out):
        """Sets the out of this Action.

        Outbound transactions related to the action  # noqa: E501

        :param out: The out of this Action.  # noqa: E501
        :type: list[Transaction]
        """
        if out is None:
            raise ValueError("Invalid value for `out`, must not be `None`")  # noqa: E501

        self._out = out

    @property
    def pools(self):
        """Gets the pools of this Action.  # noqa: E501

        Pools involved in the action  # noqa: E501

        :return: The pools of this Action.  # noqa: E501
        :rtype: list[str]
        """
        return self._pools

    @pools.setter
    def pools(self, pools):
        """Sets the pools of this Action.

        Pools involved in the action  # noqa: E501

        :param pools: The pools of this Action.  # noqa: E501
        :type: list[str]
        """
        if pools is None:
            raise ValueError("Invalid value for `pools`, must not be `None`")  # noqa: E501

        self._pools = pools

    @property
    def status(self):
        """Gets the status of this Action.  # noqa: E501

        Indicates if the action is completed or if related outbound transactions are still pending.   # noqa: E501

        :return: The status of this Action.  # noqa: E501
        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, status):
        """Sets the status of this Action.

        Indicates if the action is completed or if related outbound transactions are still pending.   # noqa: E501

        :param status: The status of this Action.  # noqa: E501
        :type: str
        """
        if status is None:
            raise ValueError("Invalid value for `status`, must not be `None`")  # noqa: E501
        allowed_values = ["success", "pending"]  # noqa: E501
        if status not in allowed_values:
            raise ValueError(
                "Invalid value for `status` ({0}), must be one of {1}"  # noqa: E501
                .format(status, allowed_values)
            )

        self._status = status

    @property
    def type(self):
        """Gets the type of this Action.  # noqa: E501

        Type of action  # noqa: E501

        :return: The type of this Action.  # noqa: E501
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """Sets the type of this Action.

        Type of action  # noqa: E501

        :param type: The type of this Action.  # noqa: E501
        :type: str
        """
        if type is None:
            raise ValueError("Invalid value for `type`, must not be `None`")  # noqa: E501
        allowed_values = ["swap", "addLiquidity", "withdraw", "donate", "refund", "switch"]  # noqa: E501
        if type not in allowed_values:
            raise ValueError(
                "Invalid value for `type` ({0}), must be one of {1}"  # noqa: E501
                .format(type, allowed_values)
            )

        self._type = type

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
        if issubclass(Action, dict):
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
        if not isinstance(other, Action):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other

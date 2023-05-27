# coding: utf-8

"""
    Mayanode API

    Mayanode REST API.  # noqa: E501

    OpenAPI spec version: 1.104.0
    Contact: devs@mayachain.org
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

import pprint
import re  # noqa: F401

import six

class InboundAddress(object):
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
        'chain': 'str',
        'pub_key': 'str',
        'address': 'str',
        'gas_rate': 'str',
        'router': 'str',
        'halted': 'bool'
    }

    attribute_map = {
        'chain': 'chain',
        'pub_key': 'pub_key',
        'address': 'address',
        'gas_rate': 'gas_rate',
        'router': 'router',
        'halted': 'halted'
    }

    def __init__(self, chain=None, pub_key=None, address=None, gas_rate=None, router=None, halted=None):  # noqa: E501
        """InboundAddress - a model defined in Swagger"""  # noqa: E501
        self._chain = None
        self._pub_key = None
        self._address = None
        self._gas_rate = None
        self._router = None
        self._halted = None
        self.discriminator = None
        if chain is not None:
            self.chain = chain
        if pub_key is not None:
            self.pub_key = pub_key
        if address is not None:
            self.address = address
        if gas_rate is not None:
            self.gas_rate = gas_rate
        if router is not None:
            self.router = router
        self.halted = halted

    @property
    def chain(self):
        """Gets the chain of this InboundAddress.  # noqa: E501


        :return: The chain of this InboundAddress.  # noqa: E501
        :rtype: str
        """
        return self._chain

    @chain.setter
    def chain(self, chain):
        """Sets the chain of this InboundAddress.


        :param chain: The chain of this InboundAddress.  # noqa: E501
        :type: str
        """

        self._chain = chain

    @property
    def pub_key(self):
        """Gets the pub_key of this InboundAddress.  # noqa: E501


        :return: The pub_key of this InboundAddress.  # noqa: E501
        :rtype: str
        """
        return self._pub_key

    @pub_key.setter
    def pub_key(self, pub_key):
        """Sets the pub_key of this InboundAddress.


        :param pub_key: The pub_key of this InboundAddress.  # noqa: E501
        :type: str
        """

        self._pub_key = pub_key

    @property
    def address(self):
        """Gets the address of this InboundAddress.  # noqa: E501


        :return: The address of this InboundAddress.  # noqa: E501
        :rtype: str
        """
        return self._address

    @address.setter
    def address(self, address):
        """Sets the address of this InboundAddress.


        :param address: The address of this InboundAddress.  # noqa: E501
        :type: str
        """

        self._address = address

    @property
    def gas_rate(self):
        """Gets the gas_rate of this InboundAddress.  # noqa: E501


        :return: The gas_rate of this InboundAddress.  # noqa: E501
        :rtype: str
        """
        return self._gas_rate

    @gas_rate.setter
    def gas_rate(self, gas_rate):
        """Sets the gas_rate of this InboundAddress.


        :param gas_rate: The gas_rate of this InboundAddress.  # noqa: E501
        :type: str
        """

        self._gas_rate = gas_rate

    @property
    def router(self):
        """Gets the router of this InboundAddress.  # noqa: E501


        :return: The router of this InboundAddress.  # noqa: E501
        :rtype: str
        """
        return self._router

    @router.setter
    def router(self, router):
        """Sets the router of this InboundAddress.


        :param router: The router of this InboundAddress.  # noqa: E501
        :type: str
        """

        self._router = router

    @property
    def halted(self):
        """Gets the halted of this InboundAddress.  # noqa: E501


        :return: The halted of this InboundAddress.  # noqa: E501
        :rtype: bool
        """
        return self._halted

    @halted.setter
    def halted(self, halted):
        """Sets the halted of this InboundAddress.


        :param halted: The halted of this InboundAddress.  # noqa: E501
        :type: bool
        """
        if halted is None:
            raise ValueError("Invalid value for `halted`, must not be `None`")  # noqa: E501

        self._halted = halted

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
        if issubclass(InboundAddress, dict):
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
        if not isinstance(other, InboundAddress):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other

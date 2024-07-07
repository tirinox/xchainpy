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

class Metadata(object):
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
        'add_liquidity': 'AddLiquidityMetadata',
        'refund': 'RefundMetadata',
        'send': 'SendMetadata',
        'swap': 'SwapMetadata',
        'thorname': 'ThornameMetadata',
        'withdraw': 'WithdrawMetadata'
    }

    attribute_map = {
        'add_liquidity': 'addLiquidity',
        'refund': 'refund',
        'send': 'send',
        'swap': 'swap',
        'thorname': 'thorname',
        'withdraw': 'withdraw'
    }

    def __init__(self, add_liquidity=None, refund=None, send=None, swap=None, thorname=None, withdraw=None):  # noqa: E501
        """Metadata - a model defined in Swagger"""  # noqa: E501
        self._add_liquidity = None
        self._refund = None
        self._send = None
        self._swap = None
        self._thorname = None
        self._withdraw = None
        self.discriminator = None
        if add_liquidity is not None:
            self.add_liquidity = add_liquidity
        if refund is not None:
            self.refund = refund
        if send is not None:
            self.send = send
        if swap is not None:
            self.swap = swap
        if thorname is not None:
            self.thorname = thorname
        if withdraw is not None:
            self.withdraw = withdraw

    @property
    def add_liquidity(self):
        """Gets the add_liquidity of this Metadata.  # noqa: E501


        :return: The add_liquidity of this Metadata.  # noqa: E501
        :rtype: AddLiquidityMetadata
        """
        return self._add_liquidity

    @add_liquidity.setter
    def add_liquidity(self, add_liquidity):
        """Sets the add_liquidity of this Metadata.


        :param add_liquidity: The add_liquidity of this Metadata.  # noqa: E501
        :type: AddLiquidityMetadata
        """

        self._add_liquidity = add_liquidity

    @property
    def refund(self):
        """Gets the refund of this Metadata.  # noqa: E501


        :return: The refund of this Metadata.  # noqa: E501
        :rtype: RefundMetadata
        """
        return self._refund

    @refund.setter
    def refund(self, refund):
        """Sets the refund of this Metadata.


        :param refund: The refund of this Metadata.  # noqa: E501
        :type: RefundMetadata
        """

        self._refund = refund

    @property
    def send(self):
        """Gets the send of this Metadata.  # noqa: E501


        :return: The send of this Metadata.  # noqa: E501
        :rtype: SendMetadata
        """
        return self._send

    @send.setter
    def send(self, send):
        """Sets the send of this Metadata.


        :param send: The send of this Metadata.  # noqa: E501
        :type: SendMetadata
        """

        self._send = send

    @property
    def swap(self):
        """Gets the swap of this Metadata.  # noqa: E501


        :return: The swap of this Metadata.  # noqa: E501
        :rtype: SwapMetadata
        """
        return self._swap

    @swap.setter
    def swap(self, swap):
        """Sets the swap of this Metadata.


        :param swap: The swap of this Metadata.  # noqa: E501
        :type: SwapMetadata
        """

        self._swap = swap

    @property
    def thorname(self):
        """Gets the thorname of this Metadata.  # noqa: E501


        :return: The thorname of this Metadata.  # noqa: E501
        :rtype: ThornameMetadata
        """
        return self._thorname

    @thorname.setter
    def thorname(self, thorname):
        """Sets the thorname of this Metadata.


        :param thorname: The thorname of this Metadata.  # noqa: E501
        :type: ThornameMetadata
        """

        self._thorname = thorname

    @property
    def withdraw(self):
        """Gets the withdraw of this Metadata.  # noqa: E501


        :return: The withdraw of this Metadata.  # noqa: E501
        :rtype: WithdrawMetadata
        """
        return self._withdraw

    @withdraw.setter
    def withdraw(self, withdraw):
        """Sets the withdraw of this Metadata.


        :param withdraw: The withdraw of this Metadata.  # noqa: E501
        :type: WithdrawMetadata
        """

        self._withdraw = withdraw

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
        if issubclass(Metadata, dict):
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
        if not isinstance(other, Metadata):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other

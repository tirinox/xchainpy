# coding: utf-8

"""
    Thornode API

    Thornode REST API.  # noqa: E501

    OpenAPI spec version: 2.135.0
    Contact: devs@thorchain.org
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

import pprint
import re  # noqa: F401

import six

class TxResponse(object):
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
        'observed_tx': 'ObservedTx',
        'consensus_height': 'int',
        'finalised_height': 'int',
        'outbound_height': 'int',
        'keysign_metric': 'TssKeysignMetric'
    }

    attribute_map = {
        'observed_tx': 'observed_tx',
        'consensus_height': 'consensus_height',
        'finalised_height': 'finalised_height',
        'outbound_height': 'outbound_height',
        'keysign_metric': 'keysign_metric'
    }

    def __init__(self, observed_tx=None, consensus_height=None, finalised_height=None, outbound_height=None, keysign_metric=None):  # noqa: E501
        """TxResponse - a model defined in Swagger"""  # noqa: E501
        self._observed_tx = None
        self._consensus_height = None
        self._finalised_height = None
        self._outbound_height = None
        self._keysign_metric = None
        self.discriminator = None
        if observed_tx is not None:
            self.observed_tx = observed_tx
        if consensus_height is not None:
            self.consensus_height = consensus_height
        if finalised_height is not None:
            self.finalised_height = finalised_height
        if outbound_height is not None:
            self.outbound_height = outbound_height
        if keysign_metric is not None:
            self.keysign_metric = keysign_metric

    @property
    def observed_tx(self):
        """Gets the observed_tx of this TxResponse.  # noqa: E501


        :return: The observed_tx of this TxResponse.  # noqa: E501
        :rtype: ObservedTx
        """
        return self._observed_tx

    @observed_tx.setter
    def observed_tx(self, observed_tx):
        """Sets the observed_tx of this TxResponse.


        :param observed_tx: The observed_tx of this TxResponse.  # noqa: E501
        :type: ObservedTx
        """

        self._observed_tx = observed_tx

    @property
    def consensus_height(self):
        """Gets the consensus_height of this TxResponse.  # noqa: E501

        the thorchain height at which the inbound reached consensus  # noqa: E501

        :return: The consensus_height of this TxResponse.  # noqa: E501
        :rtype: int
        """
        return self._consensus_height

    @consensus_height.setter
    def consensus_height(self, consensus_height):
        """Sets the consensus_height of this TxResponse.

        the thorchain height at which the inbound reached consensus  # noqa: E501

        :param consensus_height: The consensus_height of this TxResponse.  # noqa: E501
        :type: int
        """

        self._consensus_height = consensus_height

    @property
    def finalised_height(self):
        """Gets the finalised_height of this TxResponse.  # noqa: E501

        the thorchain height at which the outbound was finalised  # noqa: E501

        :return: The finalised_height of this TxResponse.  # noqa: E501
        :rtype: int
        """
        return self._finalised_height

    @finalised_height.setter
    def finalised_height(self, finalised_height):
        """Sets the finalised_height of this TxResponse.

        the thorchain height at which the outbound was finalised  # noqa: E501

        :param finalised_height: The finalised_height of this TxResponse.  # noqa: E501
        :type: int
        """

        self._finalised_height = finalised_height

    @property
    def outbound_height(self):
        """Gets the outbound_height of this TxResponse.  # noqa: E501

        the thorchain height for which the outbound was scheduled  # noqa: E501

        :return: The outbound_height of this TxResponse.  # noqa: E501
        :rtype: int
        """
        return self._outbound_height

    @outbound_height.setter
    def outbound_height(self, outbound_height):
        """Sets the outbound_height of this TxResponse.

        the thorchain height for which the outbound was scheduled  # noqa: E501

        :param outbound_height: The outbound_height of this TxResponse.  # noqa: E501
        :type: int
        """

        self._outbound_height = outbound_height

    @property
    def keysign_metric(self):
        """Gets the keysign_metric of this TxResponse.  # noqa: E501


        :return: The keysign_metric of this TxResponse.  # noqa: E501
        :rtype: TssKeysignMetric
        """
        return self._keysign_metric

    @keysign_metric.setter
    def keysign_metric(self, keysign_metric):
        """Sets the keysign_metric of this TxResponse.


        :param keysign_metric: The keysign_metric of this TxResponse.  # noqa: E501
        :type: TssKeysignMetric
        """

        self._keysign_metric = keysign_metric

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
        if issubclass(TxResponse, dict):
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
        if not isinstance(other, TxResponse):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other

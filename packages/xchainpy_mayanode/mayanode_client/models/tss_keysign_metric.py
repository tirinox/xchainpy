# coding: utf-8

"""
    Mayanode API

    Mayanode REST API.  # noqa: E501

    OpenAPI spec version: 1.103.2
    Contact: devs@mayachain.org
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

import pprint
import re  # noqa: F401

import six

class TssKeysignMetric(object):
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
        'tx_id': 'str',
        'node_tss_times': 'list[TssMetric]'
    }

    attribute_map = {
        'tx_id': 'tx_id',
        'node_tss_times': 'node_tss_times'
    }

    def __init__(self, tx_id=None, node_tss_times=None):  # noqa: E501
        """TssKeysignMetric - a model defined in Swagger"""  # noqa: E501
        self._tx_id = None
        self._node_tss_times = None
        self.discriminator = None
        if tx_id is not None:
            self.tx_id = tx_id
        self.node_tss_times = node_tss_times

    @property
    def tx_id(self):
        """Gets the tx_id of this TssKeysignMetric.  # noqa: E501


        :return: The tx_id of this TssKeysignMetric.  # noqa: E501
        :rtype: str
        """
        return self._tx_id

    @tx_id.setter
    def tx_id(self, tx_id):
        """Sets the tx_id of this TssKeysignMetric.


        :param tx_id: The tx_id of this TssKeysignMetric.  # noqa: E501
        :type: str
        """

        self._tx_id = tx_id

    @property
    def node_tss_times(self):
        """Gets the node_tss_times of this TssKeysignMetric.  # noqa: E501


        :return: The node_tss_times of this TssKeysignMetric.  # noqa: E501
        :rtype: list[TssMetric]
        """
        return self._node_tss_times

    @node_tss_times.setter
    def node_tss_times(self, node_tss_times):
        """Sets the node_tss_times of this TssKeysignMetric.


        :param node_tss_times: The node_tss_times of this TssKeysignMetric.  # noqa: E501
        :type: list[TssMetric]
        """
        if node_tss_times is None:
            raise ValueError("Invalid value for `node_tss_times`, must not be `None`")  # noqa: E501

        self._node_tss_times = node_tss_times

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
        if issubclass(TssKeysignMetric, dict):
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
        if not isinstance(other, TssKeysignMetric):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other

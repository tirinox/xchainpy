# coding: utf-8

"""
    Mayanode API

    Mayanode REST API.  # noqa: E501

    OpenAPI spec version: 1.107.3
    Contact: devs@mayachain.org
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

import pprint
import re  # noqa: F401

import six

class MetricsResponse(object):
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
        'keygen': 'KeygenMetricsResponse',
        'keysign': 'KeysignMetrics'
    }

    attribute_map = {
        'keygen': 'keygen',
        'keysign': 'keysign'
    }

    def __init__(self, keygen=None, keysign=None):  # noqa: E501
        """MetricsResponse - a model defined in Swagger"""  # noqa: E501
        self._keygen = None
        self._keysign = None
        self.discriminator = None
        if keygen is not None:
            self.keygen = keygen
        if keysign is not None:
            self.keysign = keysign

    @property
    def keygen(self):
        """Gets the keygen of this MetricsResponse.  # noqa: E501


        :return: The keygen of this MetricsResponse.  # noqa: E501
        :rtype: KeygenMetricsResponse
        """
        return self._keygen

    @keygen.setter
    def keygen(self, keygen):
        """Sets the keygen of this MetricsResponse.


        :param keygen: The keygen of this MetricsResponse.  # noqa: E501
        :type: KeygenMetricsResponse
        """

        self._keygen = keygen

    @property
    def keysign(self):
        """Gets the keysign of this MetricsResponse.  # noqa: E501


        :return: The keysign of this MetricsResponse.  # noqa: E501
        :rtype: KeysignMetrics
        """
        return self._keysign

    @keysign.setter
    def keysign(self, keysign):
        """Sets the keysign of this MetricsResponse.


        :param keysign: The keysign of this MetricsResponse.  # noqa: E501
        :type: KeysignMetrics
        """

        self._keysign = keysign

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
        if issubclass(MetricsResponse, dict):
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
        if not isinstance(other, MetricsResponse):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other

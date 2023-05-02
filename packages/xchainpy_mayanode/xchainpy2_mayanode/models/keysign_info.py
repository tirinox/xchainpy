# coding: utf-8

"""
    Mayanode API

    Mayanode REST API.  # noqa: E501

    OpenAPI spec version: 1.103.3
    Contact: devs@mayachain.org
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

import pprint
import re  # noqa: F401

import six

class KeysignInfo(object):
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
        'height': 'int',
        'tx_array': 'list[TxOutItem]'
    }

    attribute_map = {
        'height': 'height',
        'tx_array': 'tx_array'
    }

    def __init__(self, height=None, tx_array=None):  # noqa: E501
        """KeysignInfo - a model defined in Swagger"""  # noqa: E501
        self._height = None
        self._tx_array = None
        self.discriminator = None
        if height is not None:
            self.height = height
        self.tx_array = tx_array

    @property
    def height(self):
        """Gets the height of this KeysignInfo.  # noqa: E501

        the block(s) in which a tx out item is scheduled to be signed and moved from the scheduled outbound queue to the outbound queue  # noqa: E501

        :return: The height of this KeysignInfo.  # noqa: E501
        :rtype: int
        """
        return self._height

    @height.setter
    def height(self, height):
        """Sets the height of this KeysignInfo.

        the block(s) in which a tx out item is scheduled to be signed and moved from the scheduled outbound queue to the outbound queue  # noqa: E501

        :param height: The height of this KeysignInfo.  # noqa: E501
        :type: int
        """

        self._height = height

    @property
    def tx_array(self):
        """Gets the tx_array of this KeysignInfo.  # noqa: E501


        :return: The tx_array of this KeysignInfo.  # noqa: E501
        :rtype: list[TxOutItem]
        """
        return self._tx_array

    @tx_array.setter
    def tx_array(self, tx_array):
        """Sets the tx_array of this KeysignInfo.


        :param tx_array: The tx_array of this KeysignInfo.  # noqa: E501
        :type: list[TxOutItem]
        """
        if tx_array is None:
            raise ValueError("Invalid value for `tx_array`, must not be `None`")  # noqa: E501

        self._tx_array = tx_array

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
        if issubclass(KeysignInfo, dict):
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
        if not isinstance(other, KeysignInfo):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other

# coding: utf-8

"""
    Thornode API

    Thornode REST API.  # noqa: E501

    OpenAPI spec version: 1.122.0
    Contact: devs@thorchain.org
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

import pprint
import re  # noqa: F401

import six

class TxSignersResponse(object):
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
        'tx': 'ObservedTx',
        'txs': 'list[ObservedTx]',
        'actions': 'list[TxOutItem]',
        'out_txs': 'list[Tx]',
        'consensus_height': 'int',
        'finalised_height': 'int',
        'updated_vault': 'bool',
        'reverted': 'bool',
        'outbound_height': 'int'
    }

    attribute_map = {
        'tx_id': 'tx_id',
        'tx': 'tx',
        'txs': 'txs',
        'actions': 'actions',
        'out_txs': 'out_txs',
        'consensus_height': 'consensus_height',
        'finalised_height': 'finalised_height',
        'updated_vault': 'updated_vault',
        'reverted': 'reverted',
        'outbound_height': 'outbound_height'
    }

    def __init__(self, tx_id=None, tx=None, txs=None, actions=None, out_txs=None, consensus_height=None, finalised_height=None, updated_vault=None, reverted=None, outbound_height=None):  # noqa: E501
        """TxSignersResponse - a model defined in Swagger"""  # noqa: E501
        self._tx_id = None
        self._tx = None
        self._txs = None
        self._actions = None
        self._out_txs = None
        self._consensus_height = None
        self._finalised_height = None
        self._updated_vault = None
        self._reverted = None
        self._outbound_height = None
        self.discriminator = None
        if tx_id is not None:
            self.tx_id = tx_id
        self.tx = tx
        self.txs = txs
        self.actions = actions
        self.out_txs = out_txs
        if consensus_height is not None:
            self.consensus_height = consensus_height
        if finalised_height is not None:
            self.finalised_height = finalised_height
        if updated_vault is not None:
            self.updated_vault = updated_vault
        if reverted is not None:
            self.reverted = reverted
        if outbound_height is not None:
            self.outbound_height = outbound_height

    @property
    def tx_id(self):
        """Gets the tx_id of this TxSignersResponse.  # noqa: E501


        :return: The tx_id of this TxSignersResponse.  # noqa: E501
        :rtype: str
        """
        return self._tx_id

    @tx_id.setter
    def tx_id(self, tx_id):
        """Sets the tx_id of this TxSignersResponse.


        :param tx_id: The tx_id of this TxSignersResponse.  # noqa: E501
        :type: str
        """

        self._tx_id = tx_id

    @property
    def tx(self):
        """Gets the tx of this TxSignersResponse.  # noqa: E501


        :return: The tx of this TxSignersResponse.  # noqa: E501
        :rtype: ObservedTx
        """
        return self._tx

    @tx.setter
    def tx(self, tx):
        """Sets the tx of this TxSignersResponse.


        :param tx: The tx of this TxSignersResponse.  # noqa: E501
        :type: ObservedTx
        """
        if tx is None:
            raise ValueError("Invalid value for `tx`, must not be `None`")  # noqa: E501

        self._tx = tx

    @property
    def txs(self):
        """Gets the txs of this TxSignersResponse.  # noqa: E501


        :return: The txs of this TxSignersResponse.  # noqa: E501
        :rtype: list[ObservedTx]
        """
        return self._txs

    @txs.setter
    def txs(self, txs):
        """Sets the txs of this TxSignersResponse.


        :param txs: The txs of this TxSignersResponse.  # noqa: E501
        :type: list[ObservedTx]
        """
        if txs is None:
            raise ValueError("Invalid value for `txs`, must not be `None`")  # noqa: E501

        self._txs = txs

    @property
    def actions(self):
        """Gets the actions of this TxSignersResponse.  # noqa: E501


        :return: The actions of this TxSignersResponse.  # noqa: E501
        :rtype: list[TxOutItem]
        """
        return self._actions

    @actions.setter
    def actions(self, actions):
        """Sets the actions of this TxSignersResponse.


        :param actions: The actions of this TxSignersResponse.  # noqa: E501
        :type: list[TxOutItem]
        """
        if actions is None:
            raise ValueError("Invalid value for `actions`, must not be `None`")  # noqa: E501

        self._actions = actions

    @property
    def out_txs(self):
        """Gets the out_txs of this TxSignersResponse.  # noqa: E501


        :return: The out_txs of this TxSignersResponse.  # noqa: E501
        :rtype: list[Tx]
        """
        return self._out_txs

    @out_txs.setter
    def out_txs(self, out_txs):
        """Sets the out_txs of this TxSignersResponse.


        :param out_txs: The out_txs of this TxSignersResponse.  # noqa: E501
        :type: list[Tx]
        """
        if out_txs is None:
            raise ValueError("Invalid value for `out_txs`, must not be `None`")  # noqa: E501

        self._out_txs = out_txs

    @property
    def consensus_height(self):
        """Gets the consensus_height of this TxSignersResponse.  # noqa: E501

        the thorchain height at which the inbound reached consensus  # noqa: E501

        :return: The consensus_height of this TxSignersResponse.  # noqa: E501
        :rtype: int
        """
        return self._consensus_height

    @consensus_height.setter
    def consensus_height(self, consensus_height):
        """Sets the consensus_height of this TxSignersResponse.

        the thorchain height at which the inbound reached consensus  # noqa: E501

        :param consensus_height: The consensus_height of this TxSignersResponse.  # noqa: E501
        :type: int
        """

        self._consensus_height = consensus_height

    @property
    def finalised_height(self):
        """Gets the finalised_height of this TxSignersResponse.  # noqa: E501

        the thorchain height at which the outbound was finalised  # noqa: E501

        :return: The finalised_height of this TxSignersResponse.  # noqa: E501
        :rtype: int
        """
        return self._finalised_height

    @finalised_height.setter
    def finalised_height(self, finalised_height):
        """Sets the finalised_height of this TxSignersResponse.

        the thorchain height at which the outbound was finalised  # noqa: E501

        :param finalised_height: The finalised_height of this TxSignersResponse.  # noqa: E501
        :type: int
        """

        self._finalised_height = finalised_height

    @property
    def updated_vault(self):
        """Gets the updated_vault of this TxSignersResponse.  # noqa: E501


        :return: The updated_vault of this TxSignersResponse.  # noqa: E501
        :rtype: bool
        """
        return self._updated_vault

    @updated_vault.setter
    def updated_vault(self, updated_vault):
        """Sets the updated_vault of this TxSignersResponse.


        :param updated_vault: The updated_vault of this TxSignersResponse.  # noqa: E501
        :type: bool
        """

        self._updated_vault = updated_vault

    @property
    def reverted(self):
        """Gets the reverted of this TxSignersResponse.  # noqa: E501


        :return: The reverted of this TxSignersResponse.  # noqa: E501
        :rtype: bool
        """
        return self._reverted

    @reverted.setter
    def reverted(self, reverted):
        """Sets the reverted of this TxSignersResponse.


        :param reverted: The reverted of this TxSignersResponse.  # noqa: E501
        :type: bool
        """

        self._reverted = reverted

    @property
    def outbound_height(self):
        """Gets the outbound_height of this TxSignersResponse.  # noqa: E501

        the thorchain height for which the outbound was scheduled  # noqa: E501

        :return: The outbound_height of this TxSignersResponse.  # noqa: E501
        :rtype: int
        """
        return self._outbound_height

    @outbound_height.setter
    def outbound_height(self, outbound_height):
        """Sets the outbound_height of this TxSignersResponse.

        the thorchain height for which the outbound was scheduled  # noqa: E501

        :param outbound_height: The outbound_height of this TxSignersResponse.  # noqa: E501
        :type: int
        """

        self._outbound_height = outbound_height

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
        if issubclass(TxSignersResponse, dict):
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
        if not isinstance(other, TxSignersResponse):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other

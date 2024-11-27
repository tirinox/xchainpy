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
        'router': 'str',
        'halted': 'bool',
        'global_trading_paused': 'bool',
        'chain_trading_paused': 'bool',
        'chain_lp_actions_paused': 'bool',
        'gas_rate': 'str',
        'gas_rate_units': 'str',
        'outbound_tx_size': 'str',
        'outbound_fee': 'str',
        'dust_threshold': 'str'
    }

    attribute_map = {
        'chain': 'chain',
        'pub_key': 'pub_key',
        'address': 'address',
        'router': 'router',
        'halted': 'halted',
        'global_trading_paused': 'global_trading_paused',
        'chain_trading_paused': 'chain_trading_paused',
        'chain_lp_actions_paused': 'chain_lp_actions_paused',
        'gas_rate': 'gas_rate',
        'gas_rate_units': 'gas_rate_units',
        'outbound_tx_size': 'outbound_tx_size',
        'outbound_fee': 'outbound_fee',
        'dust_threshold': 'dust_threshold'
    }

    def __init__(self, chain=None, pub_key=None, address=None, router=None, halted=None, global_trading_paused=None, chain_trading_paused=None, chain_lp_actions_paused=None, gas_rate=None, gas_rate_units=None, outbound_tx_size=None, outbound_fee=None, dust_threshold=None):  # noqa: E501
        """InboundAddress - a model defined in Swagger"""  # noqa: E501
        self._chain = None
        self._pub_key = None
        self._address = None
        self._router = None
        self._halted = None
        self._global_trading_paused = None
        self._chain_trading_paused = None
        self._chain_lp_actions_paused = None
        self._gas_rate = None
        self._gas_rate_units = None
        self._outbound_tx_size = None
        self._outbound_fee = None
        self._dust_threshold = None
        self.discriminator = None
        if chain is not None:
            self.chain = chain
        if pub_key is not None:
            self.pub_key = pub_key
        if address is not None:
            self.address = address
        if router is not None:
            self.router = router
        self.halted = halted
        if global_trading_paused is not None:
            self.global_trading_paused = global_trading_paused
        if chain_trading_paused is not None:
            self.chain_trading_paused = chain_trading_paused
        if chain_lp_actions_paused is not None:
            self.chain_lp_actions_paused = chain_lp_actions_paused
        if gas_rate is not None:
            self.gas_rate = gas_rate
        if gas_rate_units is not None:
            self.gas_rate_units = gas_rate_units
        if outbound_tx_size is not None:
            self.outbound_tx_size = outbound_tx_size
        if outbound_fee is not None:
            self.outbound_fee = outbound_fee
        if dust_threshold is not None:
            self.dust_threshold = dust_threshold

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

    @property
    def global_trading_paused(self):
        """Gets the global_trading_paused of this InboundAddress.  # noqa: E501

        Returns true if trading is paused globally  # noqa: E501

        :return: The global_trading_paused of this InboundAddress.  # noqa: E501
        :rtype: bool
        """
        return self._global_trading_paused

    @global_trading_paused.setter
    def global_trading_paused(self, global_trading_paused):
        """Sets the global_trading_paused of this InboundAddress.

        Returns true if trading is paused globally  # noqa: E501

        :param global_trading_paused: The global_trading_paused of this InboundAddress.  # noqa: E501
        :type: bool
        """

        self._global_trading_paused = global_trading_paused

    @property
    def chain_trading_paused(self):
        """Gets the chain_trading_paused of this InboundAddress.  # noqa: E501

        Returns true if trading is paused for this chain  # noqa: E501

        :return: The chain_trading_paused of this InboundAddress.  # noqa: E501
        :rtype: bool
        """
        return self._chain_trading_paused

    @chain_trading_paused.setter
    def chain_trading_paused(self, chain_trading_paused):
        """Sets the chain_trading_paused of this InboundAddress.

        Returns true if trading is paused for this chain  # noqa: E501

        :param chain_trading_paused: The chain_trading_paused of this InboundAddress.  # noqa: E501
        :type: bool
        """

        self._chain_trading_paused = chain_trading_paused

    @property
    def chain_lp_actions_paused(self):
        """Gets the chain_lp_actions_paused of this InboundAddress.  # noqa: E501

        Returns true if LP actions are paused for this chain  # noqa: E501

        :return: The chain_lp_actions_paused of this InboundAddress.  # noqa: E501
        :rtype: bool
        """
        return self._chain_lp_actions_paused

    @chain_lp_actions_paused.setter
    def chain_lp_actions_paused(self, chain_lp_actions_paused):
        """Sets the chain_lp_actions_paused of this InboundAddress.

        Returns true if LP actions are paused for this chain  # noqa: E501

        :param chain_lp_actions_paused: The chain_lp_actions_paused of this InboundAddress.  # noqa: E501
        :type: bool
        """

        self._chain_lp_actions_paused = chain_lp_actions_paused

    @property
    def gas_rate(self):
        """Gets the gas_rate of this InboundAddress.  # noqa: E501

        The minimum fee rate used by vaults to send outbound TXs. The actual fee rate may be higher. For EVM chains this is returned in gwei (1e9).  # noqa: E501

        :return: The gas_rate of this InboundAddress.  # noqa: E501
        :rtype: str
        """
        return self._gas_rate

    @gas_rate.setter
    def gas_rate(self, gas_rate):
        """Sets the gas_rate of this InboundAddress.

        The minimum fee rate used by vaults to send outbound TXs. The actual fee rate may be higher. For EVM chains this is returned in gwei (1e9).  # noqa: E501

        :param gas_rate: The gas_rate of this InboundAddress.  # noqa: E501
        :type: str
        """

        self._gas_rate = gas_rate

    @property
    def gas_rate_units(self):
        """Gets the gas_rate_units of this InboundAddress.  # noqa: E501

        Units of the gas_rate.  # noqa: E501

        :return: The gas_rate_units of this InboundAddress.  # noqa: E501
        :rtype: str
        """
        return self._gas_rate_units

    @gas_rate_units.setter
    def gas_rate_units(self, gas_rate_units):
        """Sets the gas_rate_units of this InboundAddress.

        Units of the gas_rate.  # noqa: E501

        :param gas_rate_units: The gas_rate_units of this InboundAddress.  # noqa: E501
        :type: str
        """

        self._gas_rate_units = gas_rate_units

    @property
    def outbound_tx_size(self):
        """Gets the outbound_tx_size of this InboundAddress.  # noqa: E501

        Avg size of outbound TXs on each chain. For UTXO chains it may be larger than average, as it takes into account vault consolidation txs, which can have many vouts  # noqa: E501

        :return: The outbound_tx_size of this InboundAddress.  # noqa: E501
        :rtype: str
        """
        return self._outbound_tx_size

    @outbound_tx_size.setter
    def outbound_tx_size(self, outbound_tx_size):
        """Sets the outbound_tx_size of this InboundAddress.

        Avg size of outbound TXs on each chain. For UTXO chains it may be larger than average, as it takes into account vault consolidation txs, which can have many vouts  # noqa: E501

        :param outbound_tx_size: The outbound_tx_size of this InboundAddress.  # noqa: E501
        :type: str
        """

        self._outbound_tx_size = outbound_tx_size

    @property
    def outbound_fee(self):
        """Gets the outbound_fee of this InboundAddress.  # noqa: E501

        The total outbound fee charged to the user for outbound txs in the gas asset of the chain.  # noqa: E501

        :return: The outbound_fee of this InboundAddress.  # noqa: E501
        :rtype: str
        """
        return self._outbound_fee

    @outbound_fee.setter
    def outbound_fee(self, outbound_fee):
        """Sets the outbound_fee of this InboundAddress.

        The total outbound fee charged to the user for outbound txs in the gas asset of the chain.  # noqa: E501

        :param outbound_fee: The outbound_fee of this InboundAddress.  # noqa: E501
        :type: str
        """

        self._outbound_fee = outbound_fee

    @property
    def dust_threshold(self):
        """Gets the dust_threshold of this InboundAddress.  # noqa: E501

        Defines the minimum transaction size for the chain in base units (sats, wei, uatom). Transactions with asset amounts lower than the dust_threshold are ignored.  # noqa: E501

        :return: The dust_threshold of this InboundAddress.  # noqa: E501
        :rtype: str
        """
        return self._dust_threshold

    @dust_threshold.setter
    def dust_threshold(self, dust_threshold):
        """Sets the dust_threshold of this InboundAddress.

        Defines the minimum transaction size for the chain in base units (sats, wei, uatom). Transactions with asset amounts lower than the dust_threshold are ignored.  # noqa: E501

        :param dust_threshold: The dust_threshold of this InboundAddress.  # noqa: E501
        :type: str
        """

        self._dust_threshold = dust_threshold

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

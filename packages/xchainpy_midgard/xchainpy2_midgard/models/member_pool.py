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

class MemberPool(object):
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
        'asset_added': 'str',
        'asset_address': 'str',
        'asset_deposit': 'str',
        'asset_pending': 'str',
        'asset_withdrawn': 'str',
        'date_first_added': 'str',
        'date_last_added': 'str',
        'liquidity_units': 'str',
        'pool': 'str',
        'rune_added': 'str',
        'rune_address': 'str',
        'rune_deposit': 'str',
        'rune_pending': 'str',
        'rune_withdrawn': 'str'
    }

    attribute_map = {
        'asset_added': 'assetAdded',
        'asset_address': 'assetAddress',
        'asset_deposit': 'assetDeposit',
        'asset_pending': 'assetPending',
        'asset_withdrawn': 'assetWithdrawn',
        'date_first_added': 'dateFirstAdded',
        'date_last_added': 'dateLastAdded',
        'liquidity_units': 'liquidityUnits',
        'pool': 'pool',
        'rune_added': 'runeAdded',
        'rune_address': 'runeAddress',
        'rune_deposit': 'runeDeposit',
        'rune_pending': 'runePending',
        'rune_withdrawn': 'runeWithdrawn'
    }

    def __init__(self, asset_added=None, asset_address=None, asset_deposit=None, asset_pending=None, asset_withdrawn=None, date_first_added=None, date_last_added=None, liquidity_units=None, pool=None, rune_added=None, rune_address=None, rune_deposit=None, rune_pending=None, rune_withdrawn=None):  # noqa: E501
        """MemberPool - a model defined in Swagger"""  # noqa: E501
        self._asset_added = None
        self._asset_address = None
        self._asset_deposit = None
        self._asset_pending = None
        self._asset_withdrawn = None
        self._date_first_added = None
        self._date_last_added = None
        self._liquidity_units = None
        self._pool = None
        self._rune_added = None
        self._rune_address = None
        self._rune_deposit = None
        self._rune_pending = None
        self._rune_withdrawn = None
        self.discriminator = None
        self.asset_added = asset_added
        self.asset_address = asset_address
        self.asset_deposit = asset_deposit
        self.asset_pending = asset_pending
        self.asset_withdrawn = asset_withdrawn
        self.date_first_added = date_first_added
        self.date_last_added = date_last_added
        self.liquidity_units = liquidity_units
        self.pool = pool
        self.rune_added = rune_added
        self.rune_address = rune_address
        self.rune_deposit = rune_deposit
        self.rune_pending = rune_pending
        self.rune_withdrawn = rune_withdrawn

    @property
    def asset_added(self):
        """Gets the asset_added of this MemberPool.  # noqa: E501

        Int64(e8), total asset added to the pool by member  # noqa: E501

        :return: The asset_added of this MemberPool.  # noqa: E501
        :rtype: str
        """
        return self._asset_added

    @asset_added.setter
    def asset_added(self, asset_added):
        """Sets the asset_added of this MemberPool.

        Int64(e8), total asset added to the pool by member  # noqa: E501

        :param asset_added: The asset_added of this MemberPool.  # noqa: E501
        :type: str
        """
        if asset_added is None:
            raise ValueError("Invalid value for `asset_added`, must not be `None`")  # noqa: E501

        self._asset_added = asset_added

    @property
    def asset_address(self):
        """Gets the asset_address of this MemberPool.  # noqa: E501

        asset address used by the member  # noqa: E501

        :return: The asset_address of this MemberPool.  # noqa: E501
        :rtype: str
        """
        return self._asset_address

    @asset_address.setter
    def asset_address(self, asset_address):
        """Sets the asset_address of this MemberPool.

        asset address used by the member  # noqa: E501

        :param asset_address: The asset_address of this MemberPool.  # noqa: E501
        :type: str
        """
        if asset_address is None:
            raise ValueError("Invalid value for `asset_address`, must not be `None`")  # noqa: E501

        self._asset_address = asset_address

    @property
    def asset_deposit(self):
        """Gets the asset_deposit of this MemberPool.  # noqa: E501

        Int64(e8), total asset that is currently deposited to the pool by member. This field is same as the `asset_deposit_value` field in thornode. Mainly can be used  for tracking, mainly Growth Percentage   # noqa: E501

        :return: The asset_deposit of this MemberPool.  # noqa: E501
        :rtype: str
        """
        return self._asset_deposit

    @asset_deposit.setter
    def asset_deposit(self, asset_deposit):
        """Sets the asset_deposit of this MemberPool.

        Int64(e8), total asset that is currently deposited to the pool by member. This field is same as the `asset_deposit_value` field in thornode. Mainly can be used  for tracking, mainly Growth Percentage   # noqa: E501

        :param asset_deposit: The asset_deposit of this MemberPool.  # noqa: E501
        :type: str
        """
        if asset_deposit is None:
            raise ValueError("Invalid value for `asset_deposit`, must not be `None`")  # noqa: E501

        self._asset_deposit = asset_deposit

    @property
    def asset_pending(self):
        """Gets the asset_pending of this MemberPool.  # noqa: E501

        Int64(e8), asset sent but not added yet, it will be added when the rune pair arrives   # noqa: E501

        :return: The asset_pending of this MemberPool.  # noqa: E501
        :rtype: str
        """
        return self._asset_pending

    @asset_pending.setter
    def asset_pending(self, asset_pending):
        """Sets the asset_pending of this MemberPool.

        Int64(e8), asset sent but not added yet, it will be added when the rune pair arrives   # noqa: E501

        :param asset_pending: The asset_pending of this MemberPool.  # noqa: E501
        :type: str
        """
        if asset_pending is None:
            raise ValueError("Invalid value for `asset_pending`, must not be `None`")  # noqa: E501

        self._asset_pending = asset_pending

    @property
    def asset_withdrawn(self):
        """Gets the asset_withdrawn of this MemberPool.  # noqa: E501

        Int64(e8), total asset withdrawn from the pool by member  # noqa: E501

        :return: The asset_withdrawn of this MemberPool.  # noqa: E501
        :rtype: str
        """
        return self._asset_withdrawn

    @asset_withdrawn.setter
    def asset_withdrawn(self, asset_withdrawn):
        """Sets the asset_withdrawn of this MemberPool.

        Int64(e8), total asset withdrawn from the pool by member  # noqa: E501

        :param asset_withdrawn: The asset_withdrawn of this MemberPool.  # noqa: E501
        :type: str
        """
        if asset_withdrawn is None:
            raise ValueError("Invalid value for `asset_withdrawn`, must not be `None`")  # noqa: E501

        self._asset_withdrawn = asset_withdrawn

    @property
    def date_first_added(self):
        """Gets the date_first_added of this MemberPool.  # noqa: E501

        Int64, Unix timestamp for the first time member deposited into the pool  # noqa: E501

        :return: The date_first_added of this MemberPool.  # noqa: E501
        :rtype: str
        """
        return self._date_first_added

    @date_first_added.setter
    def date_first_added(self, date_first_added):
        """Sets the date_first_added of this MemberPool.

        Int64, Unix timestamp for the first time member deposited into the pool  # noqa: E501

        :param date_first_added: The date_first_added of this MemberPool.  # noqa: E501
        :type: str
        """
        if date_first_added is None:
            raise ValueError("Invalid value for `date_first_added`, must not be `None`")  # noqa: E501

        self._date_first_added = date_first_added

    @property
    def date_last_added(self):
        """Gets the date_last_added of this MemberPool.  # noqa: E501

        Int64, Unix timestamp for the last time member deposited into the pool  # noqa: E501

        :return: The date_last_added of this MemberPool.  # noqa: E501
        :rtype: str
        """
        return self._date_last_added

    @date_last_added.setter
    def date_last_added(self, date_last_added):
        """Sets the date_last_added of this MemberPool.

        Int64, Unix timestamp for the last time member deposited into the pool  # noqa: E501

        :param date_last_added: The date_last_added of this MemberPool.  # noqa: E501
        :type: str
        """
        if date_last_added is None:
            raise ValueError("Invalid value for `date_last_added`, must not be `None`")  # noqa: E501

        self._date_last_added = date_last_added

    @property
    def liquidity_units(self):
        """Gets the liquidity_units of this MemberPool.  # noqa: E501

        Int64, pool liquidity units that belong the the member  # noqa: E501

        :return: The liquidity_units of this MemberPool.  # noqa: E501
        :rtype: str
        """
        return self._liquidity_units

    @liquidity_units.setter
    def liquidity_units(self, liquidity_units):
        """Sets the liquidity_units of this MemberPool.

        Int64, pool liquidity units that belong the the member  # noqa: E501

        :param liquidity_units: The liquidity_units of this MemberPool.  # noqa: E501
        :type: str
        """
        if liquidity_units is None:
            raise ValueError("Invalid value for `liquidity_units`, must not be `None`")  # noqa: E501

        self._liquidity_units = liquidity_units

    @property
    def pool(self):
        """Gets the pool of this MemberPool.  # noqa: E501

        Pool rest of the data refers to  # noqa: E501

        :return: The pool of this MemberPool.  # noqa: E501
        :rtype: str
        """
        return self._pool

    @pool.setter
    def pool(self, pool):
        """Sets the pool of this MemberPool.

        Pool rest of the data refers to  # noqa: E501

        :param pool: The pool of this MemberPool.  # noqa: E501
        :type: str
        """
        if pool is None:
            raise ValueError("Invalid value for `pool`, must not be `None`")  # noqa: E501

        self._pool = pool

    @property
    def rune_added(self):
        """Gets the rune_added of this MemberPool.  # noqa: E501

        Int64(e8), total Rune added to the pool by member  # noqa: E501

        :return: The rune_added of this MemberPool.  # noqa: E501
        :rtype: str
        """
        return self._rune_added

    @rune_added.setter
    def rune_added(self, rune_added):
        """Sets the rune_added of this MemberPool.

        Int64(e8), total Rune added to the pool by member  # noqa: E501

        :param rune_added: The rune_added of this MemberPool.  # noqa: E501
        :type: str
        """
        if rune_added is None:
            raise ValueError("Invalid value for `rune_added`, must not be `None`")  # noqa: E501

        self._rune_added = rune_added

    @property
    def rune_address(self):
        """Gets the rune_address of this MemberPool.  # noqa: E501

        Rune address used by the member  # noqa: E501

        :return: The rune_address of this MemberPool.  # noqa: E501
        :rtype: str
        """
        return self._rune_address

    @rune_address.setter
    def rune_address(self, rune_address):
        """Sets the rune_address of this MemberPool.

        Rune address used by the member  # noqa: E501

        :param rune_address: The rune_address of this MemberPool.  # noqa: E501
        :type: str
        """
        if rune_address is None:
            raise ValueError("Invalid value for `rune_address`, must not be `None`")  # noqa: E501

        self._rune_address = rune_address

    @property
    def rune_deposit(self):
        """Gets the rune_deposit of this MemberPool.  # noqa: E501

        Int64(e8), total Rune that is currently deposited to the pool by member. This field is same as the `rune_deposit_value` field in thornode. Mainly can be used  for tracking, mainly Growth Percentage   # noqa: E501

        :return: The rune_deposit of this MemberPool.  # noqa: E501
        :rtype: str
        """
        return self._rune_deposit

    @rune_deposit.setter
    def rune_deposit(self, rune_deposit):
        """Sets the rune_deposit of this MemberPool.

        Int64(e8), total Rune that is currently deposited to the pool by member. This field is same as the `rune_deposit_value` field in thornode. Mainly can be used  for tracking, mainly Growth Percentage   # noqa: E501

        :param rune_deposit: The rune_deposit of this MemberPool.  # noqa: E501
        :type: str
        """
        if rune_deposit is None:
            raise ValueError("Invalid value for `rune_deposit`, must not be `None`")  # noqa: E501

        self._rune_deposit = rune_deposit

    @property
    def rune_pending(self):
        """Gets the rune_pending of this MemberPool.  # noqa: E501

        Int64(e8), Rune sent but not added yet, it will be added when the asset pair arrives   # noqa: E501

        :return: The rune_pending of this MemberPool.  # noqa: E501
        :rtype: str
        """
        return self._rune_pending

    @rune_pending.setter
    def rune_pending(self, rune_pending):
        """Sets the rune_pending of this MemberPool.

        Int64(e8), Rune sent but not added yet, it will be added when the asset pair arrives   # noqa: E501

        :param rune_pending: The rune_pending of this MemberPool.  # noqa: E501
        :type: str
        """
        if rune_pending is None:
            raise ValueError("Invalid value for `rune_pending`, must not be `None`")  # noqa: E501

        self._rune_pending = rune_pending

    @property
    def rune_withdrawn(self):
        """Gets the rune_withdrawn of this MemberPool.  # noqa: E501

        Int64(e8), total Rune withdrawn from the pool by member  # noqa: E501

        :return: The rune_withdrawn of this MemberPool.  # noqa: E501
        :rtype: str
        """
        return self._rune_withdrawn

    @rune_withdrawn.setter
    def rune_withdrawn(self, rune_withdrawn):
        """Sets the rune_withdrawn of this MemberPool.

        Int64(e8), total Rune withdrawn from the pool by member  # noqa: E501

        :param rune_withdrawn: The rune_withdrawn of this MemberPool.  # noqa: E501
        :type: str
        """
        if rune_withdrawn is None:
            raise ValueError("Invalid value for `rune_withdrawn`, must not be `None`")  # noqa: E501

        self._rune_withdrawn = rune_withdrawn

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
        if issubclass(MemberPool, dict):
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
        if not isinstance(other, MemberPool):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other

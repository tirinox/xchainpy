XChainPy2 THORChain query
=========================

XChainPy2 THORChain query is a Python library for querying swap quotes, pools, and other data from THORChain.

Main Query Module
-----------------

.. automodule:: xchainpy2_thorchain_query.query

Cache for frequently used data
------------------------------

.. automodule:: xchainpy2_thorchain_query.cache

Transaction Status Checker
--------------------------

.. automodule:: xchainpy2_thorchain_query.check_tx

Constants
---------

.. automodule:: xchainpy2_thorchain_query.const

Models
------

.. automodule:: xchainpy2_thorchain_query.models

Midgard interface
-----------------

.. automodule:: xchainpy2_thorchain_query.midgard

THORNode interface
------------------

.. automodule:: xchainpy2_thorchain_query.thornode

Public API URLS
---------------

.. automodule:: xchainpy2_thorchain_query.env

Swap arithmetic
---------------

.. automodule:: xchainpy2_thorchain_query.swap

Liquidity math
--------------

.. automodule:: xchainpy2_thorchain_query.liquidity

Patch clients
-------------

This module is used to patch the API clients with the following features:

1. `x-client-id` header
2. Retry mechanism
3. Backup hosts

.. automodule:: xchainpy2_thorchain_query.patch_clients

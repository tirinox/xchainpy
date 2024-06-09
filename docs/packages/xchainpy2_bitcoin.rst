XChainPy2 Bitcoin client
========================

This package provides a client to interact with Bitcoin blockchain.
It supports the following features:

- Get address, private key and public key
- Get balance of an address
- Get transaction details
- Get transactions by address
- Get unspent transaction outputs
- Get transaction fee
- Prepare and send transaction

The underlying implementation uses `bitcoinlib` library. https://bitcoinlib.readthedocs.io/en/latest/

We use the function `accumulative` from `coinselect` ported to python to calculate the fee and select the inputs and outputs of the transaction.
See: https://github.com/bitcoinjs/coinselect

Quick Start
-----------

This example shows how to create a BTC client and get the balance of an address. After that, it shows how to send a transaction
between two addresses (0 index and 1 index of the mnemonic phrase).

.. literalinclude:: ../examples/btc_ex.py
   :language: python

BTC Client class
----------------

.. automodule:: xchainpy2_bitcoin.btc_client

Constants
---------

.. automodule:: xchainpy2_bitcoin.const

.. py:data:: xchainpy2_bitcoin.utils.AssetTestBTC

    Testnet BTC asset

TX preparation functions
------------------------

.. automodule:: xchainpy2_bitcoin.tx_prepare

Bitcoin Utils
-------------

.. automodule:: xchainpy2_bitcoin.utils

Accumulative inputs selection
-----------------------------

.. automodule:: xchainpy2_bitcoin.accumulative

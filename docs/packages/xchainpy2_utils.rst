XChainPy2 Utils, Amount, Asset
==============================

Chains
------

.. automodule:: xchainpy2_utils.chain
    :members:
    :undoc-members:
    :show-inheritance:


Constants
---------

.. automodule:: xchainpy2_utils.consts
    :members:
    :undoc-members:
    :show-inheritance:

Assets
------

The class **Asset** is a data class that represents an asset identifier in the XChainPy2 ecosystem.
It is widely used in the XChainPy2 packages.

.. automodule:: xchainpy2_utils.asset
    :members:
    :undoc-members:
    :show-inheritance:

Amounts
-------

The class **Amount** is a data class that represents an amount in the XChainPy2 ecosystem.
**CryptoAmount** represents an amount of a cryptocurrency. Basically, it is a combination of an asset and a value.

.. note::

    For classes **Amount** and **CryptoAmount**, there are available math operations like addition, subtraction, multiplication, and division.


.. literalinclude:: ../examples/crypto_amount_arithmetics.py
    :language: python
    :linenos:



.. warning::

    You can not add CryptoAmount with different assets.


.. automodule:: xchainpy2_utils.amount
    :members:
    :undoc-members:
    :show-inheritance:

Format utils
------------

.. automodule:: xchainpy2_utils.format
    :members:
    :undoc-members:
    :show-inheritance:

Date utils
----------

.. automodule:: xchainpy2_utils.dates
    :members:
    :undoc-members:
    :show-inheritance:

Decimal constants
-----------------

.. automodule:: xchainpy2_utils.decimals
    :members:
    :undoc-members:
    :show-inheritance:

Math utils
----------

.. automodule:: xchainpy2_utils.math
    :members:
    :undoc-members:
    :show-inheritance:

Sequence utils
--------------

.. automodule:: xchainpy2_utils.seqs
    :members:
    :undoc-members:
    :show-inheritance:

Version utils
-------------

.. automodule:: xchainpy2_utils.versions
    :members:
    :undoc-members:
    :show-inheritance:

Testing utils
-------------

.. automodule:: xchainpy2_utils.testing_utils
    :members:
    :undoc-members:
    :show-inheritance:

Other utils
------------

.. automodule:: xchainpy2_utils.util
    :members:
    :undoc-members:
    :show-inheritance:

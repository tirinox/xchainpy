Installation
============

The XChainPy2 library is available on `PyPi <https://pypi.org/user/tirinox/>`_. You can install it using pip.
Depending on your goals, you can install different sets of packages.
Some packages entail other packages as dependencies.

Scenario 1
----------

Utilizing separate clients of blockchains. Pick the needed blockchain clients from the list below.

.. code-block:: bash

    -- UTXO chains
    python -m pip install xchainpy2_bitcoin
    python -m pip install xchainpy2_bitcoincash
    python -m pip install xchainpy2_litecoin
    python -m pip install xchainpy2_doge

    -- EVM based chais
    python -m pip install xchainpy2_ethereum
    python -m pip install xchainpy2_bsc
    python -m pip install xchainpy2_avalanche
    python -m pip install xchainpy2_arbitrum

    -- Cosmos based chains
    python -m pip install xchainpy2_cosmos
    python -m pip install xchainpy2_thorchain
    python -m pip install xchainpy2_mayachain

Scenario 2
----------

In order to interact with the THORChain protocol.

First, install the needed blockchain clients (see Scenario 1).

Second, install the THORChain protocol client and THORChain AMM interface package.

.. code-block:: bash

    python -m pip install xchainpy2_thorchain_amm


.. note::
   **xchainpy2_thorchain_amm** package is dependent on **xchainpy2_thorchain**, **xchainpy2_thornode**, **xchainpy2_midgard**, **xchainpy2_thorchain_query** packages. So you don't need to install them separately. They will be installed automatically when you install the **xchainpy2_thorchain_amm** package.


Scenario 3
----------

Analyzing THORChain network operation, collecting analytics, monitoring and so on.


.. code-block:: bash

   python -m pip install xchainpy2_thornode xchainpy2_midgard xchainpy_thorchain_query

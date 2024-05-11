Installation
============

The XChainPy2 library is available on `PyPi <https://pypi.org/user/tirinox/>`_. You can install it using **pip**.
Depending on your goals, you can install different sets of packages.
Some packages entail other packages as dependencies.

Scenario 1: chain clients
--------------------------

In case you need some blockchain clients without performing cross-chain DeFi activities,
then just pick and install the needed blockchain clients from the list below.

Each of the following packages is self-sufficient for simple fund transfers.

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

Scenario 2: AMM and DeFi
------------------------

In order to interact with the THORChain protocol.

First, install the needed blockchain clients (see Scenario 1).

Second, install the THORChain protocol client and THORChain AMM interface package.

.. code-block:: bash

    python -m pip install xchainpy2_thorchain_amm


.. note::
   **xchainpy2_thorchain_amm** package is dependent on **xchainpy2_thorchain**, **xchainpy2_thornode**, **xchainpy2_midgard**, **xchainpy2_thorchain_query** packages. So you don't need to install them separately. They will be installed automatically when you install the **xchainpy2_thorchain_amm** package.


Scenario 3: analysis and monitoring
-----------------------------------

You will fit this scenario if your task is to analyze THORChain operation, data collection or monitoring, without committing transactions.

.. code-block:: bash

   python -m pip install xchainpy_thorchain_query

.. note::
    **xchainpy2_thorchain_query** package is dependent on **xchainpy2_thorchain** and **xchainpy2_midgard** packages. So you don't need to install them separately.


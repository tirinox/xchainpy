# XChainPy2

XChainPy2 is a library for Python with a common interface for multiple blockchains, built for simple and fast
integration for wallets and more.

A free interpretation of [XChainJS](https://xchainjs.org/).

## Packages

The library is divided into several packages. You can only use the ones you need.

#### 1. xchainpy_utils

Utility helpers for XChainPy2 components. Asset, amount, formatting, math and more.

#### 2. xchainpy_crypto

Keystore management and crypto utilities.

#### 3. xchainpy_client

Base blockchain client interface. Used by all blockchain clients.
It allows you to read your balance, query transactions, broadcast your transactions to the network.

#### 4. xchainpy_midgard

Client for the THORChain Midgard API. Documentation: https://midgard.ninerealms.com/v2/doc

It is automatically generated from the Swagger specification. Just a basic client with asyncio support, does not contain any special features like retries or fallbacks.

#### 5. xchainpy_thornode

Client for the THORNode API. Documentation: https://thornode.ninerealms.com/thorchain/doc

It is automatically generated from the Swagger specification. Just a basic client with asyncio support.

#### 6. xchainpy_mayanode

Client for the MayaNode API. Documentation: https://mayanode.mayachain.info/mayachain/doc

It is automatically generated from the Swagger specification. Just a basic client with asyncio support.

#### 7. xchainpy_cosmos

Cosmos chain client. Based on the xchainpy_client interface.

#### 8. xchainpy_thorchain

THORChain chain client. Based on the xchainpy_cosmos.
Supports both native transfer transactions and deposit transactions.

#### 9. xchainpy_thorchain_query

High level interface to Midgard and THORNode/MayaNode. It has many useful features like retry, fallback servers, caching and more. Liquidity math functions are included. 

#### 10. xchainpy_utxo_providers

UTXO providers for Bitcoin and other UTXO based chains. Currently, supports Haskoin, Sochain and Blockcypher APIs.

#### 11. xchainpy_thorchain_amm

High level interface to THORChain Automated Market Maker (AMM). It includes a wallet class, swap, deposit, withdraw, pool status and more. *(Work in progress)*

#### 12. xchainpy_bitcoin
*Development has not yet begun*


## Installation

The project is still under active development and is not ready for production use.
It is not yet available on PyPi.
For now, you can install the packages manually.

### 1. In order to run the code samples

First, install the XChainPy2 packages. For example, for running THORChain examples, run the following commands.

```
python3 -m pip install --editable packages/xchainpy_crypto
python3 -m pip install --editable packages/xchainpy_utils
python3 -m pip install --editable packages/xchainpy_client
python3 -m pip install --editable packages/xchainpy_cosmos
python3 -m pip install --editable packages/xchainpy_thorchain
```

Or just `make tc_env` which does the same.

Then you can have some fun by running code samples inside the `./examples` folder.

### 2. In order to leverage the library in your project

You can install the packages manually from GitHub with the following commands.

Utils:

`pip install "git+https://github.com/tirinox/xchainpy.git@develop#egg=xchainpy2_utils&subdirectory=packages/xchainpy_utils"`

Crypto utils:

`pip install "git+https://github.com/tirinox/xchainpy.git@develop#egg=xchainpy2_crypto&subdirectory=packages/xchainpy_crypto"`

Base clients:

`pip install "git+https://github.com/tirinox/xchainpy.git@develop#egg=xchainpy_client&subdirectory=packages/xchainpy_client"`

Cosmos:

`pip install "git+https://github.com/tirinox/xchainpy.git@develop#egg=xchainpy_cosmos&subdirectory=packages/xchainpy_cosmos"`

THORChain:

`pip install "git+https://github.com/tirinox/xchainpy.git@develop#egg=xchainpy_thorchain&subdirectory=packages/xchainpy_thorchain"`

THORNode:

`pip install "git+https://github.com/tirinox/xchainpy.git@develop#egg=xchainpy_thornode&subdirectory=packages/xchainpy_thornode"`

MayaNode:

`pip install "git+https://github.com/tirinox/xchainpy.git@develop#egg=xchainpy_mayanode&subdirectory=packages/xchainpy_mayanode"`

Midgard:
`pip install "git+https://github.com/tirinox/xchainpy.git@develop#egg=xchainpy_mayanode&subdirectory=packages/xchainpy_midgard"`

UTXO Providers:
`pip install "git+https://github.com/tirinox/xchainpy.git@develop#egg=xchainpy_utxo_providers&subdirectory=packages/xchainpy_utxo_providers"`

## Test

First install the dependencies:

`make dev_tools`

Then run the tests:

`make test`

## To Do

Mandatory items.

- [x] Utils package
- [x] Crypto utils package
- [x] Base blockchain client package
- [x] THORChain package
- [x] Cosmos package
- [x] UTXO providers (Haskoin, Sochain, Blockcypher)
- [ ] Tests for the Query Package
- [ ] Examples for Query Package
- [ ] Mayachain client
- [ ] Bitcoin client
- [ ] Ethereum client
- [ ] Other UTXO clients
- [ ] Other EVM clients
- [ ] Loans

The list goes on.

### Innovation

- [ ] Block-timestamp conversion
- [v] Retry/fallback for the generated Midgard/THORNode clients
- [ ] Wait for the tx to be completed
- [ ] Utils for DEX aggregators

The list goes on.
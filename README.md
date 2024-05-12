# XChainPy2

XChainPy2 is a library of Python packages that provides a common interface for multiple blockchains, built for simple and fast
integration for wallets and more. It enables you to interact with THORChain and MayaChain DeFi protocols, as well as other blockchains like Bitcoin, Ethereum, Binance Smart Chain, and more. 
It is a free-style interpretation of [XChainJS](https://xchainjs.org/).

_⚠️WARNING: In Python you do not control memory. Regardless of how secrets are passed to the underlying lib, it still was an object in python before. It will linger in the heap for some time even after going out of scope. It is also impossible to mlock() secrets, your private keys may end up on disk in swap. Use with caution!_

Documentation is available here: https://xchainpy2.readthedocs.io/en/latest/

## Packages

The library is divided into several packages. You can only use the ones you need.

#### 1. xchainpy_utils

Utility helpers for XChainPy2 components. Asset, amount, formatting, math and more.

#### 2. xchainpy_crypto

Keystore management and crypto utilities.

#### 3. xchainpy_client

This is a base blockchain client interface. Used by all specific blockchain clients.
Each blockchain client allows you to read your balance, query transactions, broadcast your transactions to the network.
Normally, you would not use this package directly, but use the specific blockchain client packages.

#### 4. xchainpy_midgard

Client for the THORChain Midgard API. Documentation: https://midgard.ninerealms.com/v2/doc

It is automatically generated from the Swagger specification. Just a basic client with asyncio support, does not contain any special features like retries or fallbacks.
Please use the *xchainpy_thorchain_query* package for a more advanced interface.

#### 5. xchainpy_thornode

Client for the THORNode API. Documentation: https://thornode.ninerealms.com/thorchain/doc

It is automatically generated from the Swagger specification. Just a basic client with asyncio support.
Please use the *xchainpy_thorchain_query* package for a more advanced interface.

#### 6. xchainpy_mayanode

Client for the MayaNode API. Documentation: https://mayanode.mayachain.info/mayachain/doc

It is automatically generated from the Swagger specification. Just a basic client with asyncio support.

#### 7. xchainpy_cosmos

Cosmos chain client. Based on the *xchainpy_client* interface.

#### 8. xchainpy_thorchain

THORChain client. Based on the *xchainpy_cosmos*.
Supports both native transfer transactions and deposit transactions.

#### 9. xchainpy_thorchain_query

High level interface to Midgard and THORNode/MayaNode. It has many useful features like retry, fallback servers, caching and more. Liquidity math functions are included. 

#### 10. xchainpy_utxo_providers

UTXO providers for Bitcoin and other UTXO based chains. Currently, supports Haskoin, Sochain and Blockcypher APIs.

#### 11. xchainpy_thorchain_amm

High level interface to THORChain Automated Market Maker (AMM). It includes a wallet class, swap, deposit, withdraw, pool status and more. *(Work in progress)*

#### 12. xchainpy_bitcoin

Bitcoin client.

#### 13. xchainpy_ethereum

Ethereum client.

#### 14. xchainpy_binance

Binance Chain client. Deprecated. See: https://www.bnbchain.org/en/blog/bep2-bep8-asset-sunset-announcement

#### 15. xchainpy_litecoin

Litecoin client.

#### 16. xchainpy_dogecoin

Dogecoin client.

#### 17. xchainpy_bitcoincash

Bitcoin Cash client.

#### 18. xchainpy_arbitrum

Arbitrum client. Based on the *xchainpy_ethereum*.

#### 19. xchainpy_avalanche

Avalanche client. Based on the *xchainpy_ethereum*.

#### 20. xchainpy_bsc

Binance Smart Chain client. Based on the *xchainpy_ethereum*.

## Installation

The project is available on [PyPI](https://pypi.org/user/tirinox/).

Installation guide can be found in [here](https://xchainpy2.readthedocs.io/en/latest/install.html).

### 1. In order to run the code samples

After cloning the repository, you can run the code samples in the `./examples` folder.

First, install the XChainPy2 packages. For example, for running THORChain examples, run the following commands.

```
python3 -m pip install --editable packages/xchainpy_crypto
python3 -m pip install --editable packages/xchainpy_utils
python3 -m pip install --editable packages/xchainpy_client
python3 -m pip install --editable packages/xchainpy_cosmos
python3 -m pip install --editable packages/xchainpy_thorchain
```

Or just `make tc_env` which does the same thing.

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

And so on.

## Test

First install the dependencies:

`make dev_tools`

Then run the tests:

`make test`

## To Do list

Mandatory items.

- [ ] MayaProtocol AMM
- [ ] ERC20 debugging
- [ ] Documentation
- [ ] More tests
- [x] Utils package
- [x] Crypto utils package
- [x] Base blockchain client package
- [x] THORChain package
- [x] Cosmos package
- [x] UTXO providers (Haskoin, Sochain, Blockcypher)
- [x] Tests for the Query Package
- [x] Examples for Query Package
- [x] Mayachain client
- [x] Bitcoin client
- [x] Ethereum client
- [x] Other UTXO clients
- [x] Other EVM clients
- [x] Loans

The list goes on.

### Innovation

- [x] MRC20 and M-NFT support
- [ ] ERC20 token discovery
- [ ] Block-timestamp conversion
- [x] Retry/fallback for the generated Midgard/THORNode clients
- [x] Wait for the tx to be completed
- [ ] Utils for DEX aggregators

The list goes on.

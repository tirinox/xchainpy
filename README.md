# xchainpy

XChainPy2 is a library for Python with a common interface for multiple blockchains, built for simple and fast integration for wallets and more.

A free interpretation of [XChainJS](https://xchainjs.org/).

## Installation

The project is still under active development and is not ready for production use.
It is not yet available on PyPi.
For now, you can install the packages manually.

By navigating to each directory of the package of your interest, just execute the following command:
`python3 setup.py develop`

Then you can have some fun by running code samples inside the `./examples` folder.

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
- [ ] Retry/fallback for the generated Midgard/THORNode clients
- [ ] Wait for the tx to be completed
- [ ] Utils for DEX aggregators

The list goes on.
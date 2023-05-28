# XChainPy2 Wallet Client Interface

A specification for a generalised interface for crypto wallets clients, to be used by XChainPy2 implementations. 
The client should not have any functionality to generate a key, instead, 
the `asgardex-crypto` (todo: is there such lib for Py?) library should be used to ensure cross-chain compatible keystores are handled. 
The client is only ever passed a master BIP39 phrase, from which a temporary key and address is decoded.

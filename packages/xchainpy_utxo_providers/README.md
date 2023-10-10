# `@xchainpy/xchain-util`

A specification for a generalised interface for api providers, to be used by XChainPy2 implementations. The providers should not have any functionality to generate a key, instead, the xchain-crypto library should be used to ensure cross-chain compatible keystores are handled. The providers is only ever passed a master BIP39 phrase, from which a temporary key and address is decoded.


## Installation

todo

# xchainpy2-mayanode
Mayanode REST API.

This Python package is automatically generated by the [Swagger Codegen](https://github.com/swagger-api/swagger-codegen) project:

- API version: 1.108.1
- Package version: 1.108.1
- Build package: io.swagger.codegen.v3.generators.python.PythonClientCodegen

## Requirements.

Python 2.7 and 3.4+

## Installation & Usage
### pip install

If the python package is hosted on Github, you can install directly from Github

```sh
pip install git+https://github.com/GIT_USER_ID/GIT_REPO_ID.git
```
(you may need to run `pip` with root permission: `sudo pip install git+https://github.com/GIT_USER_ID/GIT_REPO_ID.git`)

Then import the package:
```python
import xchainpy2_mayanode 
```

### Setuptools

Install via [Setuptools](http://pypi.python.org/pypi/setuptools).

```sh
python setup.py install --user
```
(or `sudo python setup.py install` to install the package for all users)

Then import the package:
```python
import xchainpy2_mayanode
```

## Getting Started

Please follow the [installation procedure](#installation--usage) and then run the following:

```python
from __future__ import print_function
import time
import xchainpy2_mayanode
from xchainpy2_mayanode.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = xchainpy2_mayanode.HealthApi(xchainpy2_mayanode.ApiClient(configuration))

try:
    api_response = api_instance.ping()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling HealthApi->ping: %s\n" % e)
```

## Documentation for API Endpoints

All URIs are relative to */*

Class | Method | HTTP request | Description
------------ | ------------- | ------------- | -------------
*HealthApi* | [**ping**](docs/HealthApi.md#ping) | **GET** /mayachain/ping | 
*LiquidityProvidersApi* | [**liquidity_provider**](docs/LiquidityProvidersApi.md#liquidity_provider) | **GET** /mayachain/pool/{asset}/liquidity_provider/{address} | 
*LiquidityProvidersApi* | [**liquidity_providers**](docs/LiquidityProvidersApi.md#liquidity_providers) | **GET** /mayachain/pool/{asset}/liquidity_providers | 
*MayanamesApi* | [**mayaname**](docs/MayanamesApi.md#mayaname) | **GET** /mayachain/mayaname/{name} | 
*MimirApi* | [**mimir**](docs/MimirApi.md#mimir) | **GET** /mayachain/mimir | 
*MimirApi* | [**mimir_admin**](docs/MimirApi.md#mimir_admin) | **GET** /mayachain/mimir/admin | 
*MimirApi* | [**mimir_key**](docs/MimirApi.md#mimir_key) | **GET** /mayachain/mimir/key/{key} | 
*MimirApi* | [**mimir_node**](docs/MimirApi.md#mimir_node) | **GET** /mayachain/mimir/node/{address} | 
*MimirApi* | [**mimir_nodes**](docs/MimirApi.md#mimir_nodes) | **GET** /mayachain/mimir/nodes_all | 
*NetworkApi* | [**ban**](docs/NetworkApi.md#ban) | **GET** /mayachain/ban/{address} | 
*NetworkApi* | [**constants**](docs/NetworkApi.md#constants) | **GET** /mayachain/constants | 
*NetworkApi* | [**inbound_addresses**](docs/NetworkApi.md#inbound_addresses) | **GET** /mayachain/inbound_addresses | 
*NetworkApi* | [**lastblock**](docs/NetworkApi.md#lastblock) | **GET** /mayachain/lastblock | 
*NetworkApi* | [**lastblock_chain**](docs/NetworkApi.md#lastblock_chain) | **GET** /mayachain/lastblock/{chain} | 
*NetworkApi* | [**network**](docs/NetworkApi.md#network) | **GET** /mayachain/network | 
*NetworkApi* | [**ragnarok**](docs/NetworkApi.md#ragnarok) | **GET** /mayachain/ragnarok | 
*NetworkApi* | [**version**](docs/NetworkApi.md#version) | **GET** /mayachain/version | 
*NodesApi* | [**node**](docs/NodesApi.md#node) | **GET** /mayachain/node/{address} | 
*NodesApi* | [**nodes**](docs/NodesApi.md#nodes) | **GET** /mayachain/nodes | 
*POLApi* | [**pol**](docs/POLApi.md#pol) | **GET** /mayachain/pol | 
*PoolsApi* | [**pool**](docs/PoolsApi.md#pool) | **GET** /mayachain/pool/{asset} | 
*PoolsApi* | [**pools**](docs/PoolsApi.md#pools) | **GET** /mayachain/pools | 
*QueueApi* | [**queue**](docs/QueueApi.md#queue) | **GET** /mayachain/queue | 
*QueueApi* | [**queue_outbound**](docs/QueueApi.md#queue_outbound) | **GET** /mayachain/queue/outbound | 
*QueueApi* | [**queue_scheduled**](docs/QueueApi.md#queue_scheduled) | **GET** /mayachain/queue/scheduled | 
*QuoteApi* | [**quotesaverdeposit**](docs/QuoteApi.md#quotesaverdeposit) | **GET** /mayachain/quote/saver/deposit | 
*QuoteApi* | [**quotesaverwithdraw**](docs/QuoteApi.md#quotesaverwithdraw) | **GET** /mayachain/quote/saver/withdraw | 
*QuoteApi* | [**quoteswap**](docs/QuoteApi.md#quoteswap) | **GET** /mayachain/quote/swap | 
*SaversApi* | [**saver**](docs/SaversApi.md#saver) | **GET** /mayachain/pool/{asset}/saver/{address} | 
*SaversApi* | [**savers**](docs/SaversApi.md#savers) | **GET** /mayachain/pool/{asset}/savers | 
*TSSApi* | [**keysign**](docs/TSSApi.md#keysign) | **GET** /mayachain/keysign/{height} | 
*TSSApi* | [**keysign_pubkey**](docs/TSSApi.md#keysign_pubkey) | **GET** /mayachain/keysign/{height}/{pubkey} | 
*TSSApi* | [**metrics**](docs/TSSApi.md#metrics) | **GET** /mayachain/metrics | 
*TSSApi* | [**metrics_keygen**](docs/TSSApi.md#metrics_keygen) | **GET** /mayachain/metric/keygen/{pubkey} | 
*TransactionsApi* | [**tx**](docs/TransactionsApi.md#tx) | **GET** /mayachain/tx/{hash} | 
*TransactionsApi* | [**tx_signers**](docs/TransactionsApi.md#tx_signers) | **GET** /mayachain/tx/{hash}/signers | 
*VaultsApi* | [**asgard**](docs/VaultsApi.md#asgard) | **GET** /mayachain/vaults/asgard | 
*VaultsApi* | [**vault**](docs/VaultsApi.md#vault) | **GET** /mayachain/vaults/{pubkey} | 
*VaultsApi* | [**vault_pubkeys**](docs/VaultsApi.md#vault_pubkeys) | **GET** /mayachain/vaults/pubkeys | 
*VaultsApi* | [**yggdrasil**](docs/VaultsApi.md#yggdrasil) | **GET** /mayachain/vaults/yggdrasil | 

## Documentation For Models

 - [BanResponse](docs/BanResponse.md)
 - [ChainHeight](docs/ChainHeight.md)
 - [Coin](docs/Coin.md)
 - [ConstantsResponse](docs/ConstantsResponse.md)
 - [InboundAddress](docs/InboundAddress.md)
 - [InboundAddressesResponse](docs/InboundAddressesResponse.md)
 - [KeygenMetric](docs/KeygenMetric.md)
 - [KeygenMetric1](docs/KeygenMetric1.md)
 - [KeygenMetric2](docs/KeygenMetric2.md)
 - [KeygenMetricsResponse](docs/KeygenMetricsResponse.md)
 - [KeysignInfo](docs/KeysignInfo.md)
 - [KeysignMetrics](docs/KeysignMetrics.md)
 - [KeysignResponse](docs/KeysignResponse.md)
 - [LPBondedNode](docs/LPBondedNode.md)
 - [LastBlock](docs/LastBlock.md)
 - [LastBlockResponse](docs/LastBlockResponse.md)
 - [LiquidityProvider](docs/LiquidityProvider.md)
 - [LiquidityProviderResponse](docs/LiquidityProviderResponse.md)
 - [LiquidityProviderSummary](docs/LiquidityProviderSummary.md)
 - [LiquidityProvidersResponse](docs/LiquidityProvidersResponse.md)
 - [Mayaname](docs/Mayaname.md)
 - [Mayaname1](docs/Mayaname1.md)
 - [MayanameAlias](docs/MayanameAlias.md)
 - [MayanameResponse](docs/MayanameResponse.md)
 - [MetricsResponse](docs/MetricsResponse.md)
 - [MimirNodesResponse](docs/MimirNodesResponse.md)
 - [MimirResponse](docs/MimirResponse.md)
 - [MimirVote](docs/MimirVote.md)
 - [NetworkResponse](docs/NetworkResponse.md)
 - [Node](docs/Node.md)
 - [NodeBondProvider](docs/NodeBondProvider.md)
 - [NodeBondProviders](docs/NodeBondProviders.md)
 - [NodeJail](docs/NodeJail.md)
 - [NodeKeygenMetric](docs/NodeKeygenMetric.md)
 - [NodePreflightStatus](docs/NodePreflightStatus.md)
 - [NodePubKeySet](docs/NodePubKeySet.md)
 - [NodeResponse](docs/NodeResponse.md)
 - [NodesResponse](docs/NodesResponse.md)
 - [ObservedTx](docs/ObservedTx.md)
 - [OutboundResponse](docs/OutboundResponse.md)
 - [POLResponse](docs/POLResponse.md)
 - [Ping](docs/Ping.md)
 - [Pool](docs/Pool.md)
 - [PoolResponse](docs/PoolResponse.md)
 - [PoolsResponse](docs/PoolsResponse.md)
 - [QueueResponse](docs/QueueResponse.md)
 - [QuoteFees](docs/QuoteFees.md)
 - [QuoteSaverDepositResponse](docs/QuoteSaverDepositResponse.md)
 - [QuoteSaverWithdrawResponse](docs/QuoteSaverWithdrawResponse.md)
 - [QuoteSwapResponse](docs/QuoteSwapResponse.md)
 - [Saver](docs/Saver.md)
 - [SaverResponse](docs/SaverResponse.md)
 - [SaversResponse](docs/SaversResponse.md)
 - [ScheduledResponse](docs/ScheduledResponse.md)
 - [TssKeysignMetric](docs/TssKeysignMetric.md)
 - [TssMetric](docs/TssMetric.md)
 - [Tx](docs/Tx.md)
 - [TxOutItem](docs/TxOutItem.md)
 - [TxResponse](docs/TxResponse.md)
 - [TxSignersResponse](docs/TxSignersResponse.md)
 - [Vault](docs/Vault.md)
 - [VaultAddress](docs/VaultAddress.md)
 - [VaultInfo](docs/VaultInfo.md)
 - [VaultPubkeysResponse](docs/VaultPubkeysResponse.md)
 - [VaultResponse](docs/VaultResponse.md)
 - [VaultRouter](docs/VaultRouter.md)
 - [VaultsResponse](docs/VaultsResponse.md)
 - [VersionResponse](docs/VersionResponse.md)

## Documentation For Authorization

 All endpoints do not require authorization.


## Author

devs@mayachain.org

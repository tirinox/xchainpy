# xchainpy2_thornode.NetworkApi

All URIs are relative to */*

Method | HTTP request | Description
------------- | ------------- | -------------
[**ban**](NetworkApi.md#ban) | **GET** /thorchain/ban/{address} | 
[**constants**](NetworkApi.md#constants) | **GET** /thorchain/constants | 
[**inbound_addresses**](NetworkApi.md#inbound_addresses) | **GET** /thorchain/inbound_addresses | 
[**lastblock**](NetworkApi.md#lastblock) | **GET** /thorchain/lastblock | 
[**lastblock_chain**](NetworkApi.md#lastblock_chain) | **GET** /thorchain/lastblock/{chain} | 
[**network**](NetworkApi.md#network) | **GET** /thorchain/network | 
[**outbound_fee_asset**](NetworkApi.md#outbound_fee_asset) | **GET** /thorchain/outbound_fee/{asset} | 
[**outbound_fees**](NetworkApi.md#outbound_fees) | **GET** /thorchain/outbound_fees | 
[**ragnarok**](NetworkApi.md#ragnarok) | **GET** /thorchain/ragnarok | 
[**version**](NetworkApi.md#version) | **GET** /thorchain/version | 

# **ban**
> BanResponse ban(address, height=height)



Returns the ban status for the provided node address.

### Example
```python
from __future__ import print_function
import time
import xchainpy2_thornode
from xchainpy2_thornode.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = xchainpy2_thornode.NetworkApi()
address = 'address_example' # str | 
height = 789 # int | optional block height, defaults to current tip (optional)

try:
    api_response = api_instance.ban(address, height=height)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling NetworkApi->ban: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **address** | **str**|  | 
 **height** | **int**| optional block height, defaults to current tip | [optional] 

### Return type

[**BanResponse**](BanResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **constants**
> ConstantsResponse constants(height=height)



Returns constant configuration, can be overridden by mimir.

### Example
```python
from __future__ import print_function
import time
import xchainpy2_thornode
from xchainpy2_thornode.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = xchainpy2_thornode.NetworkApi()
height = 789 # int | optional block height, defaults to current tip (optional)

try:
    api_response = api_instance.constants(height=height)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling NetworkApi->constants: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **height** | **int**| optional block height, defaults to current tip | [optional] 

### Return type

[**ConstantsResponse**](ConstantsResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **inbound_addresses**
> list[InboundAddress] inbound_addresses(height=height)



Returns the set of asgard addresses that should be used for inbound transactions.

### Example
```python
from __future__ import print_function
import time
import xchainpy2_thornode
from xchainpy2_thornode.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = xchainpy2_thornode.NetworkApi()
height = 789 # int | optional block height, defaults to current tip (optional)

try:
    api_response = api_instance.inbound_addresses(height=height)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling NetworkApi->inbound_addresses: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **height** | **int**| optional block height, defaults to current tip | [optional] 

### Return type

[**list[InboundAddress]**](InboundAddress.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **lastblock**
> list[LastBlock] lastblock(height=height)



Returns the last block information for all chains.

### Example
```python
from __future__ import print_function
import time
import xchainpy2_thornode
from xchainpy2_thornode.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = xchainpy2_thornode.NetworkApi()
height = 789 # int | optional block height, defaults to current tip (optional)

try:
    api_response = api_instance.lastblock(height=height)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling NetworkApi->lastblock: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **height** | **int**| optional block height, defaults to current tip | [optional] 

### Return type

[**list[LastBlock]**](LastBlock.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **lastblock_chain**
> list[LastBlock] lastblock_chain(chain, height=height)



Returns the last block information for the provided chain.

### Example
```python
from __future__ import print_function
import time
import xchainpy2_thornode
from xchainpy2_thornode.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = xchainpy2_thornode.NetworkApi()
chain = 'chain_example' # str | 
height = 789 # int | optional block height, defaults to current tip (optional)

try:
    api_response = api_instance.lastblock_chain(chain, height=height)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling NetworkApi->lastblock_chain: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **chain** | **str**|  | 
 **height** | **int**| optional block height, defaults to current tip | [optional] 

### Return type

[**list[LastBlock]**](LastBlock.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **network**
> NetworkResponse network(height=height)



Returns network overview statistics.

### Example
```python
from __future__ import print_function
import time
import xchainpy2_thornode
from xchainpy2_thornode.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = xchainpy2_thornode.NetworkApi()
height = 789 # int | optional block height, defaults to current tip (optional)

try:
    api_response = api_instance.network(height=height)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling NetworkApi->network: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **height** | **int**| optional block height, defaults to current tip | [optional] 

### Return type

[**NetworkResponse**](NetworkResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **outbound_fee_asset**
> list[OutboundFee] outbound_fee_asset(asset, height=height)



Returns the outbound fee information for the provided asset.

### Example
```python
from __future__ import print_function
import time
import xchainpy2_thornode
from xchainpy2_thornode.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = xchainpy2_thornode.NetworkApi()
asset = 'asset_example' # str | 
height = 789 # int | optional block height, defaults to current tip (optional)

try:
    api_response = api_instance.outbound_fee_asset(asset, height=height)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling NetworkApi->outbound_fee_asset: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **asset** | **str**|  | 
 **height** | **int**| optional block height, defaults to current tip | [optional] 

### Return type

[**list[OutboundFee]**](OutboundFee.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **outbound_fees**
> list[OutboundFee] outbound_fees(height=height)



Returns the last block information for all chains.

### Example
```python
from __future__ import print_function
import time
import xchainpy2_thornode
from xchainpy2_thornode.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = xchainpy2_thornode.NetworkApi()
height = 789 # int | optional block height, defaults to current tip (optional)

try:
    api_response = api_instance.outbound_fees(height=height)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling NetworkApi->outbound_fees: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **height** | **int**| optional block height, defaults to current tip | [optional] 

### Return type

[**list[OutboundFee]**](OutboundFee.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **ragnarok**
> bool ragnarok(height=height)



Returns a boolean indicating whether the chain is in ragnarok.

### Example
```python
from __future__ import print_function
import time
import xchainpy2_thornode
from xchainpy2_thornode.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = xchainpy2_thornode.NetworkApi()
height = 789 # int | optional block height, defaults to current tip (optional)

try:
    api_response = api_instance.ragnarok(height=height)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling NetworkApi->ragnarok: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **height** | **int**| optional block height, defaults to current tip | [optional] 

### Return type

**bool**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **version**
> VersionResponse version(height=height)



Returns the network's current THORNode version, the network's next THORNode version, and the querier's THORNode version.

### Example
```python
from __future__ import print_function
import time
import xchainpy2_thornode
from xchainpy2_thornode.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = xchainpy2_thornode.NetworkApi()
height = 789 # int | optional block height, defaults to current tip (optional)

try:
    api_response = api_instance.version(height=height)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling NetworkApi->version: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **height** | **int**| optional block height, defaults to current tip | [optional] 

### Return type

[**VersionResponse**](VersionResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


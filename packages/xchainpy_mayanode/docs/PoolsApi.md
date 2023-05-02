# xchainpy2_mayanode.PoolsApi

All URIs are relative to */*

Method | HTTP request | Description
------------- | ------------- | -------------
[**pool**](PoolsApi.md#pool) | **GET** /mayachain/pool/{asset} | 
[**pools**](PoolsApi.md#pools) | **GET** /mayachain/pools | 

# **pool**
> Pool pool(asset, height=height)



Returns the pool information for the provided asset.

### Example
```python
from __future__ import print_function
import time
import xchainpy2_mayanode
from xchainpy2_mayanode.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = xchainpy2_mayanode.PoolsApi()
asset = 'asset_example' # str | 
height = 789 # int | optional block height, defaults to current tip (optional)

try:
    api_response = api_instance.pool(asset, height=height)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling PoolsApi->pool: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **asset** | **str**|  | 
 **height** | **int**| optional block height, defaults to current tip | [optional] 

### Return type

[**Pool**](Pool.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **pools**
> list[Pool] pools(height=height)



Returns the pool information for all assets.

### Example
```python
from __future__ import print_function
import time
import xchainpy2_mayanode
from xchainpy2_mayanode.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = xchainpy2_mayanode.PoolsApi()
height = 789 # int | optional block height, defaults to current tip (optional)

try:
    api_response = api_instance.pools(height=height)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling PoolsApi->pools: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **height** | **int**| optional block height, defaults to current tip | [optional] 

### Return type

[**list[Pool]**](Pool.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


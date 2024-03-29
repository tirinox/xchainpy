# xchainpy2_thornode.PoolsApi

All URIs are relative to */*

Method | HTTP request | Description
------------- | ------------- | -------------
[**dpool**](PoolsApi.md#dpool) | **GET** /thorchain/dpool/{asset} | 
[**dpools**](PoolsApi.md#dpools) | **GET** /thorchain/dpools | 
[**pool**](PoolsApi.md#pool) | **GET** /thorchain/pool/{asset} | 
[**pools**](PoolsApi.md#pools) | **GET** /thorchain/pools | 

# **dpool**
> DerivedPool dpool(asset, height=height)



Returns the pool information for the provided derived asset.

### Example
```python
from __future__ import print_function
import time
import xchainpy2_thornode
from xchainpy2_thornode.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = xchainpy2_thornode.PoolsApi()
asset = 'asset_example' # str | 
height = 789 # int | optional block height, defaults to current tip (optional)

try:
    api_response = api_instance.dpool(asset, height=height)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling PoolsApi->dpool: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **asset** | **str**|  | 
 **height** | **int**| optional block height, defaults to current tip | [optional] 

### Return type

[**DerivedPool**](DerivedPool.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **dpools**
> list[DerivedPool] dpools(height=height)



Returns the pool information for all derived assets.

### Example
```python
from __future__ import print_function
import time
import xchainpy2_thornode
from xchainpy2_thornode.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = xchainpy2_thornode.PoolsApi()
height = 789 # int | optional block height, defaults to current tip (optional)

try:
    api_response = api_instance.dpools(height=height)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling PoolsApi->dpools: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **height** | **int**| optional block height, defaults to current tip | [optional] 

### Return type

[**list[DerivedPool]**](DerivedPool.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **pool**
> Pool pool(asset, height=height)



Returns the pool information for the provided asset.

### Example
```python
from __future__ import print_function
import time
import xchainpy2_thornode
from xchainpy2_thornode.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = xchainpy2_thornode.PoolsApi()
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
import xchainpy2_thornode
from xchainpy2_thornode.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = xchainpy2_thornode.PoolsApi()
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


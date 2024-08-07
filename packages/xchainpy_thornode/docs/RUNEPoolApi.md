# xchainpy2_thornode.RUNEPoolApi

All URIs are relative to */*

Method | HTTP request | Description
------------- | ------------- | -------------
[**rune_pool**](RUNEPoolApi.md#rune_pool) | **GET** /thorchain/runepool | 
[**rune_provider**](RUNEPoolApi.md#rune_provider) | **GET** /thorchain/rune_provider/{address} | 
[**rune_providers**](RUNEPoolApi.md#rune_providers) | **GET** /thorchain/rune_providers | 

# **rune_pool**
> RUNEPoolResponse rune_pool(height=height)



Returns the pool information for the RUNE pool.

### Example
```python
from __future__ import print_function
import time
import xchainpy2_thornode
from xchainpy2_thornode.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = xchainpy2_thornode.RUNEPoolApi()
height = 789 # int | optional block height, defaults to current tip (optional)

try:
    api_response = api_instance.rune_pool(height=height)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling RUNEPoolApi->rune_pool: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **height** | **int**| optional block height, defaults to current tip | [optional] 

### Return type

[**RUNEPoolResponse**](RUNEPoolResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **rune_provider**
> RUNEProvider rune_provider(address, height=height)



Returns the RUNE Provider information for an address.

### Example
```python
from __future__ import print_function
import time
import xchainpy2_thornode
from xchainpy2_thornode.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = xchainpy2_thornode.RUNEPoolApi()
address = 'address_example' # str | 
height = 789 # int | optional block height, defaults to current tip (optional)

try:
    api_response = api_instance.rune_provider(address, height=height)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling RUNEPoolApi->rune_provider: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **address** | **str**|  | 
 **height** | **int**| optional block height, defaults to current tip | [optional] 

### Return type

[**RUNEProvider**](RUNEProvider.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **rune_providers**
> list[RUNEProvider] rune_providers(height=height)



Returns all RUNE Providers.

### Example
```python
from __future__ import print_function
import time
import xchainpy2_thornode
from xchainpy2_thornode.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = xchainpy2_thornode.RUNEPoolApi()
height = 789 # int | optional block height, defaults to current tip (optional)

try:
    api_response = api_instance.rune_providers(height=height)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling RUNEPoolApi->rune_providers: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **height** | **int**| optional block height, defaults to current tip | [optional] 

### Return type

[**list[RUNEProvider]**](RUNEProvider.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


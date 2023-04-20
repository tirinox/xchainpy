# thornode_client.SaversApi

All URIs are relative to */*

Method | HTTP request | Description
------------- | ------------- | -------------
[**saver**](SaversApi.md#saver) | **GET** /thorchain/pool/{asset}/saver/{address} | 
[**savers**](SaversApi.md#savers) | **GET** /thorchain/pool/{asset}/savers | 

# **saver**
> SaverResponse saver(asset, address, height=height)



Returns the saver position given then savers pool and address.

### Example
```python
from __future__ import print_function
import time
import thornode_client
from thornode_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = thornode_client.SaversApi()
asset = 'asset_example' # str | 
address = 'address_example' # str | 
height = 789 # int | optional block height, defaults to current tip (optional)

try:
    api_response = api_instance.saver(asset, address, height=height)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling SaversApi->saver: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **asset** | **str**|  | 
 **address** | **str**|  | 
 **height** | **int**| optional block height, defaults to current tip | [optional] 

### Return type

[**SaverResponse**](SaverResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **savers**
> SaversResponse savers(asset, height=height)



Returns all savers for the savers pool.

### Example
```python
from __future__ import print_function
import time
import thornode_client
from thornode_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = thornode_client.SaversApi()
asset = 'asset_example' # str | 
height = 789 # int | optional block height, defaults to current tip (optional)

try:
    api_response = api_instance.savers(asset, height=height)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling SaversApi->savers: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **asset** | **str**|  | 
 **height** | **int**| optional block height, defaults to current tip | [optional] 

### Return type

[**SaversResponse**](SaversResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


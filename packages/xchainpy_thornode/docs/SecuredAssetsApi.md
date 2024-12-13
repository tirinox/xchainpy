# xchainpy2_thornode.SecuredAssetsApi

All URIs are relative to */*

Method | HTTP request | Description
------------- | ------------- | -------------
[**secured_assets**](SecuredAssetsApi.md#secured_assets) | **GET** /thorchain/securedassets | 

# **secured_assets**
> list[SecuredAssetResponse] secured_assets(height=height)



Returns the total size and ratio of all secured asset

### Example
```python
from __future__ import print_function
import time
import xchainpy2_thornode
from xchainpy2_thornode.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = xchainpy2_thornode.SecuredAssetsApi()
height = 789 # int | optional block height, defaults to current tip (optional)

try:
    api_response = api_instance.secured_assets(height=height)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling SecuredAssetsApi->secured_assets: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **height** | **int**| optional block height, defaults to current tip | [optional] 

### Return type

[**list[SecuredAssetResponse]**](SecuredAssetResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


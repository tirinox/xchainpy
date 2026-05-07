# xchainpy2_thornode.CodesApi

All URIs are relative to *https://gateway.liquify.com/chain/thorchain_api*

Method | HTTP request | Description
------------- | ------------- | -------------
[**codes**](CodesApi.md#codes) | **GET** /thorchain/codes | 

# **codes**
> CodesResponse codes(height=height)



Returns all whitelisted contract codes

### Example
```python
from __future__ import print_function
import time
import xchainpy2_thornode
from xchainpy2_thornode.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = xchainpy2_thornode.CodesApi()
height = 789 # int | optional block height, defaults to current tip (optional)

try:
    api_response = api_instance.codes(height=height)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling CodesApi->codes: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **height** | **int**| optional block height, defaults to current tip | [optional] 

### Return type

[**CodesResponse**](CodesResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


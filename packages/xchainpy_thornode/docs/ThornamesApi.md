# xchainpy2_thornode.ThornamesApi

All URIs are relative to */*

Method | HTTP request | Description
------------- | ------------- | -------------
[**thorname**](ThornamesApi.md#thorname) | **GET** /thorchain/thorname/{name} | 

# **thorname**
> ThornameResponse thorname(name, height=height)



Returns addresses registered to the provided thorname.

### Example
```python
from __future__ import print_function
import time
import xchainpy2_thornode
from xchainpy2_thornode.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = xchainpy2_thornode.ThornamesApi()
name = 'name_example' # str | the thornode to lookup
height = 789 # int | optional block height, defaults to current tip (optional)

try:
    api_response = api_instance.thorname(name, height=height)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ThornamesApi->thorname: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **name** | **str**| the thornode to lookup | 
 **height** | **int**| optional block height, defaults to current tip | [optional] 

### Return type

[**ThornameResponse**](ThornameResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


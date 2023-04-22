# xchainpy2_mayanode.MayanamesApi

All URIs are relative to */*

Method | HTTP request | Description
------------- | ------------- | -------------
[**mayaname**](MayanamesApi.md#mayaname) | **GET** /mayachain/mayaname/{name} | 

# **mayaname**
> MayanameResponse mayaname(name, height=height)



Returns addresses registered to the provided mayaname.

### Example
```python
from __future__ import print_function
import time
import xchainpy2_mayanode
from xchainpy2_mayanode.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = xchainpy2_mayanode.MayanamesApi()
name = 'name_example' # str | the mayanode to lookup
height = 789 # int | optional block height, defaults to current tip (optional)

try:
    api_response = api_instance.mayaname(name, height=height)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling MayanamesApi->mayaname: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **name** | **str**| the mayanode to lookup | 
 **height** | **int**| optional block height, defaults to current tip | [optional] 

### Return type

[**MayanameResponse**](MayanameResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


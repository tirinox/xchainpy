# mayanode_client.POLApi

All URIs are relative to */*

Method | HTTP request | Description
------------- | ------------- | -------------
[**pol**](POLApi.md#pol) | **GET** /mayachain/pol | 

# **pol**
> POLResponse pol(height=height)



Returns protocol owned liquidity overview statistics.

### Example
```python
from __future__ import print_function
import time
import mayanode_client
from mayanode_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = mayanode_client.POLApi()
height = 789 # int | optional block height, defaults to current tip (optional)

try:
    api_response = api_instance.pol(height=height)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling POLApi->pol: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **height** | **int**| optional block height, defaults to current tip | [optional] 

### Return type

[**POLResponse**](POLResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


# xchainpy2_thornode.ExportApi

All URIs are relative to */*

Method | HTTP request | Description
------------- | ------------- | -------------
[**export**](ExportApi.md#export) | **GET** /thorchain/export | 

# **export**
> ExportResponse export()



Returns genesis export

### Example
```python
from __future__ import print_function
import time
import xchainpy2_thornode
from xchainpy2_thornode.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = xchainpy2_thornode.ExportApi()

try:
    api_response = api_instance.export()
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ExportApi->export: %s\n" % e)
```

### Parameters
This endpoint does not need any parameter.

### Return type

[**ExportResponse**](ExportResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


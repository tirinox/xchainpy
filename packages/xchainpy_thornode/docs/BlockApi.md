# xchainpy2_thornode.BlockApi

All URIs are relative to */*

Method | HTTP request | Description
------------- | ------------- | -------------
[**block**](BlockApi.md#block) | **GET** /thorchain/block | 

# **block**
> BlockResponse block(height=height)



Returns verbose details of the block.

### Example
```python
from __future__ import print_function
import time
import xchainpy2_thornode
from xchainpy2_thornode.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = xchainpy2_thornode.BlockApi()
height = 789 # int | optional block height, defaults to current tip (optional)

try:
    api_response = api_instance.block(height=height)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling BlockApi->block: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **height** | **int**| optional block height, defaults to current tip | [optional] 

### Return type

[**BlockResponse**](BlockResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


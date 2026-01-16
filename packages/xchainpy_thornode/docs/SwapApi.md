# xchainpy2_thornode.SwapApi

All URIs are relative to */*

Method | HTTP request | Description
------------- | ------------- | -------------
[**swap_details**](SwapApi.md#swap_details) | **GET** /thorchain/queue/swap/details/{tx_id} | 

# **swap_details**
> SwapDetailsResponse swap_details(tx_id, height=height)



Returns detailed information about a specific swap including its state.

### Example
```python
from __future__ import print_function
import time
import xchainpy2_thornode
from xchainpy2_thornode.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = xchainpy2_thornode.SwapApi()
tx_id = 'tx_id_example' # str | Transaction ID of the swap
height = 789 # int | optional block height, defaults to current tip (optional)

try:
    api_response = api_instance.swap_details(tx_id, height=height)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling SwapApi->swap_details: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **tx_id** | **str**| Transaction ID of the swap | 
 **height** | **int**| optional block height, defaults to current tip | [optional] 

### Return type

[**SwapDetailsResponse**](SwapDetailsResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


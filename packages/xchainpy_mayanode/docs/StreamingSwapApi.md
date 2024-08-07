# xchainpy2_mayanode.StreamingSwapApi

All URIs are relative to */*

Method | HTTP request | Description
------------- | ------------- | -------------
[**stream_swap**](StreamingSwapApi.md#stream_swap) | **GET** /mayachain/swap/streaming/{hash} | 
[**stream_swaps**](StreamingSwapApi.md#stream_swaps) | **GET** /mayachain/swaps/streaming | 

# **stream_swap**
> StreamingSwap stream_swap(hash, height=height)



Returns the state of a streaming swap

### Example
```python
from __future__ import print_function
import time
import xchainpy2_mayanode
from xchainpy2_mayanode.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = xchainpy2_mayanode.StreamingSwapApi()
hash = 'hash_example' # str | 
height = 789 # int | optional block height, defaults to current tip (optional)

try:
    api_response = api_instance.stream_swap(hash, height=height)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling StreamingSwapApi->stream_swap: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **hash** | **str**|  | 
 **height** | **int**| optional block height, defaults to current tip | [optional] 

### Return type

[**StreamingSwap**](StreamingSwap.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **stream_swaps**
> list[StreamingSwap] stream_swaps(height=height)



Returns the state of all streaming swaps

### Example
```python
from __future__ import print_function
import time
import xchainpy2_mayanode
from xchainpy2_mayanode.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = xchainpy2_mayanode.StreamingSwapApi()
height = 789 # int | optional block height, defaults to current tip (optional)

try:
    api_response = api_instance.stream_swaps(height=height)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling StreamingSwapApi->stream_swaps: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **height** | **int**| optional block height, defaults to current tip | [optional] 

### Return type

[**list[StreamingSwap]**](StreamingSwap.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


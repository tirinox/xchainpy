# xchainpy2_thornode.QueueApi

All URIs are relative to */*

Method | HTTP request | Description
------------- | ------------- | -------------
[**queue**](QueueApi.md#queue) | **GET** /thorchain/queue | 
[**queue_outbound**](QueueApi.md#queue_outbound) | **GET** /thorchain/queue/outbound | 
[**queue_scheduled**](QueueApi.md#queue_scheduled) | **GET** /thorchain/queue/scheduled | 
[**queue_swap**](QueueApi.md#queue_swap) | **GET** /thorchain/queue/swap | 

# **queue**
> QueueResponse queue(height=height)



Returns queue statistics.

### Example
```python
from __future__ import print_function
import time
import xchainpy2_thornode
from xchainpy2_thornode.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = xchainpy2_thornode.QueueApi()
height = 789 # int | optional block height, defaults to current tip (optional)

try:
    api_response = api_instance.queue(height=height)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling QueueApi->queue: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **height** | **int**| optional block height, defaults to current tip | [optional] 

### Return type

[**QueueResponse**](QueueResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **queue_outbound**
> list[TxOutItem] queue_outbound(height=height)



Returns the outbound queue including estimated RUNE values.

### Example
```python
from __future__ import print_function
import time
import xchainpy2_thornode
from xchainpy2_thornode.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = xchainpy2_thornode.QueueApi()
height = 789 # int | optional block height, defaults to current tip (optional)

try:
    api_response = api_instance.queue_outbound(height=height)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling QueueApi->queue_outbound: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **height** | **int**| optional block height, defaults to current tip | [optional] 

### Return type

[**list[TxOutItem]**](TxOutItem.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **queue_scheduled**
> list[TxOutItem] queue_scheduled(height=height)



Returns the scheduled queue.

### Example
```python
from __future__ import print_function
import time
import xchainpy2_thornode
from xchainpy2_thornode.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = xchainpy2_thornode.QueueApi()
height = 789 # int | optional block height, defaults to current tip (optional)

try:
    api_response = api_instance.queue_scheduled(height=height)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling QueueApi->queue_scheduled: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **height** | **int**| optional block height, defaults to current tip | [optional] 

### Return type

[**list[TxOutItem]**](TxOutItem.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **queue_swap**
> list[MsgSwap] queue_swap(height=height)



Returns the swap queue.

### Example
```python
from __future__ import print_function
import time
import xchainpy2_thornode
from xchainpy2_thornode.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = xchainpy2_thornode.QueueApi()
height = 789 # int | optional block height, defaults to current tip (optional)

try:
    api_response = api_instance.queue_swap(height=height)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling QueueApi->queue_swap: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **height** | **int**| optional block height, defaults to current tip | [optional] 

### Return type

[**list[MsgSwap]**](MsgSwap.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


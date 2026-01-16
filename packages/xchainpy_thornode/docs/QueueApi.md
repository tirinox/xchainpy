# xchainpy2_thornode.QueueApi

All URIs are relative to */*

Method | HTTP request | Description
------------- | ------------- | -------------
[**limit_swaps**](QueueApi.md#limit_swaps) | **GET** /thorchain/queue/limit_swaps | 
[**limit_swaps_summary**](QueueApi.md#limit_swaps_summary) | **GET** /thorchain/queue/limit_swaps/summary | 
[**queue**](QueueApi.md#queue) | **GET** /thorchain/queue | 
[**queue_outbound**](QueueApi.md#queue_outbound) | **GET** /thorchain/queue/outbound | 
[**queue_scheduled**](QueueApi.md#queue_scheduled) | **GET** /thorchain/queue/scheduled | 
[**queue_swap**](QueueApi.md#queue_swap) | **GET** /thorchain/queue/swap | 

# **limit_swaps**
> LimitSwapsResponse limit_swaps(height=height, offset=offset, limit=limit, source_asset=source_asset, target_asset=target_asset, sender=sender, sort_by=sort_by, sort_order=sort_order)



Returns limit swaps with pagination and filtering.

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
offset = 0 # int | Number of items to skip (optional) (default to 0)
limit = 100 # int | Number of items to return (optional) (default to 100)
source_asset = 'source_asset_example' # str | Filter by source asset (e.g., \"BTC.BTC\") (optional)
target_asset = 'target_asset_example' # str | Filter by target asset (e.g., \"ETH.ETH\") (optional)
sender = 'sender_example' # str | Filter by sender address (optional)
sort_by = 'ratio' # str | Sort by field (optional) (default to ratio)
sort_order = 'asc' # str | Sort order (optional) (default to asc)

try:
    api_response = api_instance.limit_swaps(height=height, offset=offset, limit=limit, source_asset=source_asset, target_asset=target_asset, sender=sender, sort_by=sort_by, sort_order=sort_order)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling QueueApi->limit_swaps: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **height** | **int**| optional block height, defaults to current tip | [optional] 
 **offset** | **int**| Number of items to skip | [optional] [default to 0]
 **limit** | **int**| Number of items to return | [optional] [default to 100]
 **source_asset** | **str**| Filter by source asset (e.g., \&quot;BTC.BTC\&quot;) | [optional] 
 **target_asset** | **str**| Filter by target asset (e.g., \&quot;ETH.ETH\&quot;) | [optional] 
 **sender** | **str**| Filter by sender address | [optional] 
 **sort_by** | **str**| Sort by field | [optional] [default to ratio]
 **sort_order** | **str**| Sort order | [optional] [default to asc]

### Return type

[**LimitSwapsResponse**](LimitSwapsResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **limit_swaps_summary**
> LimitSwapsSummaryResponse limit_swaps_summary(height=height, source_asset=source_asset, target_asset=target_asset)



Returns limit swaps summary statistics.

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
source_asset = 'source_asset_example' # str | Filter by source asset (e.g., \"BTC.BTC\") (optional)
target_asset = 'target_asset_example' # str | Filter by target asset (e.g., \"ETH.ETH\") (optional)

try:
    api_response = api_instance.limit_swaps_summary(height=height, source_asset=source_asset, target_asset=target_asset)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling QueueApi->limit_swaps_summary: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **height** | **int**| optional block height, defaults to current tip | [optional] 
 **source_asset** | **str**| Filter by source asset (e.g., \&quot;BTC.BTC\&quot;) | [optional] 
 **target_asset** | **str**| Filter by target asset (e.g., \&quot;ETH.ETH\&quot;) | [optional] 

### Return type

[**LimitSwapsSummaryResponse**](LimitSwapsSummaryResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

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


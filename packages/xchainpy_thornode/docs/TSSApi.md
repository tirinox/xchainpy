# xchainpy2_thornode.TSSApi

All URIs are relative to */*

Method | HTTP request | Description
------------- | ------------- | -------------
[**keysign**](TSSApi.md#keysign) | **GET** /thorchain/keysign/{height} | 
[**keysign_pubkey**](TSSApi.md#keysign_pubkey) | **GET** /thorchain/keysign/{height}/{pubkey} | 
[**metrics**](TSSApi.md#metrics) | **GET** /thorchain/metrics | 
[**metrics_keygen**](TSSApi.md#metrics_keygen) | **GET** /thorchain/metric/keygen/{pubkey} | 

# **keysign**
> KeysignResponse keysign(height)



Returns keysign information for the provided height - the height being the first block a tx out item appears in the signed-but-unobserved outbound queue.

### Example
```python
from __future__ import print_function
import time
import xchainpy2_thornode
from xchainpy2_thornode.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = xchainpy2_thornode.TSSApi()
height = 789 # int | 

try:
    api_response = api_instance.keysign(height)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling TSSApi->keysign: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **height** | **int**|  | 

### Return type

[**KeysignResponse**](KeysignResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **keysign_pubkey**
> KeysignResponse keysign_pubkey(height, pubkey)



Returns keysign information for the provided height and pubkey - the height being the block at which a tx out item is scheduled to be signed and moved from the scheduled outbound queue to the outbound queue.

### Example
```python
from __future__ import print_function
import time
import xchainpy2_thornode
from xchainpy2_thornode.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = xchainpy2_thornode.TSSApi()
height = 789 # int | 
pubkey = 'pubkey_example' # str | 

try:
    api_response = api_instance.keysign_pubkey(height, pubkey)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling TSSApi->keysign_pubkey: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **height** | **int**|  | 
 **pubkey** | **str**|  | 

### Return type

[**KeysignResponse**](KeysignResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **metrics**
> MetricsResponse metrics(height=height)



Returns keygen and keysign metrics for current vaults.

### Example
```python
from __future__ import print_function
import time
import xchainpy2_thornode
from xchainpy2_thornode.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = xchainpy2_thornode.TSSApi()
height = 789 # int | optional block height, defaults to current tip (optional)

try:
    api_response = api_instance.metrics(height=height)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling TSSApi->metrics: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **height** | **int**| optional block height, defaults to current tip | [optional] 

### Return type

[**MetricsResponse**](MetricsResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **metrics_keygen**
> list[KeygenMetric] metrics_keygen(pubkey, height=height)



Returns keygen metrics for the provided vault pubkey.

### Example
```python
from __future__ import print_function
import time
import xchainpy2_thornode
from xchainpy2_thornode.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = xchainpy2_thornode.TSSApi()
pubkey = 'pubkey_example' # str | 
height = 789 # int | optional block height, defaults to current tip (optional)

try:
    api_response = api_instance.metrics_keygen(pubkey, height=height)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling TSSApi->metrics_keygen: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **pubkey** | **str**|  | 
 **height** | **int**| optional block height, defaults to current tip | [optional] 

### Return type

[**list[KeygenMetric]**](KeygenMetric.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


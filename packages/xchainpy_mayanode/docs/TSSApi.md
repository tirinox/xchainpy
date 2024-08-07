# xchainpy2_mayanode.TSSApi

All URIs are relative to */*

Method | HTTP request | Description
------------- | ------------- | -------------
[**keygen_pubkey**](TSSApi.md#keygen_pubkey) | **GET** /mayachain/keygen/{height}/{pubkey} | 
[**keysign**](TSSApi.md#keysign) | **GET** /mayachain/keysign/{height} | 
[**keysign_pubkey**](TSSApi.md#keysign_pubkey) | **GET** /mayachain/keysign/{height}/{pubkey} | 
[**metrics**](TSSApi.md#metrics) | **GET** /mayachain/metrics | 
[**metrics_keygen**](TSSApi.md#metrics_keygen) | **GET** /mayachain/metric/keygen/{pubkey} | 

# **keygen_pubkey**
> KeygenResponse keygen_pubkey(height, pubkey)



Returns keygen information for the provided height and pubkey - the pubkey being of one of the members of a keygen block for that height

### Example
```python
from __future__ import print_function
import time
import xchainpy2_mayanode
from xchainpy2_mayanode.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = xchainpy2_mayanode.TSSApi()
height = 789 # int | 
pubkey = 'pubkey_example' # str | 

try:
    api_response = api_instance.keygen_pubkey(height, pubkey)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling TSSApi->keygen_pubkey: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **height** | **int**|  | 
 **pubkey** | **str**|  | 

### Return type

[**KeygenResponse**](KeygenResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **keysign**
> KeysignResponse keysign(height)



Returns keysign information for the provided height - the height being the first block a tx out item appears in the signed-but-unobserved outbound queue.

### Example
```python
from __future__ import print_function
import time
import xchainpy2_mayanode
from xchainpy2_mayanode.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = xchainpy2_mayanode.TSSApi()
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
import xchainpy2_mayanode
from xchainpy2_mayanode.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = xchainpy2_mayanode.TSSApi()
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
import xchainpy2_mayanode
from xchainpy2_mayanode.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = xchainpy2_mayanode.TSSApi()
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
import xchainpy2_mayanode
from xchainpy2_mayanode.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = xchainpy2_mayanode.TSSApi()
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


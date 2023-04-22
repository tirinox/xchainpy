# xchainpy2_thornode.TransactionsApi

All URIs are relative to */*

Method | HTTP request | Description
------------- | ------------- | -------------
[**tx**](TransactionsApi.md#tx) | **GET** /thorchain/tx/{hash} | 
[**tx_signers**](TransactionsApi.md#tx_signers) | **GET** /thorchain/tx/details/{hash} | 
[**tx_signers_old**](TransactionsApi.md#tx_signers_old) | **GET** /thorchain/tx/{hash}/signers | 
[**tx_stages**](TransactionsApi.md#tx_stages) | **GET** /thorchain/alpha/tx/stages/{hash} | 
[**tx_status**](TransactionsApi.md#tx_status) | **GET** /thorchain/alpha/tx/status/{hash} | 

# **tx**
> TxResponse tx(hash, height=height)



Returns the observed transaction for a provided inbound or outbound hash.

### Example
```python
from __future__ import print_function
import time
import xchainpy2_thornode
from xchainpy2_thornode.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = xchainpy2_thornode.TransactionsApi()
hash = 'hash_example' # str | 
height = 789 # int | optional block height, defaults to current tip (optional)

try:
    api_response = api_instance.tx(hash, height=height)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling TransactionsApi->tx: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **hash** | **str**|  | 
 **height** | **int**| optional block height, defaults to current tip | [optional] 

### Return type

[**TxResponse**](TxResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **tx_signers**
> TxDetailsResponse tx_signers(hash, height=height)



Returns the signers for a provided inbound or outbound hash.

### Example
```python
from __future__ import print_function
import time
import xchainpy2_thornode
from xchainpy2_thornode.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = xchainpy2_thornode.TransactionsApi()
hash = 'hash_example' # str | 
height = 789 # int | optional block height, defaults to current tip (optional)

try:
    api_response = api_instance.tx_signers(hash, height=height)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling TransactionsApi->tx_signers: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **hash** | **str**|  | 
 **height** | **int**| optional block height, defaults to current tip | [optional] 

### Return type

[**TxDetailsResponse**](TxDetailsResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **tx_signers_old**
> TxSignersResponse tx_signers_old(hash, height=height)



Deprecated - migrate to /thorchain/tx/details.

### Example
```python
from __future__ import print_function
import time
import xchainpy2_thornode
from xchainpy2_thornode.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = xchainpy2_thornode.TransactionsApi()
hash = 'hash_example' # str | 
height = 789 # int | optional block height, defaults to current tip (optional)

try:
    api_response = api_instance.tx_signers_old(hash, height=height)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling TransactionsApi->tx_signers_old: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **hash** | **str**|  | 
 **height** | **int**| optional block height, defaults to current tip | [optional] 

### Return type

[**TxSignersResponse**](TxSignersResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **tx_stages**
> TxStagesResponse tx_stages(hash, height=height)



Returns the processing stages of a provided inbound hash.

### Example
```python
from __future__ import print_function
import time
import xchainpy2_thornode
from xchainpy2_thornode.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = xchainpy2_thornode.TransactionsApi()
hash = 'hash_example' # str | 
height = 789 # int | optional block height, defaults to current tip (optional)

try:
    api_response = api_instance.tx_stages(hash, height=height)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling TransactionsApi->tx_stages: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **hash** | **str**|  | 
 **height** | **int**| optional block height, defaults to current tip | [optional] 

### Return type

[**TxStagesResponse**](TxStagesResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **tx_status**
> TxStatusResponse tx_status(hash, height=height)



Returns the status of a provided inbound hash.

### Example
```python
from __future__ import print_function
import time
import xchainpy2_thornode
from xchainpy2_thornode.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = xchainpy2_thornode.TransactionsApi()
hash = 'hash_example' # str | 
height = 789 # int | optional block height, defaults to current tip (optional)

try:
    api_response = api_instance.tx_status(hash, height=height)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling TransactionsApi->tx_status: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **hash** | **str**|  | 
 **height** | **int**| optional block height, defaults to current tip | [optional] 

### Return type

[**TxStatusResponse**](TxStatusResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


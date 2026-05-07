# xchainpy2_thornode.ReferenceMemosApi

All URIs are relative to *https://gateway.liquify.com/chain/thorchain_api*

Method | HTTP request | Description
------------- | ------------- | -------------
[**reference_memo**](ReferenceMemosApi.md#reference_memo) | **GET** /thorchain/memo/{asset}/{reference} | 
[**reference_memo_by_hash**](ReferenceMemosApi.md#reference_memo_by_hash) | **GET** /thorchain/memo/{hash} | 
[**reference_memo_check**](ReferenceMemosApi.md#reference_memo_check) | **GET** /thorchain/memo/check/{asset}/{amount} | 

# **reference_memo**
> ReferenceMemoResponse reference_memo(asset, reference, height=height)



Returns the memoless transaction memo for the provided asset and reference number.

### Example
```python
from __future__ import print_function
import time
import xchainpy2_thornode
from xchainpy2_thornode.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = xchainpy2_thornode.ReferenceMemosApi()
asset = 'asset_example' # str | 
reference = 'reference_example' # str | the reference number to lookup
height = 789 # int | optional block height, defaults to current tip (optional)

try:
    api_response = api_instance.reference_memo(asset, reference, height=height)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ReferenceMemosApi->reference_memo: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **asset** | **str**|  | 
 **reference** | **str**| the reference number to lookup | 
 **height** | **int**| optional block height, defaults to current tip | [optional] 

### Return type

[**ReferenceMemoResponse**](ReferenceMemoResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **reference_memo_by_hash**
> ReferenceMemoResponse reference_memo_by_hash(hash, height=height)



Returns the memoless transaction memo for the provided reference hash.

### Example
```python
from __future__ import print_function
import time
import xchainpy2_thornode
from xchainpy2_thornode.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = xchainpy2_thornode.ReferenceMemosApi()
hash = 'hash_example' # str | 
height = 789 # int | optional block height, defaults to current tip (optional)

try:
    api_response = api_instance.reference_memo_by_hash(hash, height=height)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ReferenceMemosApi->reference_memo_by_hash: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **hash** | **str**|  | 
 **height** | **int**| optional block height, defaults to current tip | [optional] 

### Return type

[**ReferenceMemoResponse**](ReferenceMemoResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **reference_memo_check**
> ReferenceMemoPreflightResponse reference_memo_check(asset, amount, height=height)



Pre-flight check for memoless transactions. Returns what reference would be extracted from the amount and whether it's available for registration.

### Example
```python
from __future__ import print_function
import time
import xchainpy2_thornode
from xchainpy2_thornode.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = xchainpy2_thornode.ReferenceMemosApi()
asset = 'asset_example' # str | 
amount = 'amount_example' # str | the transaction amount in base units to check
height = 789 # int | optional block height, defaults to current tip (optional)

try:
    api_response = api_instance.reference_memo_check(asset, amount, height=height)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling ReferenceMemosApi->reference_memo_check: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **asset** | **str**|  | 
 **amount** | **str**| the transaction amount in base units to check | 
 **height** | **int**| optional block height, defaults to current tip | [optional] 

### Return type

[**ReferenceMemoPreflightResponse**](ReferenceMemoPreflightResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


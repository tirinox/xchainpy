# xchainpy2_mayanode.InvariantsApi

All URIs are relative to */*

Method | HTTP request | Description
------------- | ------------- | -------------
[**invariant**](InvariantsApi.md#invariant) | **GET** /mayachain/invariant/{invariant} | 
[**invariants**](InvariantsApi.md#invariants) | **GET** /mayachain/invariants | 

# **invariant**
> InvariantResponse invariant(invariant, height=height)



Returns result of running the given invariant.

### Example
```python
from __future__ import print_function
import time
import xchainpy2_mayanode
from xchainpy2_mayanode.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = xchainpy2_mayanode.InvariantsApi()
invariant = 'invariant_example' # str | 
height = 789 # int | optional block height, defaults to current tip (optional)

try:
    api_response = api_instance.invariant(invariant, height=height)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling InvariantsApi->invariant: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **invariant** | **str**|  | 
 **height** | **int**| optional block height, defaults to current tip | [optional] 

### Return type

[**InvariantResponse**](InvariantResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **invariants**
> InvariantsResponse invariants(height=height)



Returns a list of available invariants.

### Example
```python
from __future__ import print_function
import time
import xchainpy2_mayanode
from xchainpy2_mayanode.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = xchainpy2_mayanode.InvariantsApi()
height = 789 # int | optional block height, defaults to current tip (optional)

try:
    api_response = api_instance.invariants(height=height)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling InvariantsApi->invariants: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **height** | **int**| optional block height, defaults to current tip | [optional] 

### Return type

[**InvariantsResponse**](InvariantsResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


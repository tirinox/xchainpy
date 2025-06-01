# xchainpy2_thornode.TCYClaimersApi

All URIs are relative to */*

Method | HTTP request | Description
------------- | ------------- | -------------
[**tcy_claimer**](TCYClaimersApi.md#tcy_claimer) | **GET** /thorchain/tcy_claimer/{address} | 
[**tcy_claimers**](TCYClaimersApi.md#tcy_claimers) | **GET** /thorchain/tcy_claimers | 

# **tcy_claimer**
> TCYClaimer tcy_claimer(address, height=height)



Returns the tcy claimer information for an address.

### Example
```python
from __future__ import print_function
import time
import xchainpy2_thornode
from xchainpy2_thornode.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = xchainpy2_thornode.TCYClaimersApi()
address = 'address_example' # str | 
height = 789 # int | optional block height, defaults to current tip (optional)

try:
    api_response = api_instance.tcy_claimer(address, height=height)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling TCYClaimersApi->tcy_claimer: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **address** | **str**|  | 
 **height** | **int**| optional block height, defaults to current tip | [optional] 

### Return type

[**TCYClaimer**](TCYClaimer.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **tcy_claimers**
> list[TCYClaimerSummary] tcy_claimers(height=height)



Returns all tcy claimers information.

### Example
```python
from __future__ import print_function
import time
import xchainpy2_thornode
from xchainpy2_thornode.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = xchainpy2_thornode.TCYClaimersApi()
height = 789 # int | optional block height, defaults to current tip (optional)

try:
    api_response = api_instance.tcy_claimers(height=height)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling TCYClaimersApi->tcy_claimers: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **height** | **int**| optional block height, defaults to current tip | [optional] 

### Return type

[**list[TCYClaimerSummary]**](TCYClaimerSummary.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


# xchainpy2_thornode.BankApi

All URIs are relative to */*

Method | HTTP request | Description
------------- | ------------- | -------------
[**balances**](BankApi.md#balances) | **GET** /bank/balances/{address} | 

# **balances**
> BalancesResponse balances(address, height=height)



Returns balances for the provided address.

### Example
```python
from __future__ import print_function
import time
import xchainpy2_thornode
from xchainpy2_thornode.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = xchainpy2_thornode.BankApi()
address = 'address_example' # str | 
height = 789 # int | optional block height, defaults to current tip (optional)

try:
    api_response = api_instance.balances(address, height=height)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling BankApi->balances: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **address** | **str**|  | 
 **height** | **int**| optional block height, defaults to current tip | [optional] 

### Return type

[**BalancesResponse**](BalancesResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


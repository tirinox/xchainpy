# xchainpy2_thornode.TradeAccountApi

All URIs are relative to */*

Method | HTTP request | Description
------------- | ------------- | -------------
[**trade_account**](TradeAccountApi.md#trade_account) | **GET** /thorchain/trade/account/{address} | 

# **trade_account**
> TradeAccountsResponse trade_account(address, height=height)



Returns the units and depth of a trade account

### Example
```python
from __future__ import print_function
import time
import xchainpy2_thornode
from xchainpy2_thornode.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = xchainpy2_thornode.TradeAccountApi()
address = 'address_example' # str | 
height = 789 # int | optional block height, defaults to current tip (optional)

try:
    api_response = api_instance.trade_account(address, height=height)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling TradeAccountApi->trade_account: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **address** | **str**|  | 
 **height** | **int**| optional block height, defaults to current tip | [optional] 

### Return type

[**TradeAccountsResponse**](TradeAccountsResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


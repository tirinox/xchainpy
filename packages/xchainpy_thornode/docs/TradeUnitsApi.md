# xchainpy2_thornode.TradeUnitsApi

All URIs are relative to */*

Method | HTTP request | Description
------------- | ------------- | -------------
[**trade_units**](TradeUnitsApi.md#trade_units) | **GET** /thorchain/trade/units | 

# **trade_units**
> list[TradeUnitResponse] trade_units(height=height)



Returns the total units and depth for each trade asset

### Example
```python
from __future__ import print_function
import time
import xchainpy2_thornode
from xchainpy2_thornode.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = xchainpy2_thornode.TradeUnitsApi()
height = 789 # int | optional block height, defaults to current tip (optional)

try:
    api_response = api_instance.trade_units(height=height)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling TradeUnitsApi->trade_units: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **height** | **int**| optional block height, defaults to current tip | [optional] 

### Return type

[**list[TradeUnitResponse]**](TradeUnitResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


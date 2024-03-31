# xchainpy2_thornode.TradeUnitApi

All URIs are relative to */*

Method | HTTP request | Description
------------- | ------------- | -------------
[**trade_unit**](TradeUnitApi.md#trade_unit) | **GET** /thorchain/trade/unit/{asset} | 

# **trade_unit**
> TradeUnitResponse trade_unit(asset, height=height)



Returns the total units and depth of a trade asset

### Example
```python
from __future__ import print_function
import time
import xchainpy2_thornode
from xchainpy2_thornode.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = xchainpy2_thornode.TradeUnitApi()
asset = 'asset_example' # str | 
height = 789 # int | optional block height, defaults to current tip (optional)

try:
    api_response = api_instance.trade_unit(asset, height=height)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling TradeUnitApi->trade_unit: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **asset** | **str**|  | 
 **height** | **int**| optional block height, defaults to current tip | [optional] 

### Return type

[**TradeUnitResponse**](TradeUnitResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


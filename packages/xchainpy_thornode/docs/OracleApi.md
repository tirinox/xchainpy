# xchainpy2_thornode.OracleApi

All URIs are relative to */*

Method | HTTP request | Description
------------- | ------------- | -------------
[**oracle_price**](OracleApi.md#oracle_price) | **GET** /thorchain/oracle/price/{symbol} | 
[**oracle_prices**](OracleApi.md#oracle_prices) | **GET** /thorchain/oracle/prices | 

# **oracle_price**
> OraclePriceResponse oracle_price(symbol, height=height)



Returns oracle price for a symbol.

### Example
```python
from __future__ import print_function
import time
import xchainpy2_thornode
from xchainpy2_thornode.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = xchainpy2_thornode.OracleApi()
symbol = 'symbol_example' # str | 
height = 789 # int | optional block height, defaults to current tip (optional)

try:
    api_response = api_instance.oracle_price(symbol, height=height)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling OracleApi->oracle_price: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **symbol** | **str**|  | 
 **height** | **int**| optional block height, defaults to current tip | [optional] 

### Return type

[**OraclePriceResponse**](OraclePriceResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **oracle_prices**
> OraclePricesResponse oracle_prices(height=height)



Returns all available oracle prices.

### Example
```python
from __future__ import print_function
import time
import xchainpy2_thornode
from xchainpy2_thornode.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = xchainpy2_thornode.OracleApi()
height = 789 # int | optional block height, defaults to current tip (optional)

try:
    api_response = api_instance.oracle_prices(height=height)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling OracleApi->oracle_prices: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **height** | **int**| optional block height, defaults to current tip | [optional] 

### Return type

[**OraclePricesResponse**](OraclePricesResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


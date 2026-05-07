# xchainpy2_thornode.SupplyApi

All URIs are relative to *https://gateway.liquify.com/chain/thorchain_api*

Method | HTTP request | Description
------------- | ------------- | -------------
[**supply**](SupplyApi.md#supply) | **GET** /thorchain/supply | 
[**supply_cmc**](SupplyApi.md#supply_cmc) | **GET** /thorchain/supply/cmc | 

# **supply**
> SupplyResponse supply(height=height)



Returns the RUNE supply breakdown.

### Example
```python
from __future__ import print_function
import time
import xchainpy2_thornode
from xchainpy2_thornode.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = xchainpy2_thornode.SupplyApi()
height = 789 # int | optional block height, defaults to current tip (optional)

try:
    api_response = api_instance.supply(height=height)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling SupplyApi->supply: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **height** | **int**| optional block height, defaults to current tip | [optional] 

### Return type

[**SupplyResponse**](SupplyResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **supply_cmc**
> int supply_cmc(type, asset=asset)



Returns a single supply value as plain text for CoinMarketCap integration.

### Example
```python
from __future__ import print_function
import time
import xchainpy2_thornode
from xchainpy2_thornode.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = xchainpy2_thornode.SupplyApi()
type = 'type_example' # str | The type of supply value to return.
asset = 'asset_example' # str | The asset to query supply for (default rune). (optional)

try:
    api_response = api_instance.supply_cmc(type, asset=asset)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling SupplyApi->supply_cmc: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **type** | **str**| The type of supply value to return. | 
 **asset** | **str**| The asset to query supply for (default rune). | [optional] 

### Return type

**int**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: text/plain

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


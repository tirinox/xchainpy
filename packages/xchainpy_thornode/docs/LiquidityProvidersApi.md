# thornode_client.LiquidityProvidersApi

All URIs are relative to */*

Method | HTTP request | Description
------------- | ------------- | -------------
[**liquidity_provider**](LiquidityProvidersApi.md#liquidity_provider) | **GET** /thorchain/pool/{asset}/liquidity_provider/{address} | 
[**liquidity_providers**](LiquidityProvidersApi.md#liquidity_providers) | **GET** /thorchain/pool/{asset}/liquidity_providers | 

# **liquidity_provider**
> LiquidityProviderResponse liquidity_provider(asset, address, height=height)



Returns the liquidity provider information for an address and asset.

### Example
```python
from __future__ import print_function
import time
import thornode_client
from thornode_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = thornode_client.LiquidityProvidersApi()
asset = 'asset_example' # str | 
address = 'address_example' # str | 
height = 789 # int | optional block height, defaults to current tip (optional)

try:
    api_response = api_instance.liquidity_provider(asset, address, height=height)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling LiquidityProvidersApi->liquidity_provider: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **asset** | **str**|  | 
 **address** | **str**|  | 
 **height** | **int**| optional block height, defaults to current tip | [optional] 

### Return type

[**LiquidityProviderResponse**](LiquidityProviderResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **liquidity_providers**
> LiquidityProvidersResponse liquidity_providers(asset, height=height)



Returns all liquidity provider information for an asset.

### Example
```python
from __future__ import print_function
import time
import thornode_client
from thornode_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = thornode_client.LiquidityProvidersApi()
asset = 'asset_example' # str | 
height = 789 # int | optional block height, defaults to current tip (optional)

try:
    api_response = api_instance.liquidity_providers(asset, height=height)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling LiquidityProvidersApi->liquidity_providers: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **asset** | **str**|  | 
 **height** | **int**| optional block height, defaults to current tip | [optional] 

### Return type

[**LiquidityProvidersResponse**](LiquidityProvidersResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


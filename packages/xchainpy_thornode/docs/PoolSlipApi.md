# xchainpy2_thornode.PoolSlipApi

All URIs are relative to */*

Method | HTTP request | Description
------------- | ------------- | -------------
[**poolslip**](PoolSlipApi.md#poolslip) | **GET** /thorchain/slip/{asset} | 
[**poolslips**](PoolSlipApi.md#poolslips) | **GET** /thorchain/slips | 

# **poolslip**
> list[InlineResponse200] poolslip(asset, height=height)



Returns the pool slip information for the provided asset.

### Example
```python
from __future__ import print_function
import time
import xchainpy2_thornode
from xchainpy2_thornode.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = xchainpy2_thornode.PoolSlipApi()
asset = 'asset_example' # str | 
height = 789 # int | optional block height, defaults to current tip (optional)

try:
    api_response = api_instance.poolslip(asset, height=height)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling PoolSlipApi->poolslip: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **asset** | **str**|  | 
 **height** | **int**| optional block height, defaults to current tip | [optional] 

### Return type

[**list[InlineResponse200]**](InlineResponse200.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **poolslips**
> list[InlineResponse200] poolslips(height=height)



Returns the pool slip information for all Available Layer 1 pool assets.

### Example
```python
from __future__ import print_function
import time
import xchainpy2_thornode
from xchainpy2_thornode.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = xchainpy2_thornode.PoolSlipApi()
height = 789 # int | optional block height, defaults to current tip (optional)

try:
    api_response = api_instance.poolslips(height=height)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling PoolSlipApi->poolslips: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **height** | **int**| optional block height, defaults to current tip | [optional] 

### Return type

[**list[InlineResponse200]**](InlineResponse200.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


# xchainpy2_thornode.NodesApi

All URIs are relative to */*

Method | HTTP request | Description
------------- | ------------- | -------------
[**node**](NodesApi.md#node) | **GET** /thorchain/node/{address} | 
[**nodes**](NodesApi.md#nodes) | **GET** /thorchain/nodes | 

# **node**
> NodeResponse node(address, height=height)



Returns node information for the provided node address.

### Example
```python
from __future__ import print_function
import time
import xchainpy2_thornode
from xchainpy2_thornode.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = xchainpy2_thornode.NodesApi()
address = 'address_example' # str | 
height = 789 # int | optional block height, defaults to current tip (optional)

try:
    api_response = api_instance.node(address, height=height)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling NodesApi->node: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **address** | **str**|  | 
 **height** | **int**| optional block height, defaults to current tip | [optional] 

### Return type

[**NodeResponse**](NodeResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **nodes**
> NodesResponse nodes(height=height)



Returns node information for all registered validators.

### Example
```python
from __future__ import print_function
import time
import xchainpy2_thornode
from xchainpy2_thornode.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = xchainpy2_thornode.NodesApi()
height = 789 # int | optional block height, defaults to current tip (optional)

try:
    api_response = api_instance.nodes(height=height)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling NodesApi->nodes: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **height** | **int**| optional block height, defaults to current tip | [optional] 

### Return type

[**NodesResponse**](NodesResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


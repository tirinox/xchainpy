# xchainpy2_mayanode.NodesApi

All URIs are relative to */*

Method | HTTP request | Description
------------- | ------------- | -------------
[**node**](NodesApi.md#node) | **GET** /mayachain/node/{address} | 
[**nodes**](NodesApi.md#nodes) | **GET** /mayachain/nodes | 

# **node**
> Node node(address, height=height)



Returns node information for the provided node address.

### Example
```python
from __future__ import print_function
import time
import xchainpy2_mayanode
from xchainpy2_mayanode.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = xchainpy2_mayanode.NodesApi()
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

[**Node**](Node.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **nodes**
> list[Node] nodes(height=height)



Returns node information for all registered validators.

### Example
```python
from __future__ import print_function
import time
import xchainpy2_mayanode
from xchainpy2_mayanode.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = xchainpy2_mayanode.NodesApi()
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

[**list[Node]**](Node.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


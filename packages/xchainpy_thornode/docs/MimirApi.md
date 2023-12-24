# xchainpy2_thornode.MimirApi

All URIs are relative to */*

Method | HTTP request | Description
------------- | ------------- | -------------
[**mimir**](MimirApi.md#mimir) | **GET** /thorchain/mimir | 
[**mimir_admin**](MimirApi.md#mimir_admin) | **GET** /thorchain/mimir/admin | 
[**mimir_key**](MimirApi.md#mimir_key) | **GET** /thorchain/mimir/key/{key} | 
[**mimir_node**](MimirApi.md#mimir_node) | **GET** /thorchain/mimir/node/{address} | 
[**mimir_nodes**](MimirApi.md#mimir_nodes) | **GET** /thorchain/mimir/nodes_all | 
[**mimir_v2**](MimirApi.md#mimir_v2) | **GET** /thorchain/mimirV2 | 
[**mimir_v2_ids**](MimirApi.md#mimir_v2_ids) | **GET** /thorchain/mimirV2/ids | 

# **mimir**
> MimirResponse mimir(height=height)



Returns current active mimir configuration.

### Example
```python
from __future__ import print_function
import time
import xchainpy2_thornode
from xchainpy2_thornode.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = xchainpy2_thornode.MimirApi()
height = 789 # int | optional block height, defaults to current tip (optional)

try:
    api_response = api_instance.mimir(height=height)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling MimirApi->mimir: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **height** | **int**| optional block height, defaults to current tip | [optional] 

### Return type

[**MimirResponse**](MimirResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **mimir_admin**
> MimirResponse mimir_admin(height=height)



Returns current admin mimir configuration.

### Example
```python
from __future__ import print_function
import time
import xchainpy2_thornode
from xchainpy2_thornode.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = xchainpy2_thornode.MimirApi()
height = 789 # int | optional block height, defaults to current tip (optional)

try:
    api_response = api_instance.mimir_admin(height=height)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling MimirApi->mimir_admin: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **height** | **int**| optional block height, defaults to current tip | [optional] 

### Return type

[**MimirResponse**](MimirResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **mimir_key**
> int mimir_key(key, height=height)



Returns current active mimir configuration for the provided key.

### Example
```python
from __future__ import print_function
import time
import xchainpy2_thornode
from xchainpy2_thornode.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = xchainpy2_thornode.MimirApi()
key = 'key_example' # str | the mimir key to lookup
height = 789 # int | optional block height, defaults to current tip (optional)

try:
    api_response = api_instance.mimir_key(key, height=height)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling MimirApi->mimir_key: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **key** | **str**| the mimir key to lookup | 
 **height** | **int**| optional block height, defaults to current tip | [optional] 

### Return type

**int**

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **mimir_node**
> MimirResponse mimir_node(address, height=height)



Returns current node mimir configuration for the provided node address.

### Example
```python
from __future__ import print_function
import time
import xchainpy2_thornode
from xchainpy2_thornode.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = xchainpy2_thornode.MimirApi()
address = 'address_example' # str | 
height = 789 # int | optional block height, defaults to current tip (optional)

try:
    api_response = api_instance.mimir_node(address, height=height)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling MimirApi->mimir_node: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **address** | **str**|  | 
 **height** | **int**| optional block height, defaults to current tip | [optional] 

### Return type

[**MimirResponse**](MimirResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **mimir_nodes**
> MimirNodesResponse mimir_nodes(height=height)



Returns current node mimir votes.

### Example
```python
from __future__ import print_function
import time
import xchainpy2_thornode
from xchainpy2_thornode.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = xchainpy2_thornode.MimirApi()
height = 789 # int | optional block height, defaults to current tip (optional)

try:
    api_response = api_instance.mimir_nodes(height=height)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling MimirApi->mimir_nodes: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **height** | **int**| optional block height, defaults to current tip | [optional] 

### Return type

[**MimirNodesResponse**](MimirNodesResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **mimir_v2**
> MimirResponse mimir_v2(height=height)



Returns current mimir V2 configuration.

### Example
```python
from __future__ import print_function
import time
import xchainpy2_thornode
from xchainpy2_thornode.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = xchainpy2_thornode.MimirApi()
height = 789 # int | optional block height, defaults to current tip (optional)

try:
    api_response = api_instance.mimir_v2(height=height)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling MimirApi->mimir_v2: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **height** | **int**| optional block height, defaults to current tip | [optional] 

### Return type

[**MimirResponse**](MimirResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **mimir_v2_ids**
> MimirV2IDsResponse mimir_v2_ids(height=height)



Returns mapping of mimir V2 IDs to name.

### Example
```python
from __future__ import print_function
import time
import xchainpy2_thornode
from xchainpy2_thornode.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = xchainpy2_thornode.MimirApi()
height = 789 # int | optional block height, defaults to current tip (optional)

try:
    api_response = api_instance.mimir_v2_ids(height=height)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling MimirApi->mimir_v2_ids: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **height** | **int**| optional block height, defaults to current tip | [optional] 

### Return type

[**MimirV2IDsResponse**](MimirV2IDsResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


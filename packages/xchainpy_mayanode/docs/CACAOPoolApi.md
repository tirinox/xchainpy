# xchainpy2_mayanode.CACAOPoolApi

All URIs are relative to */*

Method | HTTP request | Description
------------- | ------------- | -------------
[**cacao_pool**](CACAOPoolApi.md#cacao_pool) | **GET** /mayachain/cacaopool | 
[**cacao_provider**](CACAOPoolApi.md#cacao_provider) | **GET** /mayachain/cacao_provider/{address} | 
[**cacao_providers**](CACAOPoolApi.md#cacao_providers) | **GET** /mayachain/cacao_providers | 

# **cacao_pool**
> CACAOPoolResponse cacao_pool(height=height)



Returns the pool information for the CACAO pool.

### Example
```python
from __future__ import print_function
import time
import xchainpy2_mayanode
from xchainpy2_mayanode.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = xchainpy2_mayanode.CACAOPoolApi()
height = 789 # int | optional block height, defaults to current tip (optional)

try:
    api_response = api_instance.cacao_pool(height=height)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling CACAOPoolApi->cacao_pool: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **height** | **int**| optional block height, defaults to current tip | [optional] 

### Return type

[**CACAOPoolResponse**](CACAOPoolResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **cacao_provider**
> CACAOProvider cacao_provider(address, height=height)



Returns the CACAO Provider information for an address.

### Example
```python
from __future__ import print_function
import time
import xchainpy2_mayanode
from xchainpy2_mayanode.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = xchainpy2_mayanode.CACAOPoolApi()
address = 'address_example' # str | 
height = 789 # int | optional block height, defaults to current tip (optional)

try:
    api_response = api_instance.cacao_provider(address, height=height)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling CACAOPoolApi->cacao_provider: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **address** | **str**|  | 
 **height** | **int**| optional block height, defaults to current tip | [optional] 

### Return type

[**CACAOProvider**](CACAOProvider.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **cacao_providers**
> list[CACAOProvider] cacao_providers(height=height)



Returns all CACAO Providers.

### Example
```python
from __future__ import print_function
import time
import xchainpy2_mayanode
from xchainpy2_mayanode.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = xchainpy2_mayanode.CACAOPoolApi()
height = 789 # int | optional block height, defaults to current tip (optional)

try:
    api_response = api_instance.cacao_providers(height=height)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling CACAOPoolApi->cacao_providers: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **height** | **int**| optional block height, defaults to current tip | [optional] 

### Return type

[**list[CACAOProvider]**](CACAOProvider.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


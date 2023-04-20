# mayanode_client.TransactionsApi

All URIs are relative to */*

Method | HTTP request | Description
------------- | ------------- | -------------
[**tx**](TransactionsApi.md#tx) | **GET** /mayachain/tx/{hash} | 
[**tx_signers**](TransactionsApi.md#tx_signers) | **GET** /mayachain/tx/{hash}/signers | 

# **tx**
> TxResponse tx(hash, height=height)



Returns the observed transaction for a provided inbound or outbound hash.

### Example
```python
from __future__ import print_function
import time
import mayanode_client
from mayanode_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = mayanode_client.TransactionsApi()
hash = 'hash_example' # str | 
height = 789 # int | optional block height, defaults to current tip (optional)

try:
    api_response = api_instance.tx(hash, height=height)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling TransactionsApi->tx: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **hash** | **str**|  | 
 **height** | **int**| optional block height, defaults to current tip | [optional] 

### Return type

[**TxResponse**](TxResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **tx_signers**
> TxSignersResponse tx_signers(hash, height=height)



Returns the signers for a provided inbound or outbound hash.

### Example
```python
from __future__ import print_function
import time
import mayanode_client
from mayanode_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = mayanode_client.TransactionsApi()
hash = 'hash_example' # str | 
height = 789 # int | optional block height, defaults to current tip (optional)

try:
    api_response = api_instance.tx_signers(hash, height=height)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling TransactionsApi->tx_signers: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **hash** | **str**|  | 
 **height** | **int**| optional block height, defaults to current tip | [optional] 

### Return type

[**TxSignersResponse**](TxSignersResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


# xchainpy2_thornode.BorrowersApi

All URIs are relative to */*

Method | HTTP request | Description
------------- | ------------- | -------------
[**borrower**](BorrowersApi.md#borrower) | **GET** /thorchain/pool/{asset}/borrower/{address} | 
[**borrowers**](BorrowersApi.md#borrowers) | **GET** /thorchain/pool/{asset}/borrowers | 

# **borrower**
> Borrower borrower(asset, address, height=height)



Returns the borrower position given the pool and address.

### Example
```python
from __future__ import print_function
import time
import xchainpy2_thornode
from xchainpy2_thornode.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = xchainpy2_thornode.BorrowersApi()
asset = 'asset_example' # str | 
address = 'address_example' # str | 
height = 789 # int | optional block height, defaults to current tip (optional)

try:
    api_response = api_instance.borrower(asset, address, height=height)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling BorrowersApi->borrower: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **asset** | **str**|  | 
 **address** | **str**|  | 
 **height** | **int**| optional block height, defaults to current tip | [optional] 

### Return type

[**Borrower**](Borrower.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **borrowers**
> list[Borrower] borrowers(asset, height=height)



Returns all borrowers for the given pool.

### Example
```python
from __future__ import print_function
import time
import xchainpy2_thornode
from xchainpy2_thornode.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = xchainpy2_thornode.BorrowersApi()
asset = 'asset_example' # str | 
height = 789 # int | optional block height, defaults to current tip (optional)

try:
    api_response = api_instance.borrowers(asset, height=height)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling BorrowersApi->borrowers: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **asset** | **str**|  | 
 **height** | **int**| optional block height, defaults to current tip | [optional] 

### Return type

[**list[Borrower]**](Borrower.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


# xchainpy2_thornode.SmartContractsApi

All URIs are relative to *https://gateway.liquify.com/chain/thorchain_api*

Method | HTTP request | Description
------------- | ------------- | -------------
[**contract_info**](SmartContractsApi.md#contract_info) | **GET** /thorchain/contract/{address} | 
[**contract_infos**](SmartContractsApi.md#contract_infos) | **GET** /thorchain/contracts | 

# **contract_info**
> ContractInfoResponse contract_info(address, height=height)



Returns type and version from `contract_info` for requested address

### Example
```python
from __future__ import print_function
import time
import xchainpy2_thornode
from xchainpy2_thornode.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = xchainpy2_thornode.SmartContractsApi()
address = 'address_example' # str | 
height = 789 # int | optional block height, defaults to current tip (optional)

try:
    api_response = api_instance.contract_info(address, height=height)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling SmartContractsApi->contract_info: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **address** | **str**|  | 
 **height** | **int**| optional block height, defaults to current tip | [optional] 

### Return type

[**ContractInfoResponse**](ContractInfoResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **contract_infos**
> ContractInfosResponse contract_infos(height=height, contract=contract, version=version)



Returns type and version for all contracts with stored `contract_info`

### Example
```python
from __future__ import print_function
import time
import xchainpy2_thornode
from xchainpy2_thornode.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = xchainpy2_thornode.SmartContractsApi()
height = 789 # int | optional block height, defaults to current tip (optional)
contract = 'contract_example' # str | optional contract type prefix to filter results (optional)
version = 'version_example' # str | optional contract version prefix to filter results (optional)

try:
    api_response = api_instance.contract_infos(height=height, contract=contract, version=version)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling SmartContractsApi->contract_infos: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **height** | **int**| optional block height, defaults to current tip | [optional] 
 **contract** | **str**| optional contract type prefix to filter results | [optional] 
 **version** | **str**| optional contract version prefix to filter results | [optional] 

### Return type

[**ContractInfosResponse**](ContractInfosResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


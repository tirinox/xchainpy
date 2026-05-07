# xchainpy2_thornode.TCYStakersApi

All URIs are relative to *https://gateway.liquify.com/chain/thorchain_api*

Method | HTTP request | Description
------------- | ------------- | -------------
[**tcy_staker**](TCYStakersApi.md#tcy_staker) | **GET** /thorchain/tcy_staker/{address} | 
[**tcy_stakers**](TCYStakersApi.md#tcy_stakers) | **GET** /thorchain/tcy_stakers | 

# **tcy_staker**
> TCYStaker tcy_staker(address, height=height)



Returns the tcy staker information for an address.

### Example
```python
from __future__ import print_function
import time
import xchainpy2_thornode
from xchainpy2_thornode.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = xchainpy2_thornode.TCYStakersApi()
address = 'address_example' # str | 
height = 789 # int | optional block height, defaults to current tip (optional)

try:
    api_response = api_instance.tcy_staker(address, height=height)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling TCYStakersApi->tcy_staker: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **address** | **str**|  | 
 **height** | **int**| optional block height, defaults to current tip | [optional] 

### Return type

[**TCYStaker**](TCYStaker.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **tcy_stakers**
> list[TCYStakerSummary] tcy_stakers(height=height)



Returns all tcy stakers information.

### Example
```python
from __future__ import print_function
import time
import xchainpy2_thornode
from xchainpy2_thornode.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = xchainpy2_thornode.TCYStakersApi()
height = 789 # int | optional block height, defaults to current tip (optional)

try:
    api_response = api_instance.tcy_stakers(height=height)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling TCYStakersApi->tcy_stakers: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **height** | **int**| optional block height, defaults to current tip | [optional] 

### Return type

[**list[TCYStakerSummary]**](TCYStakerSummary.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


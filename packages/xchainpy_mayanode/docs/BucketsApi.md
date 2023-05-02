# xchainpy2_mayanode.BucketsApi

All URIs are relative to */*

Method | HTTP request | Description
------------- | ------------- | -------------
[**bucket**](BucketsApi.md#bucket) | **GET** /mayachain/bucket/{asset} | 
[**buckets**](BucketsApi.md#buckets) | **GET** /mayachain/buckets | 

# **bucket**
> Bucket bucket(asset, height=height)



Returns the bucket information for the provided asset.

### Example
```python
from __future__ import print_function
import time
import xchainpy2_mayanode
from xchainpy2_mayanode.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = xchainpy2_mayanode.BucketsApi()
asset = 'asset_example' # str | 
height = 789 # int | optional block height, defaults to current tip (optional)

try:
    api_response = api_instance.bucket(asset, height=height)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling BucketsApi->bucket: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **asset** | **str**|  | 
 **height** | **int**| optional block height, defaults to current tip | [optional] 

### Return type

[**Bucket**](Bucket.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **buckets**
> list[Bucket] buckets(height=height)



Returns the bucket information for all assets.

### Example
```python
from __future__ import print_function
import time
import xchainpy2_mayanode
from xchainpy2_mayanode.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = xchainpy2_mayanode.BucketsApi()
height = 789 # int | optional block height, defaults to current tip (optional)

try:
    api_response = api_instance.buckets(height=height)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling BucketsApi->buckets: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **height** | **int**| optional block height, defaults to current tip | [optional] 

### Return type

[**list[Bucket]**](Bucket.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


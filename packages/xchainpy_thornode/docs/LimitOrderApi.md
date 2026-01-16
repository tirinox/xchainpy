# xchainpy2_thornode.LimitOrderApi

All URIs are relative to */*

Method | HTTP request | Description
------------- | ------------- | -------------
[**quotelimit**](LimitOrderApi.md#quotelimit) | **GET** /thorchain/quote/limit | 

# **quotelimit**
> QuoteLimitResponse quotelimit(height=height, from_asset=from_asset, to_asset=to_asset, amount=amount, destination=destination, refund_address=refund_address, custom_ttl=custom_ttl, streaming_quantity=streaming_quantity, affiliate_bps=affiliate_bps, affiliate=affiliate)



Provide a limit order quote and memo for the provided limit order

### Example
```python
from __future__ import print_function
import time
import xchainpy2_thornode
from xchainpy2_thornode.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = xchainpy2_thornode.LimitOrderApi()
height = 789 # int | optional block height, defaults to current tip (optional)
from_asset = 'from_asset_example' # str | the source asset (optional)
to_asset = 'to_asset_example' # str | the target asset (optional)
amount = 789 # int | the source asset amount in 1e8 decimals (optional)
destination = 'destination_example' # str | the destination address, required to generate memo (optional)
refund_address = 'refund_address_example' # str | the refund address, refunds will be sent here if the swap fails (optional)
custom_ttl = 789 # int | the custom TTL in blocks for limit orders (optional)
streaming_quantity = 789 # int | the quantity of swaps within a streaming swap (optional)
affiliate_bps = 789 # int | the affiliate fee in basis points (optional)
affiliate = 'affiliate_example' # str | the affiliate (address or thorname) (optional)

try:
    api_response = api_instance.quotelimit(height=height, from_asset=from_asset, to_asset=to_asset, amount=amount, destination=destination, refund_address=refund_address, custom_ttl=custom_ttl, streaming_quantity=streaming_quantity, affiliate_bps=affiliate_bps, affiliate=affiliate)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling LimitOrderApi->quotelimit: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **height** | **int**| optional block height, defaults to current tip | [optional] 
 **from_asset** | **str**| the source asset | [optional] 
 **to_asset** | **str**| the target asset | [optional] 
 **amount** | **int**| the source asset amount in 1e8 decimals | [optional] 
 **destination** | **str**| the destination address, required to generate memo | [optional] 
 **refund_address** | **str**| the refund address, refunds will be sent here if the swap fails | [optional] 
 **custom_ttl** | **int**| the custom TTL in blocks for limit orders | [optional] 
 **streaming_quantity** | **int**| the quantity of swaps within a streaming swap | [optional] 
 **affiliate_bps** | **int**| the affiliate fee in basis points | [optional] 
 **affiliate** | **str**| the affiliate (address or thorname) | [optional] 

### Return type

[**QuoteLimitResponse**](QuoteLimitResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


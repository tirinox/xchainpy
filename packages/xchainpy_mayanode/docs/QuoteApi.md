# mayanode_client.QuoteApi

All URIs are relative to */*

Method | HTTP request | Description
------------- | ------------- | -------------
[**quotesaverdeposit**](QuoteApi.md#quotesaverdeposit) | **GET** /mayachain/quote/saver/deposit | 
[**quotesaverwithdraw**](QuoteApi.md#quotesaverwithdraw) | **GET** /mayachain/quote/saver/withdraw | 
[**quoteswap**](QuoteApi.md#quoteswap) | **GET** /mayachain/quote/swap | 

# **quotesaverdeposit**
> QuoteSaverDepositResponse quotesaverdeposit(height=height, asset=asset, amount=amount)



Provide a quote estimate for the provided saver deposit.

### Example
```python
from __future__ import print_function
import time
import mayanode_client
from mayanode_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = mayanode_client.QuoteApi()
height = 789 # int | optional block height, defaults to current tip (optional)
asset = 'asset_example' # str | the asset to deposit (optional)
amount = 789 # int | the source asset amount in 1e8 decimals (optional)

try:
    api_response = api_instance.quotesaverdeposit(height=height, asset=asset, amount=amount)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling QuoteApi->quotesaverdeposit: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **height** | **int**| optional block height, defaults to current tip | [optional] 
 **asset** | **str**| the asset to deposit | [optional] 
 **amount** | **int**| the source asset amount in 1e8 decimals | [optional] 

### Return type

[**QuoteSaverDepositResponse**](QuoteSaverDepositResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **quotesaverwithdraw**
> QuoteSaverWithdrawResponse quotesaverwithdraw(height=height, asset=asset, address=address, withdraw_bps=withdraw_bps)



Provide a quote estimate for the provided saver withdraw.

### Example
```python
from __future__ import print_function
import time
import mayanode_client
from mayanode_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = mayanode_client.QuoteApi()
height = 789 # int | optional block height, defaults to current tip (optional)
asset = 'asset_example' # str | the asset to withdraw (optional)
address = 'address_example' # str | the address for the position (optional)
withdraw_bps = 789 # int | the basis points of the existing position to withdraw (optional)

try:
    api_response = api_instance.quotesaverwithdraw(height=height, asset=asset, address=address, withdraw_bps=withdraw_bps)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling QuoteApi->quotesaverwithdraw: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **height** | **int**| optional block height, defaults to current tip | [optional] 
 **asset** | **str**| the asset to withdraw | [optional] 
 **address** | **str**| the address for the position | [optional] 
 **withdraw_bps** | **int**| the basis points of the existing position to withdraw | [optional] 

### Return type

[**QuoteSaverWithdrawResponse**](QuoteSaverWithdrawResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **quoteswap**
> QuoteSwapResponse quoteswap(height=height, from_asset=from_asset, to_asset=to_asset, amount=amount, destination=destination, tolerance_bps=tolerance_bps, affiliate_bps=affiliate_bps, affiliate=affiliate)



Provide a quote estimate for the provided swap.

### Example
```python
from __future__ import print_function
import time
import mayanode_client
from mayanode_client.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = mayanode_client.QuoteApi()
height = 789 # int | optional block height, defaults to current tip (optional)
from_asset = 'from_asset_example' # str | the source asset (optional)
to_asset = 'to_asset_example' # str | the target asset (optional)
amount = 789 # int | the source asset amount in 1e8 decimals (optional)
destination = 'destination_example' # str | the destination address, required to generate memo (optional)
tolerance_bps = 789 # int | the maximum basis points from the current feeless swap price to set the limit in the generated memo (optional)
affiliate_bps = 789 # int | the affiliate fee in basis points (optional)
affiliate = 'affiliate_example' # str | the affiliate (address or mayaname) (optional)

try:
    api_response = api_instance.quoteswap(height=height, from_asset=from_asset, to_asset=to_asset, amount=amount, destination=destination, tolerance_bps=tolerance_bps, affiliate_bps=affiliate_bps, affiliate=affiliate)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling QuoteApi->quoteswap: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **height** | **int**| optional block height, defaults to current tip | [optional] 
 **from_asset** | **str**| the source asset | [optional] 
 **to_asset** | **str**| the target asset | [optional] 
 **amount** | **int**| the source asset amount in 1e8 decimals | [optional] 
 **destination** | **str**| the destination address, required to generate memo | [optional] 
 **tolerance_bps** | **int**| the maximum basis points from the current feeless swap price to set the limit in the generated memo | [optional] 
 **affiliate_bps** | **int**| the affiliate fee in basis points | [optional] 
 **affiliate** | **str**| the affiliate (address or mayaname) | [optional] 

### Return type

[**QuoteSwapResponse**](QuoteSwapResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


# xchainpy2_thornode.QuoteApi

All URIs are relative to */*

Method | HTTP request | Description
------------- | ------------- | -------------
[**quoteloanclose**](QuoteApi.md#quoteloanclose) | **GET** /thorchain/quote/loan/close | 
[**quoteloanopen**](QuoteApi.md#quoteloanopen) | **GET** /thorchain/quote/loan/open | 
[**quotesaverdeposit**](QuoteApi.md#quotesaverdeposit) | **GET** /thorchain/quote/saver/deposit | 
[**quotesaverwithdraw**](QuoteApi.md#quotesaverwithdraw) | **GET** /thorchain/quote/saver/withdraw | 
[**quoteswap**](QuoteApi.md#quoteswap) | **GET** /thorchain/quote/swap | 

# **quoteloanclose**
> QuoteLoanCloseResponse quoteloanclose(height=height, from_asset=from_asset, amount=amount, to_asset=to_asset, loan_owner=loan_owner, min_out=min_out)



Provide a quote estimate for the provided loan close.

### Example
```python
from __future__ import print_function
import time
import xchainpy2_thornode
from xchainpy2_thornode.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = xchainpy2_thornode.QuoteApi()
height = 789 # int | optional block height, defaults to current tip (optional)
from_asset = 'from_asset_example' # str | the asset used to repay the loan (optional)
amount = 789 # int | the asset amount in 1e8 decimals (optional)
to_asset = 'to_asset_example' # str | the collateral asset of the loan (optional)
loan_owner = 'loan_owner_example' # str | the owner of the loan collateral (optional)
min_out = 'min_out_example' # str | the minimum amount of the target asset to accept (optional)

try:
    api_response = api_instance.quoteloanclose(height=height, from_asset=from_asset, amount=amount, to_asset=to_asset, loan_owner=loan_owner, min_out=min_out)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling QuoteApi->quoteloanclose: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **height** | **int**| optional block height, defaults to current tip | [optional] 
 **from_asset** | **str**| the asset used to repay the loan | [optional] 
 **amount** | **int**| the asset amount in 1e8 decimals | [optional] 
 **to_asset** | **str**| the collateral asset of the loan | [optional] 
 **loan_owner** | **str**| the owner of the loan collateral | [optional] 
 **min_out** | **str**| the minimum amount of the target asset to accept | [optional] 

### Return type

[**QuoteLoanCloseResponse**](QuoteLoanCloseResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **quoteloanopen**
> QuoteLoanOpenResponse quoteloanopen(height=height, from_asset=from_asset, amount=amount, to_asset=to_asset, destination=destination, min_out=min_out, affiliate_bps=affiliate_bps, affiliate=affiliate)



Provide a quote estimate for the provided loan open.

### Example
```python
from __future__ import print_function
import time
import xchainpy2_thornode
from xchainpy2_thornode.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = xchainpy2_thornode.QuoteApi()
height = 789 # int | optional block height, defaults to current tip (optional)
from_asset = 'from_asset_example' # str | the collateral asset (optional)
amount = 789 # int | the collateral asset amount in 1e8 decimals (optional)
to_asset = 'to_asset_example' # str | the target asset to receive (loan denominated in TOR regardless) (optional)
destination = 'destination_example' # str | the destination address, required to generate memo (optional)
min_out = 'min_out_example' # str | the minimum amount of the target asset to accept (optional)
affiliate_bps = 789 # int | the affiliate fee in basis points (optional)
affiliate = 'affiliate_example' # str | the affiliate (address or thorname) (optional)

try:
    api_response = api_instance.quoteloanopen(height=height, from_asset=from_asset, amount=amount, to_asset=to_asset, destination=destination, min_out=min_out, affiliate_bps=affiliate_bps, affiliate=affiliate)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling QuoteApi->quoteloanopen: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **height** | **int**| optional block height, defaults to current tip | [optional] 
 **from_asset** | **str**| the collateral asset | [optional] 
 **amount** | **int**| the collateral asset amount in 1e8 decimals | [optional] 
 **to_asset** | **str**| the target asset to receive (loan denominated in TOR regardless) | [optional] 
 **destination** | **str**| the destination address, required to generate memo | [optional] 
 **min_out** | **str**| the minimum amount of the target asset to accept | [optional] 
 **affiliate_bps** | **int**| the affiliate fee in basis points | [optional] 
 **affiliate** | **str**| the affiliate (address or thorname) | [optional] 

### Return type

[**QuoteLoanOpenResponse**](QuoteLoanOpenResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **quotesaverdeposit**
> QuoteSaverDepositResponse quotesaverdeposit(height=height, asset=asset, amount=amount)



Provide a quote estimate for the provided saver deposit.

### Example
```python
from __future__ import print_function
import time
import xchainpy2_thornode
from xchainpy2_thornode.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = xchainpy2_thornode.QuoteApi()
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
import xchainpy2_thornode
from xchainpy2_thornode.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = xchainpy2_thornode.QuoteApi()
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
> QuoteSwapResponse quoteswap(height=height, from_asset=from_asset, to_asset=to_asset, amount=amount, destination=destination, streaming_interval=streaming_interval, streaming_quantity=streaming_quantity, from_address=from_address, tolerance_bps=tolerance_bps, affiliate_bps=affiliate_bps, affiliate=affiliate)



Provide a quote estimate for the provided swap.

### Example
```python
from __future__ import print_function
import time
import xchainpy2_thornode
from xchainpy2_thornode.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = xchainpy2_thornode.QuoteApi()
height = 789 # int | optional block height, defaults to current tip (optional)
from_asset = 'from_asset_example' # str | the source asset (optional)
to_asset = 'to_asset_example' # str | the target asset (optional)
amount = 789 # int | the source asset amount in 1e8 decimals (optional)
destination = 'destination_example' # str | the destination address, required to generate memo (optional)
streaming_interval = 789 # int | the interval in which streaming swaps are swapped (optional)
streaming_quantity = 789 # int | the quantity of swaps within a streaming swap (optional)
from_address = 'from_address_example' # str | the from address, required if the from asset is a synth (optional)
tolerance_bps = 789 # int | the maximum basis points from the current feeless swap price to set the limit in the generated memo (optional)
affiliate_bps = 789 # int | the affiliate fee in basis points (optional)
affiliate = 'affiliate_example' # str | the affiliate (address or thorname) (optional)

try:
    api_response = api_instance.quoteswap(height=height, from_asset=from_asset, to_asset=to_asset, amount=amount, destination=destination, streaming_interval=streaming_interval, streaming_quantity=streaming_quantity, from_address=from_address, tolerance_bps=tolerance_bps, affiliate_bps=affiliate_bps, affiliate=affiliate)
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
 **streaming_interval** | **int**| the interval in which streaming swaps are swapped | [optional] 
 **streaming_quantity** | **int**| the quantity of swaps within a streaming swap | [optional] 
 **from_address** | **str**| the from address, required if the from asset is a synth | [optional] 
 **tolerance_bps** | **int**| the maximum basis points from the current feeless swap price to set the limit in the generated memo | [optional] 
 **affiliate_bps** | **int**| the affiliate fee in basis points | [optional] 
 **affiliate** | **str**| the affiliate (address or thorname) | [optional] 

### Return type

[**QuoteSwapResponse**](QuoteSwapResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


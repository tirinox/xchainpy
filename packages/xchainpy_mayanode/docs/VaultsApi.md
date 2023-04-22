# xchainpy2_mayanode.VaultsApi

All URIs are relative to */*

Method | HTTP request | Description
------------- | ------------- | -------------
[**asgard**](VaultsApi.md#asgard) | **GET** /mayachain/vaults/asgard | 
[**vault**](VaultsApi.md#vault) | **GET** /mayachain/vaults/{pubkey} | 
[**vault_pubkeys**](VaultsApi.md#vault_pubkeys) | **GET** /mayachain/vaults/pubkeys | 
[**yggdrasil**](VaultsApi.md#yggdrasil) | **GET** /mayachain/vaults/yggdrasil | 

# **asgard**
> VaultsResponse asgard(height=height)



Returns current asgard vaults.

### Example
```python
from __future__ import print_function
import time
import xchainpy2_mayanode
from xchainpy2_mayanode.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = xchainpy2_mayanode.VaultsApi()
height = 789 # int | optional block height, defaults to current tip (optional)

try:
    api_response = api_instance.asgard(height=height)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling VaultsApi->asgard: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **height** | **int**| optional block height, defaults to current tip | [optional] 

### Return type

[**VaultsResponse**](VaultsResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **vault**
> VaultResponse vault(pubkey, height=height)



Returns the vault for the provided pubkey.

### Example
```python
from __future__ import print_function
import time
import xchainpy2_mayanode
from xchainpy2_mayanode.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = xchainpy2_mayanode.VaultsApi()
pubkey = 'pubkey_example' # str | 
height = 789 # int | optional block height, defaults to current tip (optional)

try:
    api_response = api_instance.vault(pubkey, height=height)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling VaultsApi->vault: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **pubkey** | **str**|  | 
 **height** | **int**| optional block height, defaults to current tip | [optional] 

### Return type

[**VaultResponse**](VaultResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **vault_pubkeys**
> VaultPubkeysResponse vault_pubkeys(height=height)



Returns all pubkeys for current vaults.

### Example
```python
from __future__ import print_function
import time
import xchainpy2_mayanode
from xchainpy2_mayanode.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = xchainpy2_mayanode.VaultsApi()
height = 789 # int | optional block height, defaults to current tip (optional)

try:
    api_response = api_instance.vault_pubkeys(height=height)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling VaultsApi->vault_pubkeys: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **height** | **int**| optional block height, defaults to current tip | [optional] 

### Return type

[**VaultPubkeysResponse**](VaultPubkeysResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **yggdrasil**
> VaultsResponse yggdrasil(height=height)



Returns current yggdrasil vaults.

### Example
```python
from __future__ import print_function
import time
import xchainpy2_mayanode
from xchainpy2_mayanode.rest import ApiException
from pprint import pprint

# create an instance of the API class
api_instance = xchainpy2_mayanode.VaultsApi()
height = 789 # int | optional block height, defaults to current tip (optional)

try:
    api_response = api_instance.yggdrasil(height=height)
    pprint(api_response)
except ApiException as e:
    print("Exception when calling VaultsApi->yggdrasil: %s\n" % e)
```

### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **height** | **int**| optional block height, defaults to current tip | [optional] 

### Return type

[**VaultsResponse**](VaultsResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


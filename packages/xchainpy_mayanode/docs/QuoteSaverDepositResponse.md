# QuoteSaverDepositResponse

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**inbound_address** | **str** | the inbound address for the transaction on the source chain | 
**memo** | **str** | generated memo for the deposit | 
**expected_amount_out** | **str** | the minimum amount of the target asset the user can expect to deposit after fees | 
**inbound_confirmation_blocks** | **int** | the approximate number of source chain blocks required before processing | [optional] 
**inbound_confirmation_seconds** | **int** | the approximate seconds for block confirmations required before processing | [optional] 
**fees** | [**QuoteFees**](QuoteFees.md) |  | 
**slippage_bps** | **int** | the swap slippage in basis points | 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


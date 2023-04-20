# QuoteSaverWithdrawResponse

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**inbound_address** | **str** | the inbound address for the transaction on the source chain | 
**memo** | **str** | generated memo for the withdraw, the client can use this OR send the dust amount | 
**dust_amount** | **str** | the dust amount of the target asset the user should send to initialize the withdraw, the client can send this OR provide the memo | 
**expected_amount_out** | **str** | the minimum amount of the target asset the user can expect to withdraw after fees in 1e8 decimals | 
**outbound_delay_blocks** | **int** | the number of mayachain blocks the outbound will be delayed | 
**outbound_delay_seconds** | **int** | the approximate seconds for the outbound delay before it will be sent | 
**fees** | [**QuoteFees**](QuoteFees.md) |  | 
**slippage_bps** | **int** | the swap slippage in basis points | 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


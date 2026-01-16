# QuoteLimitResponse

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**inbound_address** | **str** | the inbound address for the transaction on the source chain | 
**inbound_confirmation_blocks** | **int** | the approximate number of source chain blocks required before processing | [optional] 
**inbound_confirmation_seconds** | **int** | the approximate seconds for block confirmations required before processing | [optional] 
**outbound_delay_blocks** | **int** | the number of thorchain blocks the outbound will be delayed | [optional] 
**outbound_delay_seconds** | **int** | the approximate seconds for the outbound delay before it will be sent | [optional] 
**fees** | [**QuoteFees**](QuoteFees.md) |  | 
**router** | **str** | the EVM chain router contract address | [optional] 
**expiry** | **int** | expiration timestamp in unix seconds | [optional] 
**warning** | **str** | static warning message | [optional] 
**notes** | **str** | notes about the limit order | [optional] 
**dust_threshold** | **str** | the dust threshold for the source chain | [optional] 
**recommended_min_amount_in** | **str** | the recommended minimum amount in for the limit order | [optional] 
**recommended_gas_rate** | **str** | the recommended gas rate to use for the inbound to ensure timely confirmation | [optional] 
**gas_rate_units** | **str** | the units of the recommended gas rate | [optional] 
**memo** | **str** | generated memo for the limit order | [optional] 
**expected_amount_out** | **str** | the amount of the target asset the user can expect to receive after fees | 
**order_expiry_block** | **int** | the block height when the limit order will expire | 
**order_expiry_timestamp** | **int** | the timestamp when the limit order will expire | 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


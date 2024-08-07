# QuoteSwapResponse

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**inbound_address** | **str** | the inbound address for the transaction on the source chain | [optional] 
**inbound_confirmation_blocks** | **int** | the approximate number of source chain blocks required before processing | [optional] 
**inbound_confirmation_seconds** | **int** | the approximate seconds for block confirmations required before processing | [optional] 
**outbound_delay_blocks** | **int** | the number of mayachain blocks the outbound will be delayed | 
**outbound_delay_seconds** | **int** | the approximate seconds for the outbound delay before it will be sent | 
**fees** | [**QuoteFees**](QuoteFees.md) |  | 
**router** | **str** | the EVM chain router contract address | [optional] 
**expiry** | **int** | expiration timestamp in unix seconds | 
**warning** | **str** | static warning message | 
**notes** | **str** | chain specific quote notes | 
**dust_threshold** | **str** | Defines the minimum transaction size for the chain in base units (sats, wei, uatom). Transactions with asset amounts lower than the dust_threshold are ignored. | [optional] 
**recommended_min_amount_in** | **str** | The recommended minimum inbound amount for this transaction type &amp; inbound asset. Sending less than this amount could result in failed refunds. | [optional] 
**recommended_gas_rate** | **str** | the recommended gas rate to use for the inbound to ensure timely confirmation | [optional] 
**gas_rate_units** | **str** | the units of the recommended gas rate | [optional] 
**memo** | **str** | generated memo for the swap | [optional] 
**expected_amount_out** | **str** | the amount of the target asset the user can expect to receive after fees | 
**max_streaming_quantity** | **int** | the maximum amount of trades a streaming swap can do for a trade | [optional] 
**streaming_swap_blocks** | **int** | the number of blocks the streaming swap will execute over | [optional] 
**streaming_swap_seconds** | **int** | approx the number of seconds the streaming swap will execute over | [optional] 
**total_swap_seconds** | **int** | total number of seconds a swap is expected to take (inbound conf + streaming swap + outbound delay) | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


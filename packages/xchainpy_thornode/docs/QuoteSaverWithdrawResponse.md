# QuoteSaverWithdrawResponse

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**inbound_address** | **str** | the inbound address for the transaction on the source chain | 
**inbound_confirmation_blocks** | **int** | the approximate number of source chain blocks required before processing | [optional] 
**inbound_confirmation_seconds** | **int** | the approximate seconds for block confirmations required before processing | [optional] 
**outbound_delay_blocks** | **int** | the number of thorchain blocks the outbound will be delayed | 
**outbound_delay_seconds** | **int** | the approximate seconds for the outbound delay before it will be sent | 
**fees** | [**QuoteFees**](QuoteFees.md) |  | 
**slippage_bps** | **int** | the total swap slippage in basis points | 
**router** | **str** | the EVM chain router contract address | [optional] 
**expiry** | **int** | expiration timestamp in unix seconds | 
**warning** | **str** | static warning message | 
**notes** | **str** | chain specific quote notes | 
**dust_threshold** | **str** | Defines the minimum transaction size for the chain in base units (sats, wei, uatom). Transctions with asset amounts lower than the dust_threshold are ignored. | [optional] 
**recommended_min_amount_in** | **str** | The recommended minimum inbound amount for this transaction type &amp; inbound asset. Sending less than this amount could result in failed refunds. | [optional] 
**memo** | **str** | generated memo for the withdraw, the client can use this OR send the dust amount | 
**dust_amount** | **str** | the dust amount of the target asset the user should send to initialize the withdraw, the client can send this OR provide the memo | 
**expected_amount_out** | **str** | the amount of the target asset the user can expect to withdraw after fees in 1e8 decimals | 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


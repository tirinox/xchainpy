# BaseQuoteResponse

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**inbound_address** | **str** | the inbound address for the transaction on the source chain | [optional] 
**inbound_confirmation_blocks** | **int** | the approximate number of source chain blocks required before processing | [optional] 
**inbound_confirmation_seconds** | **int** | the approximate seconds for block confirmations required before processing | [optional] 
**outbound_delay_blocks** | **int** | the number of thorchain blocks the outbound will be delayed | [optional] 
**outbound_delay_seconds** | **int** | the approximate seconds for the outbound delay before it will be sent | [optional] 
**fees** | [**QuoteFees**](QuoteFees.md) |  | [optional] 
**slippage_bps** | **int** | Deprecated - migrate to fees object. | [optional] 
**streaming_slippage_bps** | **int** | Deprecated - migrate to fees object. | [optional] 
**router** | **str** | the EVM chain router contract address | [optional] 
**expiry** | **int** | expiration timestamp in unix seconds | [optional] 
**warning** | **str** | static warning message | [optional] 
**notes** | **str** | chain specific quote notes | [optional] 
**dust_threshold** | **str** | Defines the minimum transaction size for the chain in base units (sats, wei, uatom). Transactions with asset amounts lower than the dust_threshold are ignored. | [optional] 
**recommended_min_amount_in** | **str** | The recommended minimum inbound amount for this transaction type &amp; inbound asset. Sending less than this amount could result in failed refunds. | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


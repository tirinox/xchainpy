# QuoteSaverDepositResponse

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**inbound_address** | **str** | the inbound address for the transaction on the source chain | 
**inbound_confirmation_blocks** | **int** | the approximate number of source chain blocks required before processing | [optional] 
**inbound_confirmation_seconds** | **int** | the approximate seconds for block confirmations required before processing | [optional] 
**outbound_delay_blocks** | **int** | the number of thorchain blocks the outbound will be delayed | [optional] 
**outbound_delay_seconds** | **int** | the approximate seconds for the outbound delay before it will be sent | [optional] 
**fees** | [**QuoteFees**](QuoteFees.md) |  | 
**slippage_bps** | **int** | the total swap slippage in basis points | 
**router** | **str** | the EVM chain router contract address | [optional] 
**expiry** | **int** | expiration timestamp in unix seconds | 
**warning** | **str** | static warning message | 
**notes** | **str** | chain specific quote notes | 
**dust_threshold** | **str** | Defines the minimum transaction size for the chain in base units (sats, wei, uatom). Transctions with asset amounts lower than the dust_threshold are ignored. | [optional] 
**memo** | **str** | generated memo for the deposit | 
**expected_amount_out** | **str** | migrate to expected_amount_deposit (will be deprecated in v1.104) | 
**expected_amount_deposit** | **str** | the amount of the target asset the user can expect to deposit after fees | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


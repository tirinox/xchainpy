# InboundConfirmationCountedStage

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**counting_start_height** | **int** | the THORChain block height when confirmation counting began | [optional] 
**chain** | **str** | the external source chain for which confirmation counting takes place | [optional] 
**external_observed_height** | **int** | the block height on the external source chain when the transaction was observed | [optional] 
**external_confirmation_delay_height** | **int** | the block height on the external source chain when confirmation counting will be complete | [optional] 
**remaining_confirmation_seconds** | **int** | the estimated remaining seconds before confirmation counting completes | [optional] 
**completed** | **bool** | returns true if no transaction confirmation counting remains to be done | 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


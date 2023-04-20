# ObservedTx

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**tx** | [**Tx**](Tx.md) |  | 
**status** | **str** |  | [optional] 
**out_hashes** | **list[str]** |  | [optional] 
**block_height** | **int** | same as external_observed_height, to be deprecated in favour of external_observed_height | [optional] 
**external_observed_height** | **int** | the block height on the external source chain when the transaction was observed, not provided if chain is THOR | [optional] 
**signers** | **list[str]** |  | [optional] 
**observed_pub_key** | **str** |  | [optional] 
**keysign_ms** | **int** |  | [optional] 
**finalise_height** | **int** | same as external_confirmation_delay_height, to be deprecated in favour of external_confirmation_delay_height | [optional] 
**external_confirmation_delay_height** | **int** | the block height on the external source chain when confirmation counting will be complete, not provided if chain is THOR | [optional] 
**aggregator** | **str** | the outbound aggregator to use, will also match a suffix | [optional] 
**aggregator_target** | **str** | the aggregator target asset provided to transferOutAndCall | [optional] 
**aggregator_target_limit** | **str** | the aggregator target asset limit provided to transferOutAndCall | [optional] 

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)

